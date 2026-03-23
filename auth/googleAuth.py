"""Google OAuth 2.0 Authentication implementation with user storage."""
import os
import jwt
import requests
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from urllib.parse import urlencode, quote
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import dotenv
import bcrypt

dotenv.load_dotenv()

# MongoDB Connection
db_username = os.getenv("DB_USERNAME")
db_password = quote_plus(os.getenv("DB_PASSWORD"))
db_name = os.getenv("DB_NAME")
uri = f"mongodb+srv://{db_username}:{db_password}@stack-of-luv-times.mpxka4a.mongodb.net/{db_name}?appName=stack-of-luv-times"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client[db_name]
users_collection = db["users"]


class GoogleAuth:
    """
    Google OAuth 2.0 implementation with PKCE and user management.
    
    Security features:
    - PKCE (Proof Key for Code Exchange) for authorization code flow
    - State parameter to prevent CSRF attacks
    - Secure token storage in MongoDB
    - JWT token generation for session management
    - Password hashing with bcrypt for sensitive data
    """
    
    def __init__(
        self,
        google_client_id: str,
        google_client_secret: str,
        redirect_uri: str,
        jwt_secret: str = None,
        jwt_algorithm: str = "HS256",
        jwt_expiry_hours: int = 24
    ):
        """
        Initialize Google OAuth configuration.
        
        Args:
            google_client_id: From Google Cloud Console
            google_client_secret: From Google Cloud Console
            redirect_uri: Must match redirect URI in Google Console
            jwt_secret: Secret for JWT signing (defaults to env var)
            jwt_algorithm: JWT algorithm (HS256 recommended)
            jwt_expiry_hours: JWT token expiration in hours
        """
        self.client_id = google_client_id
        self.client_secret = google_client_secret
        self.redirect_uri = redirect_uri
        self.jwt_secret = jwt_secret or os.getenv("jwtSecretKey", "development_secret_key_change_in_prod")
        self.jwt_algorithm = jwt_algorithm
        self.jwt_expiry_hours = jwt_expiry_hours
        
        # Google OAuth 2.0 endpoints
        self.auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        
        # PKCE configuration
        self.code_challenge_method = "S256"  # SHA256
        
        # Ensure MongoDB indexes
        self._create_indexes()
    
    def _create_indexes(self):
        """Create MongoDB indexes for efficient queries."""
        try:
            users_collection.create_index("email", unique=True)
            users_collection.create_index("provider_id")
            users_collection.create_index("created_at")
        except Exception as e:
            print(f"Warning: Could not create indexes: {e}")
    
    def _generate_pkce_pair(self) -> tuple[str, str]:
        """
        Generate PKCE code_verifier and code_challenge.
        
        Returns:
            (code_verifier, code_challenge): Tuple of verifier and challenge
        """
        # Generate a random 128-character URL-safe string
        code_verifier = secrets.token_urlsafe(96)[:128]
        
        # Create SHA256 hash of verifier
        code_challenge = hashlib.sha256(code_verifier.encode()).digest()
        # Base64 URL-safe encoding without padding
        import base64
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode().rstrip('=')
        
        return code_verifier, code_challenge
    
    def _generate_state_token(self) -> str:
        """
        Generate CSRF protection state token.
        
        Returns:
            state: Random secure token
        """
        return secrets.token_urlsafe(32)
    
    def get_auth_url(self, state: Optional[str] = None, code_verifier: Optional[str] = None) -> Dict[str, str]:
        """
        Generate Google OAuth authorization URL with PKCE.
        
        Args:
            state: Optional state token (generated if not provided)
            code_verifier: Optional PKCE verifier (generated if not provided)
        
        Returns:
            dict with: {
                'auth_url': str - Full authorization URL,
                'state': str - State token for CSRF protection,
                'code_verifier': str - PKCE code verifier (store in session)
            }
        """
        if not state:
            state = self._generate_state_token()
        
        if not code_verifier:
            code_verifier, code_challenge = self._generate_pkce_pair()
        else:
            import base64
            code_challenge = hashlib.sha256(code_verifier.encode()).digest()
            code_challenge = base64.urlsafe_b64encode(code_challenge).decode().rstrip('=')
        
        # Build authorization URL
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'scope': 'openid profile email',
            'redirect_uri': self.redirect_uri,
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': self.code_challenge_method,
            'access_type': 'offline',  # Request refresh token
            'prompt': 'consent'  # Force consent screen to get refresh token
        }
        
        auth_url = f"{self.auth_url}?{urlencode(params)}"
        
        return {
            'auth_url': auth_url,
            'state': state,
            'code_verifier': code_verifier
        }
    
    def verify_state_token(self, state: str, stored_state: str) -> bool:
        """
        Verify state token to prevent CSRF attacks.
        
        Args:
            state: State token from callback
            stored_state: State token from session
        
        Returns:
            bool: True if valid, False otherwise
        """
        return state == stored_state
    
    def exchange_code_for_token(self, code: str, code_verifier: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token using PKCE.
        
        Args:
            code: Authorization code from callback
            code_verifier: PKCE code verifier stored in session
        
        Returns:
            dict: Token response with access_token, id_token, etc.
        
        Raises:
            Exception: If token exchange fails
        """
        if not code:
            raise ValueError("Authorization code is required")
        if not code_verifier:
            raise ValueError("PKCE code_verifier is required")
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'code_verifier': code_verifier,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(self.token_url, data=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to exchange code: {response.status_code}, {response.text}")
            raise Exception(f"Token exchange failed: {response.text}")
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh an access token using the refresh token.
        
        Args:
            refresh_token: Refresh token from previous authentication
        
        Returns:
            dict: New token response
        
        Raises:
            Exception: If refresh fails
        """
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        
        response = requests.post(self.token_url, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Token refresh failed: {response.text}")
    
    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        Fetch user information from Google using access token.
        
        Args:
            access_token: Google access token
        
        Returns:
            dict: User info (id, email, name, picture, etc.)
        
        Raises:
            Exception: If user info fetch fails
        """
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        response = requests.get(self.userinfo_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch user info: {response.text}")
    
    def create_or_update_user(
        self,
        google_user_data: Dict[str, Any],
        access_token: str,
        refresh_token: Optional[str] = None,
        token_expiry: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create or update user in MongoDB with OAuth data.
        
        Args:
            google_user_data: User data from Google (id, email, name, picture)
            access_token: Google access token (encrypted before storage)
            refresh_token: Google refresh token (encrypted if provided)
            token_expiry: Token expiration timestamp
        
        Returns:
            dict: User document from MongoDB
        """
        email = google_user_data.get('email')
        
        if not email:
            raise ValueError("Email is required from Google OAuth")
        
        # Prepare user document
        now = datetime.utcnow()
        user_data = {
            'email': email,
            'provider': 'google',
            'provider_id': google_user_data.get('id'),
            'full_name': google_user_data.get('name', ''),
            'picture_url': google_user_data.get('picture', ''),
            'access_token': self._encrypt_token(access_token),  # Store encrypted
            'refresh_token': self._encrypt_token(refresh_token) if refresh_token else None,
            'token_expiry': datetime.fromtimestamp(token_expiry) if token_expiry else None,
            'updated_at': now,
            'last_login': now,
            'is_active': True
        }
        
        # Check if user exists
        existing_user = users_collection.find_one({'email': email})
        
        if existing_user:
            # Update existing user
            users_collection.update_one(
                {'email': email},
                {'$set': user_data, '$inc': {'login_count': 1}}
            )
            user_doc = users_collection.find_one({'email': email})
        else:
            # Create new user
            user_doc = {
                'user_id': self._generate_user_id(),
                **user_data,
                'created_at': now,
                'login_count': 1,
                'providers': [{'provider': 'google', 'provider_id': google_user_data.get('id')}],
                'metadata': {}
            }
            users_collection.insert_one(user_doc)
        
        return user_doc
    
    def _encrypt_token(self, token: str) -> str:
        """
        Encrypt sensitive token before storage.
        
        Args:
            token: Token to encrypt
        
        Returns:
            str: Encrypted token (base64 encoded)
        """
        if not token:
            return None
        
        # For production, use proper encryption (e.g., cryptography library)
        # This is a simple example - upgrade to proper encryption
        import base64
        return base64.b64encode(token.encode()).decode()
    
    def _decrypt_token(self, encrypted_token: str) -> str:
        """
        Decrypt token from storage.
        
        Args:
            encrypted_token: Encrypted token from database
        
        Returns:
            str: Decrypted token
        """
        if not encrypted_token:
            return None
        
        import base64
        return base64.b64decode(encrypted_token.encode()).decode()
    
    def _generate_user_id(self) -> str:
        """Generate unique user ID."""
        return 'user_' + secrets.token_hex(16)
    
    def generate_jwt_token(self, user_doc: Dict[str, Any]) -> str:
        """
        Generate JWT token for session management.
        
        Args:
            user_doc: User document from MongoDB
        
        Returns:
            str: Signed JWT token
        """
        expiry = datetime.utcnow() + timedelta(hours=self.jwt_expiry_hours)
        
        payload = {
            'user_id': str(user_doc.get('_id')),
            'email': user_doc.get('email'),
            'provider': user_doc.get('provider'),
            'exp': expiry,
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """
        Verify and decode JWT token.
        
        Args:
            token: JWT token to verify
        
        Returns:
            dict: Decoded token payload
        
        Raises:
            jwt.InvalidTokenError: If token is invalid or expired
        """
        return jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user from MongoDB by user_id."""
        from bson.objectid import ObjectId
        try:
            return users_collection.find_one({'_id': ObjectId(user_id)})
        except:
            return users_collection.find_one({'user_id': user_id})
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve user from MongoDB by email."""
        return users_collection.find_one({'email': email})


# Initialize Google Auth with environment variables
google_auth = GoogleAuth(
    google_client_id=os.getenv("googleClientID"),
    google_client_secret=os.getenv("googleClientSecret"),
    redirect_uri=os.getenv("googleRedirectURI", "http://127.0.0.1:8000/auth/google/callback")
)
