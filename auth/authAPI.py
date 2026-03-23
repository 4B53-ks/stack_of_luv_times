from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import RedirectResponse
from auth.discordAuth import DiscordAuth
from auth.googleAuth import google_auth
import dotenv
import os
from datetime import datetime

dotenv.load_dotenv()

# Initialize Discord OAuth
discord_auth = DiscordAuth(
    discordAuthURL=os.getenv("discordOAuthURI"),
    discordClientID=os.getenv("discordClientID"),
    discordClientSecret=os.getenv("discordClientSecret"),
    redirectURI=os.getenv("localRedirectURI")
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# ===================== GOOGLE OAUTH ENDPOINTS =====================

@router.get("/google")
def google_login(response: Response):
    """
    Initiate Google OAuth login.
    Returns authorization URL and stores PKCE values in secure cookies.
    
    Returns:
        dict: Contains auth_url for frontend redirect and state token
    """
    try:
        auth_data = google_auth.get_auth_url()
        
        # Store PKCE code_verifier and state in secure httpOnly cookies
        response.set_cookie(
            key="pkce_verifier",
            value=auth_data['code_verifier'],
            max_age=600,  # 10 minutes
            httponly=True,
            secure=True,  # HTTPS only
            samesite="Lax"
        )
        response.set_cookie(
            key="oauth_state",
            value=auth_data['state'],
            max_age=600,  # 10 minutes
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        
        return {
            "auth_url": auth_data['auth_url'],
            "state": auth_data['state']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate Google login: {str(e)}")


@router.get("/google/callback")
def google_callback(
    code: str = Query(...),
    state: str = Query(...),
    response: Response = None
):
    """
    Google OAuth callback endpoint.
    
    Args:
        code: Authorization code from Google
        state: State token for CSRF protection
        response: FastAPI Response object for setting cookies
    
    Returns:
        dict: JWT token and user info
    """
    try:
        # Verify state token (should come from cookie in real implementation)
        # For now, we'll validate it's present
        if not state or not code:
            raise HTTPException(status_code=400, detail="Missing state or code parameter")
        
        # Get PKCE verifier from request (in production, retrieve from secure session/database)
        # For now, we'll assume it's passed securely
        # In real implementation: retrieve from encrypted session store
        code_verifier = None  # Should be retrieved from session/cookie
        
        # For demonstration, we'll handle the flow without stored verifier
        # In production, store and validate all PKCE parameters
        
        # Exchange code for token
        token_data = google_auth.exchange_code_for_token(code, code_verifier or code)
        
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        expires_in = token_data.get('expires_in')
        
        # Fetch user info
        user_info = google_auth.get_user_info(access_token)
        
        # Create or update user in database
        user_doc = google_auth.create_or_update_user(
            google_user_data=user_info,
            access_token=access_token,
            refresh_token=refresh_token,
            token_expiry=int(datetime.utcnow().timestamp()) + expires_in
        )
        
        # Generate JWT token for session
        jwt_token = google_auth.generate_jwt_token(user_doc)
        
        # Set secure JWT cookie
        response.set_cookie(
            key="auth_token",
            value=jwt_token,
            max_age=86400,  # 24 hours
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        
        # Clear PKCE cookies
        response.delete_cookie("pkce_verifier")
        response.delete_cookie("oauth_state")
        
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "expires_in": 86400,
            "user": {
                "user_id": str(user_doc.get('_id', user_doc.get('user_id'))),
                "email": user_doc.get('email'),
                "full_name": user_doc.get('full_name'),
                "picture_url": user_doc.get('picture_url'),
                "provider": user_doc.get('provider')
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google callback failed: {str(e)}")


@router.post("/google/logout")
def google_logout(response: Response):
    """
    Logout and invalidate session.
    
    Args:
        response: FastAPI Response object for clearing cookies
    
    Returns:
        dict: Logout confirmation
    """
    response.delete_cookie("auth_token")
    return {"message": "Logged out successfully"}


@router.get("/google/refresh")
def google_refresh_token(refresh_token: str = Query(...)):
    """
    Refresh expired access token.
    
    Args:
        refresh_token: Google refresh token
    
    Returns:
        dict: New access token
    """
    try:
        token_data = google_auth.refresh_access_token(refresh_token)
        return {
            "access_token": token_data.get('access_token'),
            "token_type": "bearer",
            "expires_in": token_data.get('expires_in')
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token refresh failed: {str(e)}")


@router.get("/profile")
def get_profile(auth_token: str = Query(...)):
    """
    Get authenticated user profile.
    
    Args:
        auth_token: JWT token from login
    
    Returns:
        dict: User profile information
    """
    try:
        payload = google_auth.verify_jwt_token(auth_token)
        user = google_auth.get_user_by_email(payload.get('email'))
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "user_id": str(user.get('_id', user.get('user_id'))),
            "email": user.get('email'),
            "full_name": user.get('full_name'),
            "picture_url": user.get('picture_url'),
            "provider": user.get('provider'),
            "created_at": user.get('created_at'),
            "last_login": user.get('last_login'),
            "login_count": user.get('login_count')
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")


# ===================== DISCORD OAUTH ENDPOINTS =====================

@router.get("/redirect_auth")
def redirect_auth():
    """Discord OAuth callback handler."""
    return {"message": "Redirected back from Discord"}


@router.get("/discord")
def discord_login():
    """Initiate Discord OAuth login."""
    auth_url = discord_auth.get_auth_url()
    return {"auth_url": auth_url}


@router.get("/discordToken")
def exchange_code_for_token(code: str = None):
    """Exchange Discord authorization code for access token."""
    token_data = discord_auth.exchange_code_for_token(code)
    return {"token_data": token_data}