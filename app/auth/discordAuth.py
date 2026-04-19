# Flow:
# User clicks “Login with Discord”
# Redirect to Discord authorization URL
# User logs in + approves permissions
# Discord redirects back with code
# Backend exchanges code → access_token
# Backend fetches user info using token
# You create session / JWT

import discord
import os
import requests


class DiscordAuth:
    def __init__(self, discordAuthURL, discordClientID, discordClientSecret, redirectURI):
        self.discordAuthURL = discordAuthURL
        self.discordClientID = discordClientID
        self.discordClientSecret = discordClientSecret
        self.redirectURI = redirectURI
        self.jwt_secret = os.getenv("jwtSecretKey", "development_secret_key")
        self.jwt_algorithm = "HS256"

    def get_auth_url(self):
        return self.discordAuthURL
    
    def exchange_code_for_token(self, code):
        
        if code is None:
            raise ValueError("Authorization code is required")
        print(f"Using redirect_uri: {self.redirectURI}")
        data = {
            'client_id': self.discordClientID,
            'client_secret': self.discordClientSecret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirectURI  # Must match the redirect URI used in the authorization step

        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers, auth=(self.discordClientID, self.discordClientSecret))
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to exchange code: status {response.status_code}, response: {response.text}")
            raise Exception("Failed to exchange code for token")
        
    def refresh_token( self, access_tokenb):
        pass
        
    def get_user_info(self, accessToken):
        data = {}
        headers = {
            "Authorization": f"Bearer {accessToken}",
        }
        response = requests.get(
            url='https://discord.com/api/v10/users/@me', 
            data=data, 
            headers=headers
        )
        
        # db.add_many(all, fields, you, want)
        
        if response.status_code == 200:
            return response.json()
        else:
            if response.status_code == 401:
                raise Exception(status_code =response.status_code, detail = "check for auth / headers")
            if response.status_code == 400:
                raise Exception(status_code =response.status_code, detail = "confirm URI")
            print(response.status_code, response.text)
            raise Exception(status_code =response.status_code, detail = "Failed to fetch the details")
        
    def generate_jwt():
        pass