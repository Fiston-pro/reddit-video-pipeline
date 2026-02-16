# Phase 2: Web Dashboard + Vercel Deployment

## What We're Building

A **Streamlit web dashboard** hosted on **Vercel** so you can:
- Preview generated videos from anywhere
- Approve/reject videos with one click
- See story details and metrics
- Track what's been posted

## Why Vercel?

- ✅ **Free hosting** for personal projects
- ✅ **Easy deployment** (one command)
- ✅ **Always accessible** (no need to run locally)
- ✅ **Auto HTTPS** and custom domains

## Architecture

```
┌─────────────────────────────────────────────┐
│         Vercel (Cloud)                      │
│  ┌───────────────────────────────────────┐  │
│  │   Streamlit Dashboard                 │  │
│  │   - Video preview                     │  │
│  │   - Approve/Reject buttons            │  │
│  │   - Story list                        │  │
│  └───────────────────────────────────────┘  │
│               ↓↑                            │
│         Supabase API                        │
└─────────────────────────────────────────────┘
              ↓↑
┌─────────────────────────────────────────────┐
│      Your Local Machine                     │
│  ┌───────────────────────────────────────┐  │
│  │   Video Generation Pipeline           │  │
│  │   - Reddit scraper                    │  │
│  │   - Script generator                  │  │
│  │   - Video renderer                    │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

## Files to Create

1. **`streamlit_app.py`** - Main dashboard (Vercel entry point)
2. **`requirements-streamlit.txt`** - Streamlit-only dependencies
3. **`vercel.json`** - Vercel configuration
4. **`.vercelignore`** - Files to exclude from deployment

## Features

### Page 1: Video Queue
- List all videos pending approval
- Show thumbnail/preview
- Display story title + virality score
- Approve/Reject buttons
- Bulk actions

### Page 2: Approved Videos
- Ready to upload
- Schedule upload time
- Select platforms (YouTube, Instagram, TikTok)

### Page 3: Analytics
- Videos posted
- Performance metrics
- Best performing stories
- Platform comparison

### Page 4: Settings
- Configure subreddit
- Video settings (voice, fonts)
- Platform credentials
- Schedule preferences

## Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Supabase (already set up!)
- **Storage**: Google Drive links (videos accessible via URL)
- **Hosting**: Vercel (serverless deployment)
- **Auth**: Simple password protection initially

## Deployment Steps

1. **Install Streamlit**: `pip install streamlit`
2. **Create dashboard app**: `streamlit_app.py`
3. **Test locally**: `streamlit run streamlit_app.py`
4. **Setup Vercel**:
   ```bash
   npm install -g vercel
   vercel login
   vercel
   ```
5. **Deploy**: Push to GitHub, connect to Vercel
6. **Access**: `https://your-app.vercel.app`

## Security

- **Environment variables** for Supabase keys (stored in Vercel)
- **Password protection** for dashboard access
- **Read-only** Supabase access for dashboard
- **Separate** write access for local pipeline

## Cost

- **Vercel**: FREE (Hobby plan - perfect for this)
- **Supabase**: FREE (already using)
- **Total**: $0/month 🎉

## Timeline

- **Day 1**: Create Streamlit dashboard locally
- **Day 2**: Add video preview + approval flow
- **Day 3**: Setup Vercel deployment
- **Day 4**: Test and refine
- **Day 5**: Add analytics and settings

## Alternatives Considered

| Option | Pros | Cons | Chosen? |
|--------|------|------|---------|
| **Vercel + Streamlit** | Easy, free, Python | Limited compute | ✅ YES |
| Railway | Good for Python | Paid after trial | ❌ |
| Render | Free tier | Slow cold starts | ❌ |
| Heroku | Well-known | No longer free | ❌ |
| Self-hosted | Full control | Need always-on server | ❌ |

## Implementation Plan

### Step 1: Create Streamlit Dashboard
```python
# streamlit_app.py
import streamlit as st
from supabase import create_client

st.title("🎬 Video Approval Dashboard")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Get pending videos
videos = supabase.table('videos').select('*').eq('status', 'pending_approval').execute()

for video in videos.data:
    st.video(video['video_url'])  # From Google Drive

    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"Approve {video['id']}"):
            # Update status
            pass
    with col2:
        if st.button(f"Reject {video['id']}"):
            # Update status
            pass
```

### Step 2: Deploy to Vercel
```json
// vercel.json
{
  "builds": [
    {
      "src": "streamlit_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "streamlit_app.py"
    }
  ]
}
```

### Step 3: Add to GitHub
```bash
git init
git add .
git commit -m "Add Streamlit dashboard"
git push origin main
```

### Step 4: Connect Vercel
1. Go to vercel.com
2. Import GitHub repo
3. Add environment variables (SUPABASE_URL, SUPABASE_KEY)
4. Deploy!

## Video Storage Strategy

Since Vercel is serverless (no persistent storage), videos must be stored externally:

1. **Option A: Google Drive** (Current)
   - ✅ Free 15GB
   - ✅ Shareable links work in Streamlit
   - ✅ Already implemented

2. **Option B: Supabase Storage**
   - ✅ 1GB free
   - ✅ Integrated with database
   - ❌ Need to migrate

3. **Option C: Cloudinary**
   - ✅ 25GB free
   - ✅ Video player built-in
   - ❌ Extra setup

**Decision: Stick with Google Drive** (easiest, already working)

## Next Actions

1. Check if Part 1 video generated successfully
2. Create `streamlit_app.py` with basic video approval
3. Test locally with `streamlit run streamlit_app.py`
4. Deploy to Vercel
5. Access from anywhere!

---

**Estimated Time**: 2-3 hours to get basic dashboard deployed on Vercel

**Complexity**: Low (Streamlit is very easy!)

Ready to build it? 🚀
