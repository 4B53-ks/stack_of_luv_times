# 🎯 EXACTLY WHAT TO ADD IN GOOGLE CLOUD CONSOLE

## ⚠️ IMPORTANT: Do This First!

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select or create a project
3. Go to **APIs & Services → Library**
4. Search for: `Google+ API`
5. Click **ENABLE**
6. Go to **APIs & Services → Credentials**
7. Click **+ Create Credentials**
8. Select **OAuth client ID**
9. Choose **Web application**
10. Set name (e.g., "stack_of_luv_times")

---

## 📋 STEP 1: Copy & Paste - Authorized Redirect URIs

**Location in Google Console:**
```
OAuth 2.0 Client ID (Web application) 
→ Authorized redirect URIs
```

**Copy and paste ALL THREE of these into Google Console:**

```
http://127.0.0.1:8000/auth/google/callback
http://localhost:8000/auth/google/callback
https://yourdomain.com/auth/google/callback
```

⚠️ **Important:**
- Replace `yourdomain.com` with your actual domain ONLY for production
- For development, use first two only
- Copy EXACTLY as shown (matching http/https and path)

---

## 🌍 STEP 2: Copy & Paste - Authorized JavaScript Origins

**Location in Google Console:**
```
OAuth 2.0 Client ID (Web application) 
→ Authorized JavaScript origins
```

**Copy and paste ALL FIVE of these into Google Console:**

```
http://localhost:3000
http://127.0.0.1:3000
http://localhost:8000
http://127.0.0.1:8000
https://yourdomain.com
```

⚠️ **Important:**
- Add for both frontend (port 3000) and backend (port 8000)
- Replace `yourdomain.com` with your domain ONLY for production
- For development, use the localhost entries

---

## 🔑 STEP 3: Copy Your Credentials

After clicking **CREATE**, you'll see:

```
Client ID:     1234567890-abcdefghijk1234567890lmnop.apps.googleusercontent.com
Client Secret: GOCSPX-1234abcd5678efgh9IJKLmnop
```

Copy and save these! You'll need them next.

---

## 📝 STEP 4: Update Your `.env` File

**Open:** `d:\stack_of_luv_times\.env`

**Add or Update these lines:**

```env
# Google OAuth Credentials (from Google Cloud Console above)
googleClientID=PASTE_YOUR_CLIENT_ID_HERE
googleClientSecret=PASTE_YOUR_CLIENT_SECRET_HERE
googleRedirectURI=http://127.0.0.1:8000/auth/google/callback

# Generate a secure key - run this in terminal:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
# Then paste the output here:
jwtSecretKey=PASTE_GENERATED_KEY_HERE
```

**Example of filled .env:**
```env
# Google OAuth credentials
googleClientID=1234567890-abcdefghijk1234567890lmnop.apps.googleusercontent.com
googleClientSecret=GOCSPX-1234abcd5678efgh9IJKLmnop
googleRedirectURI=http://127.0.0.1:8000/auth/google/callback

# JWT Secret (example - generate your own!)
jwtSecretKey=h_O-gVqPdnL4kM9xQ5jT2wY6rP3aB8sZ1eC7fU9vW0
```

---

## 🔐 Generate Your JWT Secret Key

**Option 1: Using Python (Recommended)**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Copy the output and paste into `.env`

**Option 2: Using Node.js**
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

**Option 3: Online Generator**
Use https://randomkeygen.com/ (CodeIgniter key - 32+ chars)

---

## ✅ Verification Checklist

After updating Google Console and `.env`, verify:

```
☐ Authorized Redirect URIs added (all 3)
☐ Authorized JavaScript Origins added (all 5)  
☐ googleClientID copied to .env
☐ googleClientSecret copied to .env
☐ googleRedirectURI set correctly in .env
☐ jwtSecretKey generated and added to .env
☐ .env file saved
```

---

## 🚀 Next Command to Run

Once everything above is done:

```bash
pip install -r requirements.txt
```

This installs all dependencies needed for Google OAuth.

---

## 🧪 Test It Works

```bash
fastapi dev main.py
```

Then open in browser:
```
http://localhost:8000/auth/google
```

You should see JSON with an auth_url. Click that URL!

---

## 🔄 Callback URIs Explained

| URI | Purpose |
|-----|---------|
| `http://127.0.0.1:8000/auth/google/callback` | Development (localhost IP) |
| `http://localhost:8000/auth/google/callback` | Development (localhost name) |
| `https://yourdomain.com/auth/google/callback` | Production (your domain) |

**Why 3 URIs?**
Different browsers/tools might use IP vs name, and production needs HTTPS.

---

## 🆘 If You Get "Redirect URI Mismatch" Error

**This means:** The callback URI in Google Console doesn't exactly match what's in your `.env`

**Fix:**
1. Go back to Google Console
2. Check the redirect URI you added
3. Compare character-by-character with your `.env`
4. Ensure exact match: `http://127.0.0.1:8000/auth/google/callback`
5. Check for extra spaces, different casing, or missing slashes

---

## 🔒 Security Notes

1. **Don't commit `.env` to git** (already in .gitignore likely)
2. **jwtSecretKey** - Keep this secret, change it regularly in production
3. **googleClientSecret** - Never hardcode this, always use .env
4. **In production** - Use environment-specific secrets manager (AWS Secrets Manager, etc.)

---

## Callback Flow Diagram

```
┌──────────────────────────────────────────────────┐
│ User goes to: http://localhost:8000/auth/google  │
└────────────────────┬─────────────────────────────┘
                     ↓
        ┌────────────────────────┐
        │ Backend returns         │
        │ auth_url (Google link)  │
        └────────────┬────────────┘
                     ↓
        ┌────────────────────────┐
        │ Browser redirects to    │
        │ Google login page       │
        └────────────┬────────────┘
                     ↓
        ┌────────────────────────┐
        │ User logs in at Google  │
        │ Grants permissions      │
        └────────────┬────────────┘
                     ↓
        ┌────────────────────────────────────────┐
        │ Google redirects to:                    │
        │ http://127.0.0.1:8000/auth/google/     │
        │ callback?code=XXX&state=YYY            │
        └────────────┬─────────────────────────┘
                     ↓
        ┌────────────────────────┐
        │ Backend AUTOMATICALLY:  │
        │ 1. Exchanges code      │
        │ 2. Gets user info      │
        │ 3. Stores in MongoDB   │
        │ 4. Creates JWT token   │
        │ 5. Sets auth cookie    │
        └────────────┬────────────┘
                     ↓
        ┌────────────────────────┐
        │ Frontend receives JWT   │
        │ User is logged in! ✅   │
        └────────────────────────┘
```

---

## 📞 Still Having Issues?

1. **"Client ID or secret wrong"** → Recopy from Google Console, watch for spaces
2. **"Redirect URI invalid"** → Check exact match with Google Console
3. **"CORS error"** → Add JavaScript origins (Step 2 above)
4. **"Token verification error"** → Ensure jwtSecretKey is in .env and saved
5. **"MongoDB error"** → Check DB credentials

See `GOOGLE_OAUTH_SETUP.md` for detailed troubleshooting.

---

## All Ready! 🎉

Once you complete Steps 1-4 above, your Google OAuth is fully configured.

For any detailed questions, check:
- `AUTH_IMPLEMENTATION_SUMMARY.md` - Overview
- `GOOGLE_OAUTH_SETUP.md` - Complete security guide
- `GOOGLE_OAUTH_QUICK_START.md` - Quick reference
