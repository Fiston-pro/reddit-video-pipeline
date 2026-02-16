"""Story selection logic for choosing best stories to convert to videos."""

from typing import List, Dict, Optional
from src.database.supabase_client import db
from src.utils.logger import get_logger
from src.utils.config_loader import config
from src.processors.text_cleaner import clean_story_for_video

logger = get_logger(__name__)

class StorySelector:
    """Select and process top stories for video creation."""

    def __init__(self):
        """Initialize story selector."""
        self.max_words = config.get("reddit.max_words", 1500)
        logger.info("Story selector initialized")

    def get_unprocessed_stories(self, limit: int = 100) -> List[Dict]:
        """Get stories that haven't been processed yet.

        Args:
            limit: Maximum number of stories to fetch

        Returns:
            List of story dictionaries sorted by virality score
        """
        stories = db.get_stories_by_status("scraped", limit=limit)
        logger.info(f"Found {len(stories)} unprocessed stories")
        return stories

    def select_top_stories(self, count: int = 5) -> List[Dict]:
        """Select top N stories by virality score.

        Args:
            count: Number of stories to select

        Returns:
            List of selected story dictionaries with cleaned text
        """
        # Get all scraped stories
        stories = self.get_unprocessed_stories()

        if not stories:
            logger.warning("No stories available for selection")
            return []

        # Already sorted by virality_score (DESC) from database
        top_stories = stories[:count]

        logger.info(f"Selected top {len(top_stories)} stories")

        # Clean and prepare each story
        processed_stories = []
        for story in top_stories:
            # Clean text for TTS
            cleaned = clean_story_for_video(story["title"], story["body"])

            # Add cleaned data to story
            story["cleaned_title"] = cleaned["title"]
            story["cleaned_body"] = cleaned["body"]
            story["full_text"] = cleaned["full_text"]
            story["word_count"] = cleaned["word_count"]

            # Update status to 'selected'
            db.update_story_status(story["id"], "selected")

            processed_stories.append(story)

            logger.info(
                f"Selected story {story['reddit_id']}: "
                f"{story['title'][:50]}... "
                f"(virality: {story['virality_score']}, words: {story['word_count']})"
            )

        return processed_stories

    def get_story_by_id(self, story_id: str) -> Optional[Dict]:
        """Get a specific story by ID and prepare it.

        Args:
            story_id: Story UUID

        Returns:
            Story dictionary with cleaned text or None
        """
        try:
            result = db.client.table("stories").select("*").eq("id", story_id).execute()
            if not result.data:
                logger.warning(f"Story {story_id} not found")
                return None

            story = result.data[0]

            # Clean text
            cleaned = clean_story_for_video(story["title"], story["body"])
            story["cleaned_title"] = cleaned["title"]
            story["cleaned_body"] = cleaned["body"]
            story["full_text"] = cleaned["full_text"]
            story["word_count"] = cleaned["word_count"]

            return story

        except Exception as e:
            logger.error(f"Failed to get story: {e}")
            return None

# CLI interface
if __name__ == "__main__":
    import sys

    selector = StorySelector()

    # Get number of stories from command line, default to 1 for Phase 1
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    print(f"Selecting top {count} story/stories...")
    stories = selector.select_top_stories(count)

    if stories:
        print(f"\n✅ Selected {len(stories)} story/stories:\n")
        for i, story in enumerate(stories, 1):
            print(f"{i}. {story['title']}")
            print(f"   Virality: {story['virality_score']}")
            print(f"   Words: {story['word_count']}")
            print(f"   ID: {story['id']}\n")
    else:
        print("❌ No stories found. Run reddit_scraper.py first.")
