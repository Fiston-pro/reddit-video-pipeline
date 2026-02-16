"""Quick start script to test all components."""

import sys
from pathlib import Path

def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60 + "\n")

def check_env_file():
    """Check if .env file exists."""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found")
        print("\nPlease create .env file:")
        print("  1. Copy .env.example to .env")
        print("  2. Fill in your API credentials")
        print("\nSee SETUP.md for detailed instructions.")
        return False
    print("✅ .env file exists")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    print("Checking dependencies...")
    try:
        import praw
        import supabase
        import edge_tts
        import moviepy
        import textblob
        print("✅ All required packages installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e.name}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    import subprocess
    print("Checking FFmpeg...")
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✅ FFmpeg installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg not found")
        print("\nPlease install FFmpeg:")
        print("  Windows: Download from ffmpeg.org, add to PATH")
        print("  Mac: brew install ffmpeg")
        print("  Linux: sudo apt install ffmpeg")
        return False

def test_supabase():
    """Test Supabase connection."""
    print("Testing Supabase connection...")
    try:
        from src.database.supabase_client import SupabaseClient
        client = SupabaseClient()
        if client.test_connection():
            print("✅ Supabase connection successful")
            return True
        else:
            print("❌ Supabase connection failed")
            return False
    except Exception as e:
        print(f"❌ Supabase error: {e}")
        print("\nCheck your SUPABASE_URL and SUPABASE_KEY in .env")
        return False

def test_reddit():
    """Test Reddit connection."""
    print("Testing Reddit connection...")
    try:
        from src.scrapers.reddit_scraper import RedditScraper
        scraper = RedditScraper()
        if scraper.test_connection():
            print("✅ Reddit connection successful")
            return True
        else:
            print("❌ Reddit connection failed")
            return False
    except Exception as e:
        print(f"❌ Reddit error: {e}")
        print("\nCheck your REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in .env")
        return False

def test_tts():
    """Test TTS generation."""
    print("Testing TTS generation...")
    try:
        from src.generators.tts_engine import TTSEngine
        tts = TTSEngine()
        test_file = "test_quickstart_tts.mp3"
        success = tts.generate("This is a test.", test_file)
        if success:
            print(f"✅ TTS working - generated {test_file}")
            # Cleanup
            Path(test_file).unlink(missing_ok=True)
            return True
        else:
            print("❌ TTS generation failed")
            return False
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return False

def check_backgrounds():
    """Check if background videos exist."""
    print("Checking background videos...")
    bg_dir = Path("assets/backgrounds")

    if not bg_dir.exists():
        bg_dir.mkdir(parents=True, exist_ok=True)
        print("❌ No background videos found")
        print(f"\nPlease download videos to: {bg_dir}")
        print("  1. Visit: https://www.pexels.com/search/videos/minecraft%20parkour/")
        print("  2. Download 1-2 videos (1080p+)")
        print(f"  3. Save as: {bg_dir}/minecraft_parkour_01.mp4")
        return False

    videos = list(bg_dir.glob("*.mp4"))
    if not videos:
        print("❌ No background videos found")
        print(f"\nPlease add .mp4 files to: {bg_dir}")
        return False

    print(f"✅ Found {len(videos)} background video(s):")
    for v in videos:
        print(f"  - {v.name}")
    return True

def run_quickstart():
    """Run all checks."""
    print_header("QUICKSTART - System Check")

    checks = [
        ("Environment file", check_env_file),
        ("Python dependencies", check_dependencies),
        ("FFmpeg", check_ffmpeg),
        ("Supabase database", test_supabase),
        ("Reddit API", test_reddit),
        ("Text-to-Speech", test_tts),
        ("Background videos", check_backgrounds),
    ]

    results = []

    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results.append((name, False))
        print()

    # Summary
    print_header("SUMMARY")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All checks passed! You're ready to run the pipeline.")
        print("\nNext step:")
        print("  python src/jobs/scrape_and_generate.py")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nSee SETUP.md for detailed setup instructions.")

if __name__ == "__main__":
    try:
        run_quickstart()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
