"""Supabase database client for managing stories, videos, and metrics."""

import os
from typing import List, Dict, Optional, Any
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()

class SupabaseClient:
    """Wrapper for Supabase database operations."""

    def __init__(self):
        """Initialize Supabase client."""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in .env file"
            )

        self.client: Client = create_client(self.url, self.key)
        logger.info("Supabase client initialized")

    # ========================================================================
    # STORIES TABLE
    # ========================================================================

    def insert_story(self, story_data: Dict[str, Any]) -> Optional[Dict]:
        """Insert a new story into the database.

        Args:
            story_data: Dictionary with story fields (reddit_id, title, body, etc.)

        Returns:
            Inserted story data or None if failed
        """
        try:
            result = self.client.table("stories").insert(story_data).execute()
            logger.info(f"Inserted story: {story_data.get('reddit_id')}")
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to insert story: {e}")
            return None

    def get_stories_by_status(self, status: str, limit: int = 100) -> List[Dict]:
        """Get stories filtered by status.

        Args:
            status: Story status ('scraped', 'selected', 'processed', 'rejected')
            limit: Maximum number of stories to return

        Returns:
            List of story dictionaries
        """
        try:
            result = (
                self.client.table("stories")
                .select("*")
                .eq("status", status)
                .order("virality_score", desc=True)
                .limit(limit)
                .execute()
            )
            return result.data
        except Exception as e:
            logger.error(f"Failed to get stories: {e}")
            return []

    def update_story_status(self, story_id: str, status: str) -> bool:
        """Update story status.

        Args:
            story_id: Story UUID
            status: New status

        Returns:
            True if successful
        """
        try:
            self.client.table("stories").update({"status": status}).eq("id", story_id).execute()
            logger.info(f"Updated story {story_id} status to {status}")
            return True
        except Exception as e:
            logger.error(f"Failed to update story status: {e}")
            return False

    # ========================================================================
    # VIDEOS TABLE
    # ========================================================================

    def insert_video(self, video_data: Dict[str, Any]) -> Optional[Dict]:
        """Insert a new video into the database.

        Args:
            video_data: Dictionary with video fields (story_id, video_url, etc.)

        Returns:
            Inserted video data or None if failed
        """
        try:
            result = self.client.table("videos").insert(video_data).execute()
            logger.info(f"Inserted video for story: {video_data.get('story_id')}")
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to insert video: {e}")
            return None

    def get_videos_by_status(self, status: str) -> List[Dict]:
        """Get videos filtered by status.

        Args:
            status: Video status ('pending_approval', 'approved', 'rejected')

        Returns:
            List of video dictionaries with story data
        """
        try:
            result = (
                self.client.table("videos")
                .select("*, stories(*)")
                .eq("status", status)
                .order("created_at", desc=True)
                .execute()
            )
            return result.data
        except Exception as e:
            logger.error(f"Failed to get videos: {e}")
            return []

    def update_video_status(
        self,
        video_id: str,
        status: str,
        approved_by: Optional[str] = None,
        rejection_reason: Optional[str] = None
    ) -> bool:
        """Update video approval status.

        Args:
            video_id: Video UUID
            status: New status ('approved' or 'rejected')
            approved_by: Username who approved/rejected
            rejection_reason: Reason for rejection (if rejected)

        Returns:
            True if successful
        """
        try:
            update_data = {"status": status}

            if status == "approved":
                update_data["approved_at"] = datetime.now().isoformat()
                if approved_by:
                    update_data["approved_by"] = approved_by
            elif status == "rejected" and rejection_reason:
                update_data["rejection_reason"] = rejection_reason

            self.client.table("videos").update(update_data).eq("id", video_id).execute()
            logger.info(f"Updated video {video_id} status to {status}")
            return True
        except Exception as e:
            logger.error(f"Failed to update video status: {e}")
            return False

    # ========================================================================
    # PLATFORM_POSTS TABLE
    # ========================================================================

    def insert_platform_post(self, post_data: Dict[str, Any]) -> Optional[Dict]:
        """Insert a platform post record.

        Args:
            post_data: Dictionary with platform post fields

        Returns:
            Inserted post data or None if failed
        """
        try:
            result = self.client.table("platform_posts").insert(post_data).execute()
            logger.info(f"Inserted platform post: {post_data.get('platform')}")
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to insert platform post: {e}")
            return None

    def update_platform_post_status(
        self,
        post_id: str,
        status: str,
        post_url: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> bool:
        """Update platform post status.

        Args:
            post_id: Post UUID
            status: New status ('published' or 'failed')
            post_url: URL of published post
            error_message: Error message if failed

        Returns:
            True if successful
        """
        try:
            update_data = {"status": status}

            if status == "published":
                update_data["published_at"] = datetime.now().isoformat()
                if post_url:
                    update_data["post_url"] = post_url
            elif status == "failed" and error_message:
                update_data["error_message"] = error_message

            self.client.table("platform_posts").update(update_data).eq("id", post_id).execute()
            logger.info(f"Updated platform post {post_id} status to {status}")
            return True
        except Exception as e:
            logger.error(f"Failed to update platform post status: {e}")
            return False

    # ========================================================================
    # PLATFORM_METRICS TABLE
    # ========================================================================

    def insert_metrics(self, metrics_data: Dict[str, Any]) -> Optional[Dict]:
        """Insert platform metrics.

        Args:
            metrics_data: Dictionary with metric fields

        Returns:
            Inserted metrics data or None if failed
        """
        try:
            result = self.client.table("platform_metrics").insert(metrics_data).execute()
            logger.info(f"Inserted metrics for post: {metrics_data.get('post_id')}")
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to insert metrics: {e}")
            return None

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def test_connection(self) -> bool:
        """Test database connection.

        Returns:
            True if connection successful
        """
        try:
            result = self.client.table("stories").select("count", count="exact").limit(1).execute()
            logger.info("Database connection successful")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False

# Global database client
db = SupabaseClient()

__all__ = ["SupabaseClient", "db"]

# Test connection if run directly
if __name__ == "__main__":
    print("Testing Supabase connection...")
    client = SupabaseClient()
    if client.test_connection():
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed. Check your .env file.")
