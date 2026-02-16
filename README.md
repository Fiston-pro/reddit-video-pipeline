# Automated Reddit-to-Social-Media Video Pipeline

Fully automated content creation system that scrapes viral Reddit stories, generates TikTok-style videos, and publishes to multiple social media platforms.

## Features

- ✅ Daily Reddit scraping from r/cheating_stories
- ✅ AI-powered viral prediction and story selection
- ✅ Automated video generation (TTS voiceover + background + subtitles)
- ✅ Web dashboard for manual video approval
- ✅ Multi-platform upload (YouTube Shorts, Instagram Reels, TikTok)
- ✅ Performance tracking across all platforms
- ✅ 100% free using open-source tools and free cloud tiers

## Tech Stack

- **Reddit**: PRAW (Python Reddit API Wrapper)
- **Database**: Supabase PostgreSQL (free tier)
- **TTS**: edge-tts (Microsoft, free unlimited)
- **Video**: MoviePy + FFmpeg
- **Dashboard**: Streamlit
- **Storage**: Google Drive API (15GB free)

## Quick Start

### Prerequisites

1. **Python 3.8+**
2. **FFmpeg** - Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
3. **Reddit Account** - Create app at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
4. **Supabase Account** - Sign up at [supabase.com](https://supabase.com)

### Installation

1. **Clone and setup**:
   ```bash
   cd c:\Users\HP\Desktop\CODE\Agents
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

2. **Setup Supabase**:
   - Create project at supabase.com
   - Run SQL from `scripts/setup_supabase.sql` in SQL Editor
   - Copy URL and anon key

3. **Configure credentials**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Download background videos**:
   ```bash
   python scripts/download_backgrounds.py
   ```

### Usage

**Phase 1 - Generate first video**:
```bash
# 1. Scrape Reddit stories
python src/scrapers/reddit_scraper.py

# 2. Select top story
python src/processors/story_selector.py

# 3. Generate video
python src/generators/video_generator.py

# 4. Review and approve (CLI)
python src/jobs/scrape_and_generate.py
```

**Phase 2 - Web dashboard**:
```bash
streamlit run src/dashboard/approval_app.py
```

**Phase 5 - Full automation**:
```bash
# Runs continuously with scheduled tasks
python src/main.py
```

## Project Structure

```
Agents/
├── config/          # Configuration files
├── credentials/     # API credentials (git-ignored)
├── assets/         # Background videos
├── data/           # Generated content and logs
├── src/
│   ├── scrapers/   # Reddit scraping
│   ├── processors/ # Story selection
│   ├── generators/ # Video creation
│   ├── uploaders/  # Platform APIs
│   ├── trackers/   # Analytics
│   ├── dashboard/  # Approval UI
│   ├── database/   # Supabase client
│   └── utils/      # Shared utilities
├── scripts/        # Setup scripts
└── tests/          # Unit tests
```

## Configuration

Edit `config/config.yaml` to customize:
- Subreddit to scrape
- Video parameters (aspect ratio, fonts, etc.)
- Platform settings
- Scheduling intervals

## Roadmap

- [x] Phase 1: Core pipeline (scrape → generate)
- [ ] Phase 2: Subtitles + web dashboard
- [ ] Phase 3: Multi-platform upload
- [ ] Phase 4: Performance tracking
- [ ] Phase 5: Full automation

## Cost Breakdown

**Free Tier (Current)**:
- Supabase: 500MB database (FREE)
- Google Drive: 15GB storage (FREE)
- edge-tts: Unlimited (FREE)
- YouTube/Instagram/TikTok APIs: FREE

**Total**: $0/month

**Optional Upgrades**:
- ElevenLabs TTS: $5/mo (better voice quality)
- Supabase Pro: $25/mo (if >500MB needed)

## License

MIT

## Support

For issues or questions, create an issue on GitHub.
