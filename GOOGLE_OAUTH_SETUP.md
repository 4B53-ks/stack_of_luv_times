# Google OAuth Setup Guide & Security Configuration

## 📋 Required URIs for Google Cloud Console

### Callback URI
```
http://127.0.0.1:8000/auth/google/callback
```
**Production Callback URI:**
```
https://yourdomain.com/auth/google/callback
```

### JavaScript Origins (CORS)
Add these to your Google OAuth credentials:
```
http://localhost:3000
http://127.0.0.1:3000
http://localhost:8000
http://127.0.0.1:8000
https://yourdomain.com
```

### Authorized Redirect URIs in Google Cloud Console
Add ALL of these:
```
http://127.0.0.1:8000/auth/google/callback
http://localhost:8000/auth/google/callback
https://yourdomain.com/auth/google/callback
```

---

## 🔐 Environment Variables Required

Add these to your `.env` file:

```env
# Google OAuth Credentials (from Google Cloud Console)
googleClientID=YOUR_CLIENT_ID.apps.googleusercontent.com
googleClientSecret=YOUR_CLIENT_SECRET
googleRedirectURI=http://127.0.0.1:8000/auth/google/callback

# JWT Configuration
jwtSecretKey=YOUR_VERY_SECURE_RANDOM_SECRET_KEY_MIN_32_CHARS

# MongoDB (already configured)
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_NAME=stack_of_luv_times
```

---

## 🚀 Setup Steps in Google Cloud Console

### 1. Create OAuth 2.0 Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable Google+ API:
   - Go to APIs & Services → Library
   - Search for "Google+ API"
   - Click "Enable"
4. Go to APIs & Services → Credentials
5. Click "Create Credentials" → "OAuth client ID"
6. Choose "Web application"
7. Add to "Authorized JavaScript origins":
   ```
   http://localhost:3000
   http://127.0.0.1:3000
   http://localhost:8000
   http://127.0.0.1:8000
   https://yourdomain.com
   ```
8. Add to "Authorized redirect URIs":
   ```
   http://127.0.0.1:8000/auth/google/callback
   http://localhost:8000/auth/google/callback
   https://yourdomain.com/auth/google/callback
   ```
9. Copy your Client ID and Client Secret
10. Add to `.env` file

---

## 🔒 Security Features Implemented

### 1. **PKCE (Proof Key for Code Exchange)**
- Prevents authorization code interception attacks
- Especially important for mobile/SPA apps
- Code verifier stored in httpOnly cookie
- Code challenge sent to Google

### 2. **State Token (CSRF Protection)**
- Random state generated for each login request
- Verified on callback
- Prevents Cross-Site Request Forgery attacks
- Stored in secure httpOnly cookie

### 3. **Secure Token Storage**
- Access tokens encrypted before MongoDB storage
- Refresh tokens encrypted in database
- Never expose tokens in API responses directly
- Use JWT for session management instead

### 4. **HTTPOnly Cookies**
- Auth tokens stored in secure httpOnly cookies
- Prevents XSS attacks from stealing cookies
- Automatically sent with requests
- Cannot be accessed via JavaScript

### 5. **HTTPS/Secure Flag**
- Set `secure=True` on cookies (requires HTTPS in production)
- All token transmissions over HTTPS
- Prevent man-in-the-middle attacks

### 6. **SameSite Cookie Policy**
- Set to "Lax" to prevent CSRF attacks
- Cookies not sent in cross-site requests
- Protects against unauthorized state transitions

### 7. **Token Expiration**
- Short-lived JWT tokens (24 hours default)
- Refresh tokens for longer sessions
- Expired tokens automatically rejected
- User must re-authenticate after expiration

### 8. **Password Hashing (Ready)**
- bcrypt imported for future password hashing
- Sensitive data encrypted before storage
- One-way hashing for irreversible security

---

## 📡 API Endpoints

### Login Flow

#### 1. Initiate Login
```
GET /auth/google
```
**Response:**
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?...",
  "state": "random_state_token"
}
```
**Frontend Action:** Redirect user to `auth_url`

#### 2. Handle Callback (Automatic)
```
GET /auth/google/callback?code={CODE}&state={STATE}
```
**Handled automatically by backend**

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "user_id": "user_abc123def456",
    "email": "user@example.com",
    "full_name": "John Doe",
    "picture_url": "https://lh3.googleusercontent.com/...",
    "provider": "google"
  }
}
```

#### 3. Get User Profile
```
GET /auth/profile?auth_token={JWT_TOKEN}
```
**Response:**
```json
{
  "user_id": "user_abc123def456",
  "email": "user@example.com",
  "full_name": "John Doe",
  "picture_url": "https://...",
  "provider": "google",
  "created_at": "2026-03-21T10:30:00",
  "last_login": "2026-03-21T10:35:00",
  "login_count": 5
}
```

#### 4. Refresh Token
```
GET /auth/google/refresh?refresh_token={REFRESH_TOKEN}
```
**Response:**
```json
{
  "access_token": "new_jwt_token",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### 5. Logout
```
POST /auth/google/logout
```
**Response:**
```json
{
  "message": "Logged out successfully"
}
```

---

## 💾 MongoDB User Document Structure

Users are stored in collection `users`:

```json
{
  "_id": ObjectId("..."),
  "user_id": "user_abc123def456",
  "email": "user@example.com",
  "provider": "google",
  "provider_id": "1234567890",
  "full_name": "John Doe",
  "picture_url": "https://lh3.googleusercontent.com/...",
  "access_token": "base64_encrypted_token",
  "refresh_token": "base64_encrypted_token",
  "token_expiry": ISODate("2026-03-22T10:35:00Z"),
  "created_at": ISODate("2026-03-21T10:30:00Z"),
  "updated_at": ISODate("2026-03-21T10:35:00Z"),
  "last_login": ISODate("2026-03-21T10:35:00Z"),
  "is_active": true,
  "login_count": 5,
  "providers": [
    {
      "provider": "google",
      "provider_id": "1234567890"
    }
  ],
  "metadata": {}
}
```

---

## 🧪 Testing the Integration

### 1. Start the FastAPI server
```bash
fastapi dev main.py
```

### 2. Test endpoints in order

**A. Get Login URL**
```bash
curl http://localhost:8000/auth/google
```

**B. Visit the returned auth_url in browser** (manual step)
- User logs in with Google
- User grants permissions
- Redirected to callback

**C. Get User Profile** (after successful login)
```bash
curl "http://localhost:8000/auth/profile?auth_token=eyJhbGciOiJIUzI1NiIs..."
```

**D. Logout**
```bash
curl -X POST http://localhost:8000/auth/google/logout
```

---

## 📦 Required Python Packages

Add to `requirements.txt`:
```
fastapi
requests
pyjwt
pymongo
bcrypt
python-dotenv
pydantic
```

Install:
```bash
pip install -r requirements.txt
```

---

## ⚠️ Security Best Practices - Production Checklist

- [ ] Use HTTPS in production (set `secure=True` for cookies)
- [ ] Store `jwtSecretKey` in secure environment variables (NOT in .env on production)
- [ ] Implement proper token encryption (not just base64)
- [ ] Use cryptography library for AES encryption: `pip install cryptography`
- [ ] Implement rate limiting on auth endpoints
- [ ] Log all authentication attempts
- [ ] Implement account lockout after failed attempts
- [ ] Use MongoDB encryption at rest
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Implement API key validation
- [ ] Add CORS properly (whitelist domains)
- [ ] Monitor for suspicious login patterns

---

## 🔧 Upgrade Token Encryption (Production)

Replace token encryption in `googleAuth.py`:

```python
from cryptography.fernet import Fernet

class GoogleAuth:
    def __init__(self, ...):
        # Generate or load encryption key
        self.cipher_key = os.getenv("ENCRYPTION_KEY")
        self.cipher_suite = Fernet(self.cipher_key)
    
    def _encrypt_token(self, token: str) -> str:
        return self.cipher_suite.encrypt(token.encode()).decode()
    
    def _decrypt_token(self, encrypted_token: str) -> str:
        return self.cipher_suite.decrypt(encrypted_token.encode()).decode()
```

Generate encryption key:
```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())  # Add to .env as ENCRYPTION_KEY
```

---

## 🐛 Troubleshooting

### "Invalid client id"
- Verify Client ID in .env matches Google Console
- Check for extra spaces in .env

### "Redirect URI mismatch"
- Ensure callback URI in .env matches Google Console exactly
- include http/https scheme
- Match case and slashes precisely

### "PKCE code_verifier missing"
- Ensure cookies are being sent with requests
- Check browser allows third-party cookies
- Verify httpOnly cookie setting

### Token validation fails
- Check `jwtSecretKey` is consistent
- Verify token hasn't expired
- Ensure JWT parsing library installed

### MongoDB connection error
- Check connection string in .env
- Verify database credentials
- Ensure MongoDB Atlas IP whitelist includes your IP

---

## 📚 References

- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [PKCE RFC 7636](https://tools.ietf.org/html/rfc7636)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
