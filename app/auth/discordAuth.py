
import os
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qsl, urlencode, urlparse

import jwt
import requests


class DiscordAuth:
    def __init__(self, discordAuthURL, discordClientID, discordClientSecret, redirectURI):
        self.discordAuthURL = discordAuthURL
        self.discordClientID = discordClientID
        self.discordClientSecret = discordClientSecret
        self.redirectURI = self._normalize_redirect_uri(redirectURI)
        self.jwt_secret = (
            os.getenv("JWT_SECRET_KEY")
            or os.getenv("jwtSecretKey")
            or os.getenv("PROD_SECRET_KEY")
        )
        if not self.jwt_secret:
            raise RuntimeError(
                "JWT_SECRET_KEY environment variable is required for production auth. "
                "Do not use a placeholder or default secret."
            )
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        if self.jwt_algorithm.startswith("HS") and len(self.jwt_secret.encode("utf-8")) < 32:
            raise RuntimeError("JWT_SECRET_KEY must be at least 32 characters long for HS256/HMAC signing.")
        self.jwt_expiration_minutes = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))

    @staticmethod
    def _normalize_redirect_uri(uri: str | None) -> str:
        if not uri:
            raise ValueError("Discord redirect URI is required.")
        return uri.strip().replace(" ", "")

    def get_auth_url(self):
        if not self.discordAuthURL:
            raise ValueError("discordOAuthURI is not configured.")

        parsed = urlparse(self.discordAuthURL)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("discordOAuthURI must be a valid Discord OAuth URL.")

        params = dict(parse_qsl(parsed.query, keep_blank_values=True))
        params.update(
            {
                "client_id": self.discordClientID,
                "response_type": "code",
                "redirect_uri": self.redirectURI,
                "scope": params.get("scope", "identify email guilds"),
                "prompt": "consent",
            }
        )
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(params, doseq=True)}"

    def exchange_code_for_token(self, code):
        if not code or not str(code).strip():
            raise ValueError("Authorization code is required")

        data = {
            "client_id": self.discordClientID,
            "client_secret": self.discordClientSecret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirectURI,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            "https://discord.com/api/v10/oauth2/token",
            data=data,
            headers=headers,
            auth=(self.discordClientID, self.discordClientSecret),
            timeout=30,
        )

        if response.status_code != 200:
            error_payload = response.json() if response.headers.get("Content-Type", "").startswith("application/json") else {"error": response.text}
            error_message = error_payload.get("error_description") or error_payload.get("error") or "Failed to exchange code for token"
            raise ValueError(f"Discord token exchange failed: {error_message}")

        token_data = response.json()
        user_data = self.get_user_info(token_data["access_token"])
        token_data["user"] = user_data
        token_data["jwt"] = self.generate_jwt(
            {
                "sub": str(user_data.get("id")),
                "username": user_data.get("username"),
                "global_name": user_data.get("global_name"),
                "email": user_data.get("email"),
            }
        )
        return token_data

    def refresh_token(self, refresh_token):
        if not refresh_token:
            raise ValueError("Refresh token is required")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            url="https://discord.com/api/v10/oauth2/token",
            data=data,
            headers=headers,
            auth=(self.discordClientID, self.discordClientSecret),
            timeout=30,
        )
        if response.status_code != 200:
            error_payload = response.json() if response.headers.get("Content-Type", "").startswith("application/json") else {"error": response.text}
            error_message = error_payload.get("error_description") or error_payload.get("error") or "Failed to refresh token"
            raise ValueError(f"Discord token refresh failed: {error_message}")
        return response.json()

    def revoke_token(self, token):
        if not token:
            raise ValueError("Token is required")

        data = {
            "token": token,
            "token_type_hint": "access_token",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            url="https://discord.com/api/v10/oauth2/token/revoke",
            data=data,
            headers=headers,
            auth=(self.discordClientID, self.discordClientSecret),
            timeout=30,
        )
        if response.status_code != 200:
            error_payload = response.json() if response.headers.get("Content-Type", "").startswith("application/json") else {"error": response.text}
            error_message = error_payload.get("error_description") or error_payload.get("error") or "Failed to revoke token"
            raise ValueError(f"Discord token revocation failed: {error_message}")
        return response.json()

    def get_user_info(self, accessToken):
        headers = {"Authorization": f"Bearer {accessToken}"}
        response = requests.get(
            url="https://discord.com/api/v10/users/@me",
            headers=headers,
            timeout=30,
        )

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            raise ValueError("Discord access token is invalid or expired.")
        if response.status_code == 400:
            raise ValueError("Discord OAuth redirect URI or credentials are invalid.")
        raise ValueError(f"Failed to fetch Discord user details: {response.status_code}")

    def generate_jwt(self, payload=None):
        now = datetime.now(timezone.utc)
        token_payload = {
            "iat": int(now.timestamp()),
            "nbf": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self.jwt_expiration_minutes)).timestamp()),
        }
        if payload:
            token_payload.update(payload)
        return jwt.encode(token_payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def verify_jwt(self, token):
        if not token:
            raise ValueError("JWT token is required.")
        try:
            return jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
        except jwt.PyJWTError as exc:
            raise ValueError("JWT token is invalid or expired.") from exc