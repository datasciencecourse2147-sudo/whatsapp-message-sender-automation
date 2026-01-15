# WhatsApp Message Sender - Render Deployment Guide

This guide will help you deploy your WhatsApp Message Sender application to Render.

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com)
3. Your project code pushed to a GitHub repository

## Step-by-Step Deployment Instructions

### Step 1: Prepare Your Repository

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - WhatsApp Message Sender"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

### Step 2: Create a New Web Service on Render

1. **Log in to Render:**
   - Go to https://dashboard.render.com
   - Sign in with your GitHub account

2. **Create a New Web Service:**
   - Click on "New +" button in the top right
   - Select "Web Service"
   - Connect your GitHub account if not already connected
   - Select the repository containing your WhatsApp Message Sender project

### Step 3: Configure the Web Service

Fill in the following configuration:

**Basic Settings:**
- **Name:** `whatsapp-message-sender` (or any name you prefer)
- **Region:** Choose the closest region to you
- **Branch:** `main` (or your default branch)
- **Root Directory:** Leave empty (or `.` if your files are in a subdirectory)

**Build & Deploy:**
- **Environment:** `Docker` (Recommended) or `Python 3`
- If using Docker: No build/start commands needed (uses Dockerfile)
- If using Python 3:
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT send_msg:app`

**Advanced Settings:**
- Click "Advanced" to add environment variables:
  - **Key:** `HEADLESS`
  - **Value:** `true`
  - **Key:** `PYTHON_VERSION`
  - **Value:** `3.11.0`

### Step 4: Choose Deployment Method

You have two options for deployment:

**Option 1: Using Docker (Highly Recommended)**
- The project includes a `Dockerfile` that handles Chrome installation automatically
- In Render, select **Environment: Docker**
- Render will automatically detect and use the Dockerfile
- No additional build/start commands needed
- Chrome and all dependencies are pre-installed

**Option 2: Using Python Build (Limited)**
- Select **Environment: Python 3**
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT send_msg:app`
- **⚠️ Important:** Chrome may not be available in Python environment. You may need to:
  - Use a Chrome headless service (external)
  - Or switch to Docker deployment
  - Or use Selenium Grid/Cloud services

### Step 5: Deploy

1. Click "Create Web Service"
2. Render will start building your application
3. Monitor the build logs - the first build may take 5-10 minutes
4. Once deployed, you'll get a URL like: `https://whatsapp-message-sender.onrender.com`

### Step 6: Access Your Application

1. Open the provided URL in your browser
2. You should see the WhatsApp Message Sender interface

## Important Notes

### ⚠️ Limitations on Render

1. **QR Code Scanning:** 
   - WhatsApp Web requires QR code scanning for authentication
   - In headless mode, you cannot scan QR codes directly
   - **Solution:** You may need to:
     - Use a service that supports VNC/remote desktop for initial setup
     - Or use WhatsApp Business API (paid service)
     - Or run the app locally for QR code scanning, then export the session

2. **Session Persistence:**
   - The `whatsapp_session` folder may be reset on each deployment
   - Consider using persistent storage or external session management

3. **Free Tier Limitations:**
   - Render free tier services spin down after 15 minutes of inactivity
   - First request after spin-down may take 30-60 seconds
   - Consider upgrading to a paid plan for always-on service

### 🔧 Troubleshooting

**Build Fails:**
- Check build logs for errors
- Ensure all dependencies are in `requirements.txt`
- Verify Chrome installation commands

**App Crashes:**
- Check runtime logs in Render dashboard
- Ensure `PORT` environment variable is being used
- Verify Chrome/ChromeDriver compatibility

**WhatsApp Not Working:**
- Headless mode may have limitations with WhatsApp Web
- Check if WhatsApp Web blocks headless browsers
- Consider using WhatsApp Business API instead

### 📝 Environment Variables

You can add these in Render Dashboard → Environment:
- `HEADLESS=true` - Enable headless mode
- `FLASK_ENV=production` - Production mode
- `PORT` - Automatically set by Render (don't change)

### 🔄 Updating Your App

1. Push changes to your GitHub repository
2. Render will automatically detect and redeploy
3. Or manually trigger a deploy from Render dashboard

## Alternative: Using Docker (Advanced)

If you prefer Docker, you can create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

CMD gunicorn --bind 0.0.0.0:$PORT send_msg:app
```

## Support

If you encounter issues:
1. Check Render's documentation: https://render.com/docs
2. Review build and runtime logs in Render dashboard
3. Ensure all file paths and configurations are correct

---

**Good luck with your deployment! 🚀**
