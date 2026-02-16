"""Phase 1 pipeline: Scrape Reddit, select stories, and generate videos."""

import sys
from pathlib import Path
from src.scrapers.reddit_scraper import RedditScraper
from src.processors.story_selector import StorySelector
from src.generators.video_generator import VideoGenerator
from src.utils.logger import get_logger

logger = get_logger(__name__)

def run_phase1_pipeline(story_count: int = 1):
    """Run complete Phase 1 pipeline.

    Args:
        story_count: Number of stories to process (default 1 for Phase 1)

    Returns:
        Number of videos generated
    """
    print("=" * 60)
    print("PHASE 1 PIPELINE: Reddit to Video")
    print("=" * 60)

    # Step 1: Scrape Reddit
    print("\n[1/3] Scraping Reddit stories...")
    print("-" * 60)

    scraper = RedditScraper()

    if not scraper.test_connection():
        print("❌ Failed to connect to Reddit. Check your .env file.")
        return 0

    scraped_count = scraper.scrape_and_save()

    if scraped_count == 0:
        print("❌ No stories scraped. Check logs for details.")
        return 0

    print(f"✅ Scraped {scraped_count} stories")

    # Step 2: Select top stories
    print(f"\n[2/3] Selecting top {story_count} story/stories...")
    print("-" * 60)

    selector = StorySelector()
    stories = selector.select_top_stories(count=story_count)

    if not stories:
        print("❌ No stories selected.")
        return 0

    print(f"✅ Selected {len(stories)} story/stories:")
    for i, story in enumerate(stories, 1):
        print(f"  {i}. {story['title'][:50]}... (virality: {story['virality_score']})")

    # Step 3: Generate videos
    print(f"\n[3/3] Generating videos...")
    print("-" * 60)

    generator = VideoGenerator()

    # Check backgrounds exist
    if not generator.get_random_background():
        print("\n❌ No background videos found!")
        print(f"Please download videos to: {generator.backgrounds_dir}")
        print("\nQuick instructions:")
        print("1. Go to https://www.pexels.com/search/videos/minecraft%20parkour/")
        print("2. Download 1-2 videos (1080p or higher)")
        print(f"3. Save to: {generator.backgrounds_dir}/minecraft_parkour_01.mp4")
        return 0

    videos_generated = 0

    for i, story in enumerate(stories, 1):
        print(f"\nGenerating video {i}/{len(stories)}: {story['title'][:50]}...")

        video_path = generator.generate_video(story)

        if video_path:
            print(f"✅ Video generated: {video_path.name}")
            videos_generated += 1

            # Simple CLI approval
            print("\nPreview:")
            print(f"  Title: {story['title']}")
            print(f"  Virality Score: {story['virality_score']}")
            print(f"  Word Count: {story.get('word_count', 'N/A')}")
            print(f"  Video Location: {video_path}")

            while True:
                response = input("\nApprove this video? (y/n): ").lower().strip()

                if response == 'y':
                    # Update video status to approved
                    from src.database.supabase_client import db
                    videos = db.get_videos_by_status("pending_approval")
                    for vid in videos:
                        if vid["story_id"] == story["id"]:
                            db.update_video_status(vid["id"], "approved", approved_by="CLI")
                            print("✅ Video approved!")
                            break
                    break
                elif response == 'n':
                    # Update video status to rejected
                    from src.database.supabase_client import db
                    videos = db.get_videos_by_status("pending_approval")
                    for vid in videos:
                        if vid["story_id"] == story["id"]:
                            db.update_video_status(vid["id"], "rejected", rejection_reason="Manual rejection via CLI")
                            print("❌ Video rejected.")
                            break
                    break
                else:
                    print("Please enter 'y' or 'n'")

        else:
            print(f"❌ Failed to generate video for story {i}")

    # Summary
    print("\n" + "=" * 60)
    print(f"PIPELINE COMPLETE")
    print("=" * 60)
    print(f"Stories scraped: {scraped_count}")
    print(f"Stories selected: {len(stories)}")
    print(f"Videos generated: {videos_generated}")
    print("=" * 60)

    return videos_generated

if __name__ == "__main__":
    # Get story count from command line, default to 1
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    try:
        videos_count = run_phase1_pipeline(story_count=count)

        if videos_count > 0:
            print("\n✅ Phase 1 pipeline completed successfully!")
            print(f"\nGenerated {videos_count} video(s). Check the data/videos/ folder.")
        else:
            print("\n❌ No videos generated. Check logs for errors.")

    except KeyboardInterrupt:
        print("\n\n❌ Pipeline interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)
