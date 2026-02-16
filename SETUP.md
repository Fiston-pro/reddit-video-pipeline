# Setup Guide

Follow these steps to get your automated content pipeline running.

## Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux

# Install Python packages
pip install -r requirements.txt
```

## Step 2: Install FFmpeg

FFmpeg is required for video processing.

**Windows**:
1. Download from https://ffmpeg.org/download.html (Windows builds)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to System PATH
4. Test: `ffmpeg -version` in command prompt

**Mac**:
```bash
brew install ffmpeg
```

**Linux**:
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
```

## Step 3: Setup Supabase

1. **Create Supabase project**:
   - Go to https://supabase.com
   - Sign in / Create account (free)
   - Click "New Project"
   - Enter project name: `reddit-video-pipeline`
   - Choose a database password
   - Select region closest to you
   - Click "Create new project" (wait 2-3 minutes)

2. **Run database setup**:
   - In Supabase dashboard, go to **SQL Editor**
   - Click "New query"
   - Copy contents of `scripts/setup_supabase.sql`
   - Paste into query editor
   - Click "Run" button
   - You should see: "Database setup complete!"

3. **Get API credentials**:
   - In Supabase dashboard, go to **Settings** → **API**
   - Copy **Project URL** (looks like: https://xxx.supabase.co)
   - Copy **anon public** key (long string starting with "eyJ...")

## Step 4: Setup Reddit API

1. **Create Reddit app**:
   - Go to https://www.reddit.com/prefs/apps
   - Scroll to bottom, click "create another app..."
   - Fill in:
     - Name: `reddit-video-bot`
     - Type: Select "script"
     - Description: `Automated content creation bot`
     - About URL: (leave blank)
     - Redirect URI: `http://localhost:8080`
   - Click "create app"

2. **Get credentials**:
   - **Client ID**: Under app name (looks like: `abc123XYZ`)
   - **Client Secret**: Next to "secret" (click to reveal)

## Step 5: Configure Environment Variables

1. **Create .env file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file** with your credentials:
   ```bash
   # Reddit API
   REDDIT_CLIENT_ID=your_client_id_from_step4
   REDDIT_CLIENT_SECRET=your_client_secret_from_step4
   REDDIT_USER_AGENT=content-bot/1.0

   # Supabase
   SUPABASE_URL=your_project_url_from_step3
   SUPABASE_KEY=your_anon_key_from_step3

   # Leave others blank for now (needed in later phases)
   GOOGLE_CLIENT_ID=
   GOOGLE_CLIENT_SECRET=
   FB_ACCESS_TOKEN=
   IG_USER_ID=
   TIKTOK_ACCESS_TOKEN=
   DISCORD_WEBHOOK_URL=
   ```

## Step 6: Test Connection

```bash
# Test Supabase connection
python src/database/supabase_client.py
# Should see: ✅ Connection successful!

# Test Reddit connection (we'll create this file next)
python src/scrapers/reddit_scraper.py --test
```

## Step 7: Download Background Videos

Create the backgrounds folder and download some videos:

```bash
mkdir -p assets/backgrounds
```

**Manual download** (for now):
1. Go to https://www.pexels.com/search/videos/minecraft%20parkour/
2. Download 1-2 videos (1080p or higher)
3. Save to `assets/backgrounds/minecraft_parkour_01.mp4`

Later we'll create a script to automate this.

## Step 8: Create Data Directories

```bash
mkdir -p data/videos
mkdir -p data/voiceovers
mkdir -p data/logs
mkdir -p data/stories
```

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip list` shows praw, supabase, etc.)
- [ ] FFmpeg installed (`ffmpeg -version` works)
- [ ] Supabase project created and tables setup
- [ ] Reddit app created and credentials obtained
- [ ] .env file created with valid credentials
- [ ] Supabase connection test passes
- [ ] At least 1 background video downloaded

## Next Steps

Once setup is complete, proceed to Phase 1 implementation:

1. Run Reddit scraper to fetch stories
2. Select top story
3. Generate your first video!

See README.md for usage instructions.

## Troubleshooting

**"Module not found" errors**:
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**"FFmpeg not found"**:
- Check FFmpeg is in PATH: `echo %PATH%` (Windows) or `echo $PATH` (Mac/Linux)
- Restart terminal after adding to PATH

**Supabase connection fails**:
- Check SUPABASE_URL and SUPABASE_KEY in .env
- Make sure URL includes https://
- Verify anon key is correct (starts with "eyJ")

**Reddit API errors**:
- Verify REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET
- Check that app type is "script" not "web app"
- Try different user agent string
