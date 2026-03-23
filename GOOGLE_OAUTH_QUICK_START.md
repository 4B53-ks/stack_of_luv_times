# 🔗 Google OAuth URIs - Copy/Paste Ready

## ✅ Add These to Google Cloud Console

### Step 1: Authorized Redirect URIs
Copy and add ALL of these under:
**APIs & Services → Credentials → OAuth 2.0 Client ID (Web application)**

```
http://127.0.0.1:8000/auth/google/callback
http://localhost:8000/auth/google/callback
https://yourdomain.com/auth/google/callback
```

### Step 2: Authorized JavaScript Origins
Copy and add ALL of these (for CORS):

```
http://localhost:3000
http://127.0.0.1:3000
http://localhost:8000
http://127.0.0.1:8000
https://yourdomain.com
```

---

## 📝 Add These to Your `.env` File

```env
# Get these from Google Cloud Console
googleClientID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
googleClientSecret=YOUR_CLIENT_SECRET_HERE
googleRedirectURI=http://127.0.0.1:8000/auth/google/callback

# Generate a secure random key (min 32 characters)
jwtSecretKey=your_very_secure_random_secret_key_minimum_32_characters_long
```

---

## 🚀 API Callback Flow

When user clicks "Login with Google":

1. **Frontend** → GET `/auth/google`
   - Returns `auth_url` 
   - Redirect user there

2. **User** → Logs in at Google (manual step)
   - User grants permissions
   - Google auto-redirects to:
   ```
   http://127.0.0.1:8000/auth/google/callback?code=XXXX&state=YYYY
   ```

3. **Backend** → Automatically handles callback
   - Exchanges code for token
   - Fetches user info
   - Stores user in MongoDB
   - Returns JWT token + user data

4. **Frontend** → Receives JWT token
   - Store in httpOnly cookie (automatic)
   - Use for authenticated requests

---

## 📊 Quick Implementation Checklist

- [ ] Add Client ID & Secret to Google Cloud Console
- [ ] Copy redirect URIs from above to Google Console  
- [ ] Copy URIs to `.env` file
- [ ] Update `requirements.txt`: `pip install -r requirements.txt`
- [ ] Test with: `fastapi dev main.py`
- [ ] Visit `http://localhost:8000/auth/google` in browser
- [ ] Click returned auth_url
- [ ] Login with Google account
- [ ] Backend automatically processes callback
- [ ] User created in MongoDB ✅

---

## 🔐 Environment Variable Generator

Generate secure JWT secret:

```python
import secrets
secret = secrets.token_urlsafe(32)
print(secret)
# Add the output to .env as jwtSecretKey=...
```

Or in terminal:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📱 Frontend Integration Example (JavaScript/React)

```javascript
// Get login URL
const response = await fetch('http://localhost:8000/auth/google');
const { auth_url } = await response.json();

// Redirect user to Google
window.location.href = auth_url;

// After callback (backend auto-handles):
// User gets JWT in httpOnly cookie
// Can fetch /auth/profile to get user data

const profileResponse = await fetch('http://localhost:8000/auth/profile');
const userProfile = await profileResponse.json();
console.log(userProfile);
```

---

## 🔄 Complete OAuth Flow Diagram

```
┌─────────────┐
│   Frontend  │ → GET /auth/google → Returns auth_url
└─────────────┘                          ↓
                                   Redirect to Google
                                         ↓
┌─────────────┐                   ┌──────────────┐
│   Google    │ ← User logs in ─→ │ Grant Perms  │
└─────────────┘                   └──────────────┘
       ↓
   Redirects to callback with code
       ↓
┌─────────────────────────────────────────────────────┐
│ GET /auth/google/callback?code=XXX&state=YYY        │
│ ↓                                                   │
│ 1. Verify state (CSRF protection)                   │
│ 2. Exchange code for token (PKCE)                   │
│ 3. Fetch user info from Google                      │
│ 4. Create/update user in MongoDB                    │
│ 5. Generate JWT token                               │
│ 6. Set secure httpOnly cookie                       │
│ 7. Return user data + JWT                           │
└─────────────────────────────────────────────────────┘
       ↓
  Frontend receives JWT
  Auto-stored in httpOnly cookie
       ↓
  Can now access protected endpoints
  Cookie auto-sent with requests ✅
```

---

## ⚠️ Production Changes Required

When deploying to production:

1. **Update callback URI:**
   ```
   https://yourdomain.com/auth/google/callback
   ```

2. **Add to .env (production):**
   ```env
   googleRedirectURI=https://yourdomain.com/auth/google/callback
   ```

3. **Enable HTTPS** (required for `secure=True` cookies)

4. **Upgrade token encryption:**
   ```python
   # See GOOGLE_OAUTH_SETUP.md for cryptography setup
   ```

5. **Store secrets securely:**
   - Use environment-specific secrets manager
   - NOT in version control
   - Rotate jwtSecretKey periodically

---

## 🆘 Common Issues

| Problem | Solution |
|---------|----------|
| "Invalid client id" | Check Client ID in .env matches Google Console exactly |
| "Redirect URI mismatch" | Verify redirect URI in .env matches Google Console (https/http, path) |
| "CORS error" | Add JavaScript origins to Google Console (step 2 above) |
| "Token verification failed" | Ensure jwtSecretKey is consistent in .env |
| "User not created" | Check MongoDB connection in db/connection.py |

---

## 📞 Support References

- **Google OAuth Docs**: https://developers.google.com/identity/protocols/oauth2
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **MongoDB Docs**: https://docs.mongodb.com/
- **JWT Docs**: https://pyjwt.readthedocs.io/
