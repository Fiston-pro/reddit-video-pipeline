"""Manually insert a test story into the database (for testing without Reddit API)."""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.database.supabase_client import db
from src.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

# Sample story for testing
TEST_STORY = {
    "reddit_id": "test_story_001",
    "title": "My Wife Cheated With My Best Friend - I Need Advice",
    "body": """I cannot believe I am writing this. Last week I discovered my wife of 5 years has been having an affair with my best friend since college. I found out when I came home early from work and saw his car in our driveway. When I walked in, they were together in our bedroom. I feel completely betrayed by the two people I trusted most in the world. I do not know what to do. We have two young kids and I am worried about how this will affect them. Should I try to work things out or is this unforgivable? I am lost and need advice from anyone who has been through something similar.""",
    "author": "test_user",
    "created_utc": datetime.now().isoformat(),
    "upvotes": 450,
    "comments": 89,
    "upvote_ratio": 0.95,
    "awards": 3,
    "virality_score": 75.5,
    "sentiment_score": -0.6,
    "status": "scraped"
}

def insert_test_story():
    """Insert test story into database."""
    print("=" * 60)
    print("MANUAL STORY INSERTION")
    print("=" * 60)
    print("\nThis will insert a test story into your Supabase database.")
    print("\nStory details:")
    print(f"  Title: {TEST_STORY['title']}")
    print(f"  Length: {len(TEST_STORY['body'])} characters")
    print(f"  Virality Score: {TEST_STORY['virality_score']}")
    print()

    # Test connection first
    print("Testing database connection...")
    if not db.test_connection():
        print("\n❌ Database connection failed!")
        print("\nPossible issues:")
        print("1. Incorrect SUPABASE_KEY in .env file")
        print("2. Incorrect SUPABASE_URL in .env file")
        print("3. Database tables not created yet")
        print("\nSee GET_SUPABASE_KEY.md for help getting the correct key.")
        return False

    print("✅ Database connection successful!\n")

    # Insert story
    print("Inserting test story...")
    result = db.insert_story(TEST_STORY)

    if result:
        print(f"\n✅ Story inserted successfully!")
        print(f"Story ID: {result['id']}")
        print(f"\nYou can now:")
        print(f"1. Select this story: python src/processors/story_selector.py")
        print(f"2. Generate a video: python src/generators/video_generator.py {result['id']}")
        return True
    else:
        print("\n❌ Failed to insert story")
        print("Check the logs for details.")
        return False

def insert_multiple_stories(count=5):
    """Insert multiple test stories with variations."""
    print(f"\nInserting {count} test stories...\n")

    stories = [
        {
            **TEST_STORY,
            "reddit_id": f"test_story_{i:03d}",
            "title": f"Test Story {i}: {TEST_STORY['title']}",
            "upvotes": 100 + (i * 50),
            "virality_score": 50 + (i * 5),
        }
        for i in range(1, count + 1)
    ]

    success_count = 0
    for i, story in enumerate(stories, 1):
        print(f"[{i}/{count}] Inserting: {story['title'][:50]}...")
        result = db.insert_story(story)
        if result:
            print(f"  ✅ Inserted (ID: {result['id']})")
            success_count += 1
        else:
            print(f"  ❌ Failed")

    print(f"\n✅ Inserted {success_count}/{count} stories")
    return success_count

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Insert test stories into database")
    parser.add_argument("--multiple", type=int, help="Insert multiple test stories (specify count)")
    args = parser.parse_args()

    if args.multiple:
        insert_multiple_stories(args.multiple)
    else:
        insert_test_story()
