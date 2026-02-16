"""Reddit scraper for fetching stories from r/cheating_stories."""

import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv
import praw
from textblob import TextBlob
from src.database.supabase_client import db
from src.utils.logger import get_logger
from src.utils.config_loader import config

logger = get_logger(__name__)
load_dotenv()

class RedditScraper:
    """Scrape Reddit stories and calculate virality scores."""

    def __init__(self):
        """Initialize Reddit scraper with PRAW."""
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "content-bot/1.0")
        )

        # Load configuration
        self.subreddit_name = config.get("reddit.subreddit", "cheating_stories")
        self.posts_per_day = config.get("reddit.posts_per_day", 50)
        self.min_upvotes = config.get("reddit.min_upvotes", 100)
        self.max_words = config.get("reddit.max_words", 1500)
        self.min_hours_old = config.get("reddit.min_hours_old", 1)

        # Virality weights
        self.weights = {
            "upvote_velocity": config.get("virality.upvote_velocity_weight", 0.30),
            "comment_velocity": config.get("virality.comment_velocity_weight", 0.25),
            "upvote_ratio": config.get("virality.upvote_ratio_weight", 0.15),
            "awards": config.get("virality.awards_weight", 0.15),
            "length": config.get("virality.length_weight", 0.10),
            "sentiment": config.get("virality.sentiment_weight", 0.05),
        }

        logger.info(f"Reddit scraper initialized for r/{self.subreddit_name}")

    def test_connection(self) -> bool:
        """Test Reddit API connection.

        Returns:
            True if connection successful
        """
        try:
            subreddit = self.reddit.subreddit(self.subreddit_name)
            _ = subreddit.display_name
            logger.info(f"Successfully connected to r/{self.subreddit_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Reddit: {e}")
            return False

    def calculate_virality_score(self, post_data: Dict) -> float:
        """Calculate virality score for a story.

        Args:
            post_data: Dictionary with post metrics

        Returns:
            Virality score (0-100+)
        """
        # Extract metrics
        upvotes = post_data.get("upvotes", 0)
        comments = post_data.get("comments", 0)
        upvote_ratio = post_data.get("upvote_ratio", 0)
        awards = post_data.get("awards", 0)
        word_count = len(post_data.get("body", "").split())
        hours_old = post_data.get("hours_old", 1)
        sentiment_score = post_data.get("sentiment_score", 0)

        # Calculate velocity metrics
        upvote_velocity = upvotes / max(hours_old, 0.1)
        comment_velocity = comments / max(hours_old, 0.1)

        # Length score (optimal length: 300-800 words)
        if 300 <= word_count <= 800:
            length_score = 1.0
        elif word_count < 300:
            length_score = word_count / 300
        else:
            length_score = max(0, 1 - (word_count - 800) / 700)

        # Sentiment score (absolute value - controversy matters)
        sentiment_contribution = abs(sentiment_score)

        # Weighted combination
        virality = (
            self.weights["upvote_velocity"] * min(upvote_velocity, 100) +
            self.weights["comment_velocity"] * min(comment_velocity, 50) +
            self.weights["upvote_ratio"] * (upvote_ratio * 100) +
            self.weights["awards"] * min(awards * 10, 50) +
            self.weights["length"] * (length_score * 100) +
            self.weights["sentiment"] * (sentiment_contribution * 100)
        )

        return round(virality, 2)

    def calculate_sentiment(self, text: str) -> float:
        """Calculate sentiment polarity of text.

        Args:
            text: Story text

        Returns:
            Sentiment score (-1 to 1, where -1 is negative, 1 is positive)
        """
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        except Exception as e:
            logger.warning(f"Failed to calculate sentiment: {e}")
            return 0.0

    def fetch_stories(self, limit: Optional[int] = None) -> List[Dict]:
        """Fetch top stories from subreddit.

        Args:
            limit: Maximum number of posts to fetch. If None, uses config value.

        Returns:
            List of story dictionaries
        """
        if limit is None:
            limit = self.posts_per_day

        subreddit = self.reddit.subreddit(self.subreddit_name)
        stories = []
        cutoff_time = datetime.utcnow() - timedelta(hours=24)

        logger.info(f"Fetching top {limit} posts from r/{self.subreddit_name}")

        try:
            for post in subreddit.top("day", limit=limit * 2):  # Fetch extra for filtering
                # Skip non-text posts
                if not post.is_self:
                    continue

                # Skip removed/deleted posts
                if post.removed_by_category or post.selftext in ["[removed]", "[deleted]"]:
                    continue

                # Calculate post age
                created_time = datetime.utcfromtimestamp(post.created_utc)
                hours_old = (datetime.utcnow() - created_time).total_seconds() / 3600

                # Skip very new posts (might not have enough engagement yet)
                if hours_old < self.min_hours_old:
                    continue

                # Skip if too few upvotes
                if post.score < self.min_upvotes:
                    continue

                # Skip if too long
                word_count = len(post.selftext.split())
                if word_count > self.max_words:
                    logger.debug(f"Skipping post {post.id}: too long ({word_count} words)")
                    continue

                # Calculate sentiment
                sentiment_score = self.calculate_sentiment(post.selftext)

                # Prepare story data
                story_data = {
                    "reddit_id": post.id,
                    "title": post.title,
                    "body": post.selftext,
                    "author": str(post.author) if post.author else "[deleted]",
                    "created_utc": created_time.isoformat(),
                    "upvotes": post.score,
                    "comments": post.num_comments,
                    "upvote_ratio": post.upvote_ratio,
                    "awards": post.total_awards_received,
                    "sentiment_score": sentiment_score,
                    "hours_old": hours_old,
                }

                # Calculate virality score
                story_data["virality_score"] = self.calculate_virality_score(story_data)

                stories.append(story_data)

                # Stop if we have enough stories
                if len(stories) >= limit:
                    break

                # Rate limiting (1 request per second)
                time.sleep(1)

            logger.info(f"Fetched {len(stories)} valid stories")
            return stories

        except Exception as e:
            logger.error(f"Error fetching stories: {e}")
            return []

    def save_stories_to_db(self, stories: List[Dict]) -> int:
        """Save stories to Supabase database.

        Args:
            stories: List of story dictionaries

        Returns:
            Number of stories successfully saved
        """
        saved_count = 0

        for story in stories:
            # Remove temporary fields not in database schema
            db_story = {k: v for k, v in story.items() if k not in ["hours_old"]}
            db_story["status"] = "scraped"
            db_story["scraped_at"] = datetime.now().isoformat()

            result = db.insert_story(db_story)
            if result:
                saved_count += 1

            # Rate limiting
            time.sleep(0.5)

        logger.info(f"Saved {saved_count}/{len(stories)} stories to database")
        return saved_count

    def scrape_and_save(self, limit: Optional[int] = None) -> int:
        """Main method: fetch stories and save to database.

        Args:
            limit: Maximum number of posts to fetch

        Returns:
            Number of stories saved
        """
        logger.info("Starting Reddit scrape")

        # Fetch stories
        stories = self.fetch_stories(limit)

        if not stories:
            logger.warning("No stories fetched")
            return 0

        # Save to database
        saved_count = self.save_stories_to_db(stories)

        logger.info(f"Scrape complete: {saved_count} stories saved")
        return saved_count

# CLI interface
if __name__ == "__main__":
    import sys

    scraper = RedditScraper()

    # Test connection if --test flag
    if "--test" in sys.argv:
        print("Testing Reddit connection...")
        if scraper.test_connection():
            print("✅ Reddit connection successful!")
        else:
            print("❌ Reddit connection failed. Check your .env file.")
        sys.exit(0)

    # Run scraper
    print(f"Scraping r/{scraper.subreddit_name}...")
    count = scraper.scrape_and_save()
    print(f"✅ Scraped and saved {count} stories")
