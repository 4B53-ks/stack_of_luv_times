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
from db.dbWrite import db_write
from basic_data.dataModel import userData


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
        response = requests.post('https://discord.com/api/v10/oauth2/token', data=data, headers=headers, auth=(self.discordClientID, self.discordClientSecret))
        if response.status_code == 200:
            
            # db data write
            # {"token_data":
            #     {"token_type":"Bearer",
            #      "access_token":"MTQ4NDU0MTYzODAwODI0NjMwMg.Vr50Rt0WDvctqUz6ZScvelaJmM7Xwc",
            #      "expires_in":604800,
            #      "refresh_token":"TLkXxH6iHwHYXS21ijISwfVnhyvTqH",
            #      "scope":"email identify connections guilds"
            #      }
            #     }
            respJSON = response.json()
            print(respJSON)
            print(respJSON["access_token"])
            
            user_data__response = self.get_user_info(respJSON["access_token"])
            print(user_data__response)
            
            return response.json()
        else:
            print(f"Failed to exchange code: status {response.status_code}, response: {response.text}")
            raise Exception("Failed to exchange code for token")
        
    def refresh_token(self, refresh_token):
        if refresh_token is None:
            raise ValueError("Refresh token is required")
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'Content-Type':'application/x-www-form-urlencoded'
        }
        response = requests.post(url='https://discord.com/api/v10/oauth2/token', data=data, headers=headers, auth=(self.discordClientID, self.discordClientSecret))
        if 200 == response.status_code:
            response.raise_for_status()
            return response.json()
        else:
            print(f"Failed to exchange code: status {response.status_code}, response: {response.text}")
            raise Exception("Failed to exchange code for token")
        
    def revoke_token( self, token):
        if self.refresh_token is None:
            raise ValueError("Authorization code is required")
        data = {
            'token': token,
            'token_type_hint': 'access_token'
        }
        headers = {
            'Content-Type':'application/x-www-form-urlencoded'
        }
        response = requests.post(url='https://discord.com/api/v10/oauth2/token/revoke', data=data, headers=headers, auth=(self.discordClientID, self.discordClientSecret))
        if 200 == response.status_code:
            response.raise_for_status()
            return response.json()
        else:
            print(f"Failed to exchange code: status {response.status_code}, response: {response.text}")
            raise Exception("Failed to exchange code for token")
        
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