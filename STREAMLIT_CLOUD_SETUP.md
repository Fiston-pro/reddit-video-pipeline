# 🚀 Deploy to Streamlit Cloud - Step by Step

## ✅ Prerequisites
- GitHub account
- Your project code (already have it!)
- Supabase credentials (already set up!)

---

## 📋 Step-by-Step Guide (5 Minutes)

### Step 1: Push Code to GitHub

#### Option A: If you already have a GitHub repo
```bash
cd c:/Users/HP/Desktop/CODE/Agents

# Add all files
git add .
git commit -m "Add Streamlit dashboard with video approval"
git push
```

#### Option B: If you need to create a new GitHub repo
```bash
cd c:/Users/HP/Desktop/CODE/Agents

# Initialize git (if not already)
git init

# Add all files
git add .
git commit -m "Initial commit: Reddit video pipeline with Streamlit dashboard"

# Create repo on GitHub (go to github.com/new)
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/reddit-video-pipeline.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io
   - Click **"Sign in with GitHub"**

2. **Create New App:**
   - Click **"New app"** button
   - You'll see this form:

3. **Fill in Deployment Settings:**
   ```
   Repository: YOUR_USERNAME/reddit-video-pipeline
   Branch: main
   Main file path: streamlit_app.py
   App URL (optional): reddit-video-dashboard
   ```

4. **Advanced Settings:**
   - Click **"Advanced settings..."** at the bottom
   - Add these environment secrets:

   ```bash
   # Required
   SUPABASE_URL=https://yoxkfigtbhlpdohirrtt.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # Your actual key

   # Optional (default is admin123)
   DASHBOARD_PASSWORD=your_secure_password
   ```

5. **Deploy:**
   - Click **"Deploy!"**
   - Wait 2-3 minutes for first deployment
   - Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

---

## 🎯 What You'll Get

Once deployed, your dashboard will have:

### ✅ Full Features:
- **Video Player** - Watch videos inline
- **Approval Buttons** - Click to approve/reject
- **Analytics Dashboard** - See metrics and stats
- **Story Preview** - Read full stories
- **Real-time Updates** - Instant status changes

### 📱 Pages:
1. **Pending Approval** - Review new videos
2. **Approved Videos** - See what's ready to post
3. **Analytics** - View performance metrics
4. **Settings** - Configure dashboard

---

## 🔐 Security

Your dashboard will be password-protected:
- Default password: `admin123`
- Change it by setting `DASHBOARD_PASSWORD` in Streamlit Cloud settings

---

## 🔄 Auto-Deploy

Once connected to GitHub:
- ✅ Every `git push` automatically redeploys
- ✅ Changes go live in 2-3 minutes
- ✅ No manual deployment needed

---

## 📊 Resource Limits (FREE Tier)

Streamlit Cloud FREE tier includes:
- ✅ 1 GB RAM
- ✅ 1 CPU core
- ✅ Unlimited apps
- ✅ Always on (no cold starts)
- ✅ Automatic SSL certificate

**This is MORE than enough for your dashboard!**

---

## 🎨 Example URLs

After deployment, you'll have:
```
Main Dashboard:
https://reddit-video-dashboard.streamlit.app

Alternative names (if taken):
https://reddit-pipeline.streamlit.app
https://video-approval-dashboard.streamlit.app
```

---

## 🐛 Troubleshooting

### Issue: App won't start
**Solution:** Check that `requirements.txt` includes:
```
streamlit>=1.31.0
supabase>=2.3.0
pandas>=2.0.0
```

### Issue: Can't connect to Supabase
**Solution:** Verify environment variables are set correctly in Streamlit Cloud settings.

### Issue: Password not working
**Solution:** Check `DASHBOARD_PASSWORD` environment variable. Default is `admin123`.

---

## 🚀 I Can Help Deploy Right Now!

**Want me to:**
1. ✅ Check if your code is ready
2. ✅ Create the GitHub repo commands
3. ✅ Guide you through Streamlit Cloud setup

Just say "yes" and I'll walk you through each step!

---

## 📌 Quick Commands Reference

```bash
# Check git status
git status

# Add and commit changes
git add .
git commit -m "Update dashboard"

# Push to GitHub (triggers auto-deploy)
git push

# Check Streamlit logs (in browser)
# Go to: https://share.streamlit.io → Your App → Manage app → Logs
```

---

## ✅ Final Checklist

Before deploying, make sure you have:
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account (free)
- [ ] Supabase URL and API key ready
- [ ] Decided on a dashboard password

**Ready? Let's deploy!** 🚀
