# AI Enhancement & Random Backgrounds Guide

## What's New ✨

### 1. Random Background Switching 🎬
Videos now switch between **different backgrounds every 12 seconds** instead of using one background throughout.

**Before**:
- Minecraft parkour for entire 2 minutes → boring, repetitive

**After**:
- 0-12s: Minecraft parkour
- 12-24s: Subway Surfer
- 24-36s: Satisfying loops
- 36-48s: (random again)
- And so on... → **much more engaging!**

**Why it works**:
- Keeps viewers engaged
- Mimics viral TikTok style
- No two videos look the same

---

### 2. AI-Enhanced Scripts with Claude Haiku 🤖

Every script is now optimized for **maximum virality** using Claude Haiku AI.

**What AI Does**:
1. **Powerful 3-second hooks** that make people STOP scrolling
2. **Dramatic pacing** - short punchy sentences for emotional impact
3. **Natural pauses** with "..." for dramatic effect
4. **Tension building** and emotional peaks
5. **Conversational tone** - sounds like a friend telling you a story
6. **Cliffhangers** for multi-part series
7. **Binge-worthy structure** - people NEED to know what happens next

**Example Transformation**:

**Before (Basic Script)**:
```
After 4 years and a wedding, my partner left me for a guy on Discord.

I met my partner 4 years ago. Red flags were everywhere, but I ignored them...
```

**After (AI-Enhanced)**:
```
Four years... a wedding... all of it meant nothing.

My wife left me for someone she'd never even met in person.

A guy on Discord.

Let that sink in. Discord.

We had a condo. A dog. A life. Or so I thought...
```

See the difference? **Dramatic pauses, emotional impact, immediate hook.**

---

## Costs Breakdown 💰

### Current Monthly Costs

| Service | What It Does | Free Tier | Cost |
|---------|-------------|-----------|------|
| **Claude Haiku API** | AI script enhancement | None | **$0.30/month** |
| **Vercel Hosting** | Dashboard UI | 100GB bandwidth | **$0** |
| **Supabase** | Database | 500MB, 2GB transfer | **$0** |
| **Google Drive** | Video storage | 15GB | **$0** |
| **gTTS** | Text-to-speech | Unlimited | **$0** |
| **Total** | | | **$0.30/month** |

### AI Enhancement Cost Details

**Claude Haiku Pricing**:
- Input: $0.0008 per 1M tokens ($0.0000008 per token)
- Output: $0.004 per 1M tokens ($0.000004 per token)

**Per Script**:
- Input: ~800 tokens (original script + prompt)
- Output: ~400 tokens (enhanced script)
- **Cost**: ~$0.0024 per video (0.24 cents)

**Monthly** (30 videos/day):
- 30 videos × 30 days = 900 videos
- 900 × $0.0024 = **$2.16/month**

Wait, that's higher! Let me recalculate:

Actually for 5 videos/day (your plan):
- 5 videos × 30 days = 150 videos/month
- 150 × $0.0024 = **$0.36/month**

**Still under 50 cents!** 🎉

---

## Vercel Hosting - It's FREE! ✅

### What You Were Worried About (Wrong!)
❌ "Video storage on Vercel will cost a lot"
❌ "Bandwidth will exceed free tier"

### Reality ✅
✅ **Vercel hosts ONLY the dashboard UI** (~5MB total)
✅ **Videos stay on Google Drive** (15GB free, ~160 videos)
✅ **Database on Supabase** (free tier, plenty)
✅ **100GB/month bandwidth** is more than enough for a dashboard

### How It Works
```
User opens dashboard on phone
       ↓
Vercel serves HTML/CSS/JS (5MB, one-time)
       ↓
Dashboard fetches metadata from Supabase (tiny API calls)
       ↓
Videos are streamed from Google Drive (NOT through Vercel)
       ↓
Zero Vercel bandwidth used for videos!
```

### Why It's Perfect for "On the Fly" Access
- ✅ Access from **phone, tablet, anywhere**
- ✅ **Approve videos** while at coffee shop
- ✅ **Check analytics** remotely
- ✅ **No PC needed** for approval workflow
- ✅ **Always online** (no need to keep PC running)

---

## Setup Instructions

### 1. Get Claude API Key (For AI Enhancement)

1. Go to: https://console.anthropic.com/
2. Sign up / Log in
3. Go to **API Keys** section
4. Create new key
5. Add to `.env`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

**Free Credits**: You get $5 free credits → enough for ~2000 scripts!

After that: Add payment method, but you'll only pay for what you use (~$0.36/month for 150 videos)

### 2. Install New Dependencies

```bash
pip install anthropic==0.39.0
pip install gTTS==2.5.0
```

Or just:
```bash
pip install -r requirements.txt
```

### 3. Test AI Enhancement

```bash
python src/processors/ai_script_enhancer.py
```

You should see:
- Original script
- AI-enhanced script (with better hooks, pacing)
- Multiple hook options generated

### 4. Generate Videos with New Features

```bash
python src/generators/video_generator.py e6dd307b-caa4-4de7-bbb0-6fd650c2a32a
```

**What happens**:
1. Loads story from database
2. Generates basic script (from script_generator.py)
3. **AI enhances script** (Claude Haiku makes it viral)
4. Generates TTS voiceover
5. **Creates background with random switching** every 12 seconds
6. Composites final video
7. Saves to database

### 5. Deploy Dashboard to Vercel (Optional)

See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for full guide.

Quick version:
```bash
npm install -g vercel
vercel login
vercel
```

Add environment variables in Vercel dashboard:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `DASHBOARD_PASSWORD`

---

## Testing the Improvements

Let's generate Part 1 again with AI enhancement and random backgrounds:

```bash
# Delete old Part 1 video (optional)
rm data/videos/video_e6dd307b-caa4-4de7-bbb0-6fd650c2a32a_*.mp4

# Generate new Part 1 with AI + random backgrounds
python src/generators/video_generator.py e6dd307b-caa4-4de7-bbb0-6fd650c2a32a
```

**Compare**:
- Old version: One background, basic script
- New version: Multiple backgrounds, AI-enhanced viral script

---

## Disabling AI Enhancement (If Needed)

If you don't want to use AI or don't have API key:

**Option 1**: Don't set `ANTHROPIC_API_KEY` in `.env`
- AI enhancement automatically disabled
- Falls back to basic script from script_generator.py
- Still gets random backgrounds

**Option 2**: Comment out AI enhancement in video_generator.py:
```python
# Enhance script with AI for maximum virality
# logger.info("Enhancing script with AI for viral hooks and pacing...")
# script = self.ai_enhancer.enhance_script(script, story['title'])
```

---

## Cost Comparison: Free vs Paid

### Fully Free Setup ($0/month)
- ✅ Random backgrounds
- ✅ Basic engaging scripts (script_generator.py)
- ✅ gTTS voiceover
- ✅ Google Drive storage
- ✅ Supabase database
- ✅ Vercel dashboard
- ❌ No AI enhancement

**Quality**: Good, but scripts not optimized

### With AI Enhancement ($0.36/month)
- ✅ All of the above
- ✅ **AI-optimized viral scripts**
- ✅ **Powerful hooks**
- ✅ **Dramatic pacing**
- ✅ **Higher engagement**

**Quality**: Viral-ready, professional

---

## Recommended: Try Both!

1. **Start with AI** using free credits ($5 free = 2000 videos)
2. **Compare results** - do AI-enhanced videos perform better?
3. **Decide** if $0.36/month is worth it for better engagement

My bet: **YES**, the AI enhancement is worth 36 cents 😄

---

## Next Steps

1. ✅ Get Claude API key (free $5 credits)
2. ✅ Add to `.env`
3. ✅ Install dependencies
4. ✅ Test AI enhancement
5. ✅ Generate Part 1, 2, 3 with new features
6. ✅ Deploy dashboard to Vercel
7. 🚀 **Start going viral!**
