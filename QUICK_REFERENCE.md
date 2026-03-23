# 🎯 QUICK REFERENCE CARD - Copy & Paste Ready

## ✂️ Copy These Exact URIs to Google Console

### Authorized Redirect URIs (3 total)
```
http://127.0.0.1:8000/auth/google/callback
http://localhost:8000/auth/google/callback
https://yourdomain.com/auth/google/callback
```

### Authorized JavaScript Origins (5 total)
```
http://localhost:3000
http://127.0.0.1:3000
http://localhost:8000
http://127.0.0.1:8000
https://yourdomain.com
```

---

## ✂️ Copy to `.env` File

```env
googleClientID=YOUR_CLIENT_ID.apps.googleusercontent.com
googleClientSecret=YOUR_CLIENT_SECRET
googleRedirectURI=http://127.0.0.1:8000/auth/google/callback
jwtSecretKey=GENERATE_AND_PASTE_HERE
```

---

## 🎯 All API Endpoints

### Google OAuth
```
GET  /auth/google                                    [Start login]
GET  /auth/google/callback?code=X&state=Y           [Auto-handled by server]
GET  /auth/profile?auth_token=JWT                   [Get user profile]
POST /auth/google/logout                            [Logout]
GET  /auth/google/refresh?refresh_token=TOKEN       [Refresh token]
```

### Discord OAuth (Still Available)
```
GET  /auth/discord                                  [Start login]
GET  /auth/discordToken?code=X                      [Exchange for token]
GET  /auth/redirect_auth                            [Callback handler]
```

---

## 🗂️ Files Created

**New files:**
- `auth/googleAuth.py` — Complete OAuth implementation
- `basic_data/userModel.py` — User database models  
- `SETUP_INSTRUCTIONS.md` — Step-by-step setup guide
- `AUTH_IMPLEMENTATION_SUMMARY.md` — Full technical overview
- `GOOGLE_OAUTH_SETUP.md` — Security & best practices
- `GOOGLE_OAUTH_QUICK_START.md` — Quick reference

**Modified files:**
- `auth/authAPI.py` — Added Google OAuth endpoints
- `requirements.txt` — Added dependencies

---

## 📦 New Dependencies

Automatically handled by:
```bash
pip install -r requirements.txt
```

Includes:
- `pymongo` — MongoDB driver
- `pyjwt` — JWT token handling
- `bcrypt` — Password hashing
- `pydantic` — Data validation
- `cryptography` — Token encryption

---

## 🔐 Security Features

✅ PKCE (Proof Key for Code Exchange)
✅ State token CSRF protection
✅ HTTPOnly cookie XSS protection
✅ Token encryption in database
✅ JWT session management
✅ Secure token expiration
✅ HTTPS enforcement (production)
✅ SameSite cookie policy
✅ MongoDB index optimization
✅ Multiple provider support

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get credentials from Google Cloud Console

# 3. Update .env with credentials

# 4. Run server
fastapi dev main.py

# 5. Test
curl http://localhost:8000/auth/google
```

---

## 📊 Database Structure

Users stored in MongoDB collection `users`:

```json
{
  "_id": "mongo_object_id",
  "user_id": "user_abc123",
  "email": "user@google.com",
  "full_name": "John Doe",
  "picture_url": "https://...",
  "provider": "google",
  "provider_id": "google_user_id",
  "access_token": "encrypted_token",
  "refresh_token": "encrypted_token",
  "token_expiry": "2026-03-22T10:00:00Z",
  "created_at": "2026-03-21T10:00:00Z",
  "last_login": "2026-03-21T15:30:00Z",
  "login_count": 5,
  "is_active": true,
  "providers": [{"provider": "google", "provider_id": "..."}],
  "metadata": {}
}
```

---

## 🧪 Test Tokens

### Get Login URL
```bash
curl http://localhost:8000/auth/google
```

**Returns:**
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...",
  "state": "random_state_token"
}
```

### Get User Profile (After Login)
```bash
curl "http://localhost:8000/auth/profile?auth_token=YOUR_JWT_TOKEN"
```

**Returns:**
```json
{
  "user_id": "user_abc123",
  "email": "user@gmail.com",
  "full_name": "Your Name",
  "picture_url": "https://lh3.googleusercontent.com/...",
  "provider": "google",
  "created_at": "2026-03-21T...",
  "last_login": "2026-03-21T...",
  "login_count": 1
}
```

### Logout
```bash
curl -X POST http://localhost:8000/auth/google/logout
```

---

## 🎯 Why Each Security Feature?

| Feature | Attack Prevented |
|---------|-----------------|
| PKCE | Authorization code interception |
| State Token | CSRF (Cross-Site Request Forgery) |
| HTTPOnly | XSS (Cross-Site Scripting) |
| Token Encryption | Database breach exposure |
| JWT Signature | Token tampering |
| HTTPS | Man-in-the-middle attacks |
| SameSite | Cross-site cookie theft |
| Token Expiry | Stolen token misuse window |

---

## 📱 Frontend Integration

```javascript
// 1. Get login URL
const response = await fetch('http://localhost:8000/auth/google');
const { auth_url } = await response.json();

// 2. Redirect user
window.location.href = auth_url;

// 3. After callback (backend handles this)
//    JWT auto-stored in httpOnly cookie

// 4. Access protected route
const profile = await fetch('http://localhost:8000/auth/profile');
const user = await profile.json();
// User now logged in! ✅
```

---

## ⚠️ Common Mistakes

❌ Forgetting to enable Google+ API
❌ Wrong redirect URI (different http/https or path)
❌ Missing JavaScript origins (CORS)
❌ Not updating .env file
❌ Using hardcoded secrets in code

---

## ✅ Pre-Launch Checklist

- [ ] Google+ API enabled
- [ ] Redirect URIs added to Google Console
- [ ] JavaScript origins added to Google Console
- [ ] Credentials copied to .env
- [ ] jwtSecretKey generated and added
- [ ] `pip install -r requirements.txt` completed
- [ ] MongoDB connection verified
- [ ] `fastapi dev main.py` starts without errors
- [ ] `/auth/google` endpoint returns valid auth_url
- [ ] User can login and get JWT token

---

## 🆘 Troubleshooting

**Error: "sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL"**
→ Not relevant, we use MongoDB

**Error: "Redirect mismatch"**
→ Copy exact URI from above to Google Console

**Error: "CORS error"**
→ Add JavaScript origins from above

**Error: "Invalid JWT"**
→ Verify jwtSecretKey in .env

**Error: "mongodb connection failed"**
→ Check DB credentials in .env

---

## 📚 Documentation Files

For more details, see:

| File | Content |
|------|---------|
| `SETUP_INSTRUCTIONS.md` | Step-by-step Google Console setup |
| `AUTH_IMPLEMENTATION_SUMMARY.md` | Complete technical documentation |
| `GOOGLE_OAUTH_SETUP.md` | In-depth security guide |
| `GOOGLE_OAUTH_QUICK_START.md` | Quick reference with examples |

---

## 🎉 You Have Everything!

All Google OAuth functionality is implemented and ready to use.

Just:
1. Get Google credentials
2. Add to .env
3. Install dependencies
4. Test it!

For questions, check the documentation files above.
