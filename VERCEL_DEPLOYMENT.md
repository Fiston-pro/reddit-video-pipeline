# Deploying Dashboard to Vercel

## Quick Start

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy
```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? (select your account)
- Link to existing project? **N**
- Project name? **reddit-video-dashboard** (or your choice)
- Directory? **./** (current directory)
- Override settings? **N**

### 4. Set Environment Variables

After first deployment, add these environment variables in Vercel dashboard:

Go to: Project Settings → Environment Variables

Add:
- `SUPABASE_URL` = `https://yoxkfigtbhlpdohirrtt.supabase.co`
- `SUPABASE_KEY` = Your Supabase anon key (from .env)
- `DASHBOARD_PASSWORD` = Your chosen password (default: admin123)

### 5. Redeploy
```bash
vercel --prod
```

Your dashboard will be live at: `https://your-project.vercel.app`

---

## Alternative: GitHub Integration

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Add Streamlit dashboard"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### 2. Import to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Framework Preset: **Other**
5. Build Command: (leave empty)
6. Output Directory: (leave empty)
7. Install Command: `pip install -r requirements-streamlit.txt`
8. Add environment variables (SUPABASE_URL, SUPABASE_KEY, DASHBOARD_PASSWORD)
9. Deploy!

---

## Important Notes

### File Structure for Vercel
Vercel will deploy only:
- `streamlit_app.py` (main app)
- `src/database/` (Supabase client)
- `src/utils/` (utilities)
- `requirements-streamlit.txt` (dependencies)

Everything else is excluded via `.vercelignore` (videos, backgrounds, generators, etc.)

### Dashboard Features
- ✅ Password protection
- ✅ Video preview (from Google Drive links)
- ✅ Approve/Reject workflow
- ✅ Analytics dashboard
- ✅ Real-time sync with Supabase

### Limitations
- Vercel free tier: 100GB bandwidth/month
- Serverless function timeout: 10 seconds (edge), 60 seconds (serverless)
- No persistent storage (videos must be on Google Drive)

### Troubleshooting

**Error: "Module not found"**
- Check `requirements-streamlit.txt` has all dependencies
- Redeploy with `vercel --prod`

**Error: "Supabase connection failed"**
- Verify environment variables are set in Vercel dashboard
- Make sure you're using the **anon key**, not the publishable key

**Video preview not working**
- Google Drive links must be publicly shareable
- Check video URL format in database

---

## Local Testing

Before deploying to Vercel, test locally:

```bash
# Install dependencies
pip install -r requirements-streamlit.txt

# Run Streamlit
streamlit run streamlit_app.py
```

Open browser to `http://localhost:8501`

---

## Next Steps After Deployment

1. **Bookmark your dashboard URL**
2. **Test approval workflow** (approve a test video)
3. **Configure auto-upload** to run when videos are approved
4. **Set up monitoring** (Vercel Analytics, Supabase logs)

Your dashboard is now accessible from anywhere! 🚀
