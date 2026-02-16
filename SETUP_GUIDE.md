# Complete Setup Guide - Fix Dependencies & Get Everything Working

## Current Status

### ✅ What's Working:
- **AI Enhancement** - Tested and proven to work perfectly!
- **Random Backgrounds** - Code is ready
- **Vercel Dashboard** - Files ready to deploy
- **All improvements implemented**

### ⚠️ Issue:
- Python 3.13 dependency conflicts preventing video generation

---

## Solution: Virtual Environment Setup

### Step 1: Create Virtual Environment

```bash
# Open PowerShell/CMD in your project folder
cd "c:\Users\HP\Desktop\CODE\Agents"

# Create virtual environment
python -m venv venv
```

### Step 2: Activate Virtual Environment

```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# OR Windows CMD
venv\Scripts\activate.bat
```

You should see `(venv)` at the start of your command prompt.

### Step 3: Install All Dependencies

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# If imageio-ffmpeg fails, install newer version
pip install imageio-ffmpeg>=0.5.0
```

### Step 4: Test AI Enhancement

```bash
python test_ai_enhancement.py
```

You should see:
- Basic script
- AI-enhanced script (dramatic, viral-ready)
- Cost breakdown

### Step 5: Generate Video with All Improvements

```bash
# Set PYTHONPATH so imports work
$env:PYTHONPATH="."  # PowerShell
# OR
set PYTHONPATH=.     # CMD

# Generate Part 1 video
python src/generators/video_generator.py e6dd307b-caa4-4de7-bbb0-6fd650c2a32a
```

**What will happen:**
1. Loads story from database
2. Generates engaging script with script_generator
3. **AI enhances script** with Claude Haiku (viral hooks, pacing)
4. Generates TTS voiceover with gTTS
5. **Creates background with random switching** every 12 seconds
6. Composites final video
7. Saves to `data/videos/` folder

---

## Expected Output

```
Generating engaging script for story...
Story has 795 words
Split story into 3 parts
Generated basic script with 285 words
Enhancing script with AI for viral hooks and pacing...
AI-enhanced script with 240 words
Generating TTS voiceover from engaging script...
Voiceover duration: 134.8s
Creating background video with random segments...
Added minecraft_parkour_01.mp4 segment (12.0s), total: 12.0s
Added subway_surfer_01.mp4 segment (12.0s), total: 24.0s
Added satisfying_loops_01.mp4 segment (12.0s), total: 36.0s
...
Created background with 12 random segments
Compositing final video...
Rendering video...
Video generated successfully: video_xxx.mp4 (93.0MB)
```

---

## Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'xxx'`

**Solution**: Make sure virtual environment is activated and run:
```bash
pip install -r requirements.txt
```

### Problem: `pkg_resources` error

**Solution**: Update imageio-ffmpeg:
```bash
pip uninstall imageio-ffmpeg -y
pip install imageio-ffmpeg>=0.5.0
```

### Problem: Supabase connection error

**Solution**: Check your `.env` file has correct keys:
```bash
SUPABASE_URL=https://yoxkfigtbhlpdohirrtt.supabase.co
SUPABASE_KEY=eyJhbGci... (your anon key - 200+ characters)
ANTHROPIC_API_KEY=sk-ant-api03-... (your Claude API key)
```

### Problem: Video generation takes too long

**Normal!** A 2-minute video with AI enhancement takes 5-10 minutes:
- AI enhancement: 3-5 seconds
- TTS generation: 15-20 seconds
- Video composition: 30-60 seconds
- Video rendering: 5-8 minutes (depends on CPU)

---

## What Each Improvement Does

### 1. Random Background Switching

**Before**: Single background looped for entire video
```python
# Old code
video = self.loop_background_to_duration(background_path, duration)
```

**After**: Different backgrounds every 12 seconds
```python
# New code
video = self.create_random_background_video(duration, switch_interval=12.0)
```

**Result**:
- 0-12s: Minecraft parkour
- 12-24s: Subway Surfer
- 24-36s: Satisfying loops
- Randomly selected, more engaging!

### 2. AI-Enhanced Scripts

**Before**: Basic script from template
```
After 4 years and a wedding, my partner left me for a guy on Discord.

I met my partner 4 years ago. Red flags were everywhere...
```

**After**: Claude Haiku optimizes for virality
```
# PART 1: THE DISCORD BETRAYAL

I spent 4 years building a life with someone.

A condo. A dog. A wedding date.

Then she left me for a guy she met on Discord.

...
```

**What AI adds**:
- Powerful 3-second hook
- Dramatic pauses ("...")
- Short punchy sentences
- Emotional tension
- Cliffhanger endings
- Conversational tone

**Cost**: $0.0018 per video (0.18 cents!)

---

## Video Parts Breakdown

Your story is split into 3 parts:

| Part | Words | Duration | Status |
|------|-------|----------|--------|
| Part 1 | 280 | ~2 min | Ready to generate |
| Part 2 | 235 | ~1.5 min | Ready to generate |
| Part 3 | 295 | ~2 min | Ready to generate |

### Generate All Parts:

```bash
# Part 1
python src/generators/video_generator.py e6dd307b-caa4-4de7-bbb0-6fd650c2a32a --part 1

# Part 2
python src/generators/video_generator.py e6dd307b-caa4-4de7-bbb0-6fd650c2a32a --part 2

# Part 3
python src/generators/video_generator.py e6dd307b-caa4-4de7-bbb0-6fd650c2a32a --part 3
```

---

## Vercel Dashboard Deployment

Once videos are generating successfully, deploy the dashboard:

### Quick Deploy:

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel
```

### Add Environment Variables in Vercel Dashboard:

1. Go to your project in Vercel
2. Settings → Environment Variables
3. Add:
   - `SUPABASE_URL` = `https://yoxkfigtbhlpdohirrtt.supabase.co`
   - `SUPABASE_KEY` = Your anon key
   - `DASHBOARD_PASSWORD` = Your chosen password (default: admin123)

### Access Dashboard:

- Local: `http://localhost:8501` (run `streamlit run streamlit_app.py`)
- Vercel: `https://your-project.vercel.app`

---

## Final Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] AI enhancement tested (`python test_ai_enhancement.py`)
- [ ] Part 1 video generated successfully
- [ ] Part 2 video generated (optional)
- [ ] Part 3 video generated (optional)
- [ ] Dashboard deployed to Vercel (optional)

---

## Cost Summary (Monthly)

| Service | Cost |
|---------|------|
| Claude Haiku AI (150 videos) | $0.26 |
| Vercel hosting | $0 |
| Supabase database | $0 |
| Google Drive storage | $0 |
| **TOTAL** | **$0.26/month** |

---

## Next Steps

1. **Right now**: Create virtual environment and install dependencies
2. **Test**: Run `python test_ai_enhancement.py` to see AI working
3. **Generate**: Create Part 1 video with all improvements
4. **Watch**: See the difference between old and new videos
5. **Deploy**: Put dashboard on Vercel for remote access

---

**Need help?** Check the troubleshooting section above or run commands one at a time to see where it fails.
