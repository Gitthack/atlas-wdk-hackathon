# Railway Deployment Guide

## Quick Deploy

### Step 1: Connect Railway to GitHub
1. Go to https://railway.app/
2. Sign up/login (can use GitHub account)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose: `Gitthack/atlas-wdk-hackathon`

### Step 2: Deploy
Railway will automatically:
- Detect Python project
- Install dependencies from `requirements.txt`
- Use `Procfile` start command
- Assign a public URL

### Step 3: Get Your URL
After deployment:
1. Go to your project dashboard
2. Click on the service
3. Find the public URL (e.g., `https://atlas-wdk-hackathon-production.up.railway.app`)
4. Share this URL on your phone!

---

## Configuration Files

### Procfile
```
web: python3 dashboard.py
```
Tells Railway how to start the app.

### railway.json
```json
{
  "deploy": {
    "startCommand": "python3 dashboard.py"
  }
}
```
Explicit deployment configuration.

### dashboard.py (PORT handling)
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```
Uses Railway's assigned PORT.

---

## Troubleshooting

### Build Failed?
- Check `requirements.txt` has all dependencies
- Check Python version (3.10+)

### App Crashed?
- Check logs in Railway dashboard
- Make sure `Procfile` has correct command

### Can't Access?
- Check service is "Deployed" (green)
- Check public domain is generated

---

## Alternative: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

---

## After Deployment

Your app will be live at:
```
https://[your-project-name].up.railway.app
```

You can:
- View on phone anytime
- Share with judges
- Add custom domain (optional)

---

## Free Tier Limits

- 500 hours/month runtime
- $5 credit/month
- For hackathon demo: more than enough!

---

**Ready to deploy?** Go to https://railway.app/ and connect your GitHub repo!
