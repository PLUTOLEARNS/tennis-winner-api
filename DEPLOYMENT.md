# 🚀 Deployment Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository (e.g., `wimbledon-api`)
5. Make it public (required for free hosting)
6. Don't initialize with README (we already have one)
7. Click "Create repository"

## Step 2: Upload Your Code to GitHub

Open PowerShell in your project directory and run:

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Wimbledon Finals API"

# Add your GitHub repository as remote (replace USERNAME and REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render.com (Recommended - 100% Free)

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account (no credit card required)
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: `wimbledon-api`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Instance Type**: Free
6. Click "Create Web Service"
7. Wait for deployment (takes 2-5 minutes)
8. Your API will be live at: `https://your-app-name.onrender.com`

## Step 4: Alternative - Deploy on Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign up with your GitHub account
3. Click "New Project"
4. Import your GitHub repository
5. Vercel will automatically detect it's a Python project
6. Click "Deploy"
7. Your API will be live at: `https://your-app-name.vercel.app`

## Step 5: Test Your Deployed API

Replace `YOUR_API_URL` with your actual deployed URL:

```bash
# Test health endpoint
curl https://YOUR_API_URL/health

# Test Wimbledon endpoint
curl "https://YOUR_API_URL/wimbledon?year=2021"
```

## Step 6: Update README with Live URL

Once deployed, update the README.md file with your live API URL.

## Free Hosting Limits

### Render.com (Recommended)
- ✅ Completely free
- ✅ No credit card required
- ✅ Custom domains
- ✅ HTTPS included
- ⚠️ Sleeps after 15 minutes of inactivity
- ⚠️ 750 hours/month limit

### Vercel
- ✅ Completely free
- ✅ No credit card required
- ✅ Excellent performance
- ✅ No sleep mode
- ⚠️ 100GB bandwidth/month
- ⚠️ Serverless functions (good for APIs)

## Troubleshooting

**If deployment fails:**
1. Check the build logs in your hosting platform
2. Ensure all dependencies are in `requirements.txt`
3. Check that your Python version is compatible
4. Verify the start command is correct

**If API returns errors:**
1. Check the application logs
2. Verify the CSV data is being generated correctly
3. Test locally first with `python app.py`

## Monitoring

- **Render**: Check logs in the Render dashboard
- **Vercel**: Check function logs in the Vercel dashboard
- **Health Check**: Use `/health` endpoint to monitor API status

## Custom Domain (Optional)

Both Render and Vercel support custom domains on their free tiers. You can add your own domain in the platform settings.
