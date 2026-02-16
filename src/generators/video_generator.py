"""Video generator for creating TikTok-style videos from stories."""

import random
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# Fix for Pillow 10.x compatibility with MoviePy
try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS
except ImportError:
    pass

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip
)
from src.generators.tts_engine import TTSEngine
from src.processors.script_generator import ScriptGenerator
from src.processors.ai_script_enhancer import AIScriptEnhancer
from src.database.supabase_client import db
from src.utils.logger import get_logger
from src.utils.config_loader import config

logger = get_logger(__name__)

class VideoGenerator:
    """Generate videos from Reddit stories."""

    def __init__(self):
        """Initialize video generator."""
        self.tts = TTSEngine()
        self.script_generator = ScriptGenerator(max_words_per_video=300)
        self.ai_enhancer = AIScriptEnhancer()

        # Directories
        self.project_root = Path(__file__).parent.parent.parent
        self.backgrounds_dir = self.project_root / "assets" / "backgrounds"
        self.data_dir = self.project_root / "data"
        self.videos_dir = self.data_dir / "videos"
        self.voiceovers_dir = self.data_dir / "voiceovers"

        # Create directories
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        self.voiceovers_dir.mkdir(parents=True, exist_ok=True)

        # Video settings
        self.fps = config.get("video.fps", 24)
        self.target_width = config.get("video.resolution")[0]  # 1080
        self.target_height = config.get("video.resolution")[1]  # 1920

        logger.info("Video generator initialized")

    def get_random_background(self) -> Optional[Path]:
        """Get a random background video.

        Returns:
            Path to background video or None if no backgrounds found
        """
        if not self.backgrounds_dir.exists():
            logger.error(f"Backgrounds directory not found: {self.backgrounds_dir}")
            return None

        backgrounds = list(self.backgrounds_dir.glob("*.mp4"))

        if not backgrounds:
            logger.error("No background videos found. Please download backgrounds first.")
            return None

        selected = random.choice(backgrounds)
        logger.info(f"Selected background: {selected.name}")
        return selected

    def crop_to_vertical(self, video: VideoFileClip) -> VideoFileClip:
        """Crop video to 9:16 aspect ratio (vertical/portrait).

        Args:
            video: Input video clip

        Returns:
            Cropped video clip
        """
        w, h = video.size
        target_aspect = self.target_width / self.target_height  # 9/16

        # Calculate crop dimensions
        if w / h > target_aspect:
            # Video is too wide, crop width
            new_width = int(h * target_aspect)
            x_center = w / 2
            x1 = int(x_center - new_width / 2)
            x2 = int(x_center + new_width / 2)
            cropped = video.crop(x1=x1, x2=x2)
        else:
            # Video is too tall, crop height
            new_height = int(w / target_aspect)
            y_center = h / 2
            y1 = int(y_center - new_height / 2)
            y2 = int(y_center + new_height / 2)
            cropped = video.crop(y1=y1, y2=y2)

        # Resize to target resolution
        resized = cropped.resize((self.target_width, self.target_height))

        logger.debug(f"Cropped video from {w}x{h} to {self.target_width}x{self.target_height}")
        return resized

    def loop_background_to_duration(
        self,
        background_path: Path,
        target_duration: float
    ) -> VideoFileClip:
        """Loop background video to match target duration.

        Args:
            background_path: Path to background video
            target_duration: Desired duration in seconds

        Returns:
            Looped and cropped video clip
        """
        # Load background
        bg = VideoFileClip(str(background_path))

        # Crop to 9:16
        bg = self.crop_to_vertical(bg)

        # Calculate how many loops needed
        loop_count = int(target_duration / bg.duration) + 1

        # Concatenate loops
        clips = [bg] * loop_count
        looped = concatenate_videoclips(clips)

        # Trim to exact duration
        final = looped.subclip(0, target_duration)

        logger.info(f"Looped background {loop_count} times to {target_duration:.1f}s")

        # Close original clip to free memory
        bg.close()

        return final

    def create_random_start_background(self, target_duration: float):
        """Create background video starting from a random position.

        Each video will use the same background asset but start at a different
        random timestamp, making each video look unique.

        Args:
            target_duration: Desired total duration in seconds

        Returns:
            Video clip with random start position
        """
        import random

        # Get all available backgrounds
        backgrounds = list(self.backgrounds_dir.glob("*.mp4"))
        if not backgrounds:
            logger.error("No background videos found")
            return None

        # Pick ONE random background
        bg_path = random.choice(backgrounds)
        logger.info(f"Selected background: {bg_path.name}")

        # Load and crop to vertical
        bg = VideoFileClip(str(bg_path))
        bg = self.crop_to_vertical(bg)

        # Choose a random start position
        # Make sure we have enough video left from the start position
        max_start = max(0, bg.duration - target_duration)
        random_start = random.uniform(0, max_start) if max_start > 0 else 0

        logger.info(f"Random start position: {random_start:.1f}s (background duration: {bg.duration:.1f}s)")

        # If background is shorter than needed, loop it
        if bg.duration < target_duration:
            loop_count = int(target_duration / bg.duration) + 1
            clips = [bg] * loop_count
            looped = concatenate_videoclips(clips)
            bg.close()

            # Start from random position in looped video
            final = looped.subclip(random_start, random_start + target_duration)
            logger.info(f"Looped background {loop_count} times and started at {random_start:.1f}s")
            return final
        else:
            # Extract segment from random start position
            final = bg.subclip(random_start, random_start + target_duration)
            logger.info(f"Extracted {target_duration:.1f}s clip starting at {random_start:.1f}s")
            return final

    def generate_video(
        self,
        story: Dict,
        output_filename: Optional[str] = None
    ) -> Optional[Path]:
        """Generate video from story.

        Args:
            story: Story dictionary with 'full_text', 'id', etc.
            output_filename: Optional custom output filename

        Returns:
            Path to generated video or None if failed
        """
        story_id = story["id"]

        # Generate engaging script with hook (standalone, no parts)
        logger.info(f"Generating engaging script for story {story_id}")
        script = self.script_generator.generate_script(
            story=story['body'],
            title=story['title'],
            max_duration=180  # 3 minutes max
        )

        word_count = len(script.split())
        logger.info(f"Generated script with {word_count} words (includes hook)")

        # Enhance script with AI for maximum virality
        logger.info("Enhancing script with AI for viral hooks and pacing...")
        script = self.ai_enhancer.enhance_script(script, story['title'])

        word_count = len(script.split())
        logger.info(f"AI-enhanced script with {word_count} words")
        logger.info(f"Generating video for story {story_id}")

        try:
            # Step 1: Generate voiceover from SCRIPT (not raw story)
            voiceover_path = self.voiceovers_dir / f"voiceover_{story_id}.mp3"
            logger.info("Generating TTS voiceover from engaging script...")

            if not self.tts.generate(script, str(voiceover_path)):
                logger.error("Failed to generate voiceover")
                return None

            # Step 2: Load audio to get duration
            audio = AudioFileClip(str(voiceover_path))
            duration = audio.duration
            logger.info(f"Voiceover duration: {duration:.1f}s")

            # Step 3: Create background video with random start position
            logger.info("Creating background video from random start position...")
            video = self.create_random_start_background(duration)
            if not video:
                logger.error("Failed to create background video")
                return None

            # Step 4: Add audio to video
            logger.info("Compositing final video...")
            final = video.set_audio(audio)

            # Step 5: Export video
            if output_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"video_{story_id}_{timestamp}.mp4"

            output_path = self.videos_dir / output_filename

            logger.info(f"Rendering video to {output_path}")
            final.write_videofile(
                str(output_path),
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                logger=None  # Suppress moviepy verbose output
            )

            # Calculate file size
            file_size_mb = output_path.stat().st_size / (1024 * 1024)

            logger.info(f"Video generated successfully: {output_path.name} ({file_size_mb:.1f}MB)")

            # Step 6: Save to database
            video_data = {
                "story_id": story_id,
                "video_url": str(output_path),  # Will update with Google Drive link later
                "local_path": str(output_path),
                "duration": duration,
                "file_size_mb": round(file_size_mb, 2),
                "status": "pending_approval"
            }

            db.insert_video(video_data)

            # Update story status
            db.update_story_status(story_id, "processed")

            # Cleanup
            audio.close()
            video.close()
            final.close()

            return output_path

        except Exception as e:
            logger.error(f"Failed to generate video: {e}", exc_info=True)
            return None

# CLI interface
if __name__ == "__main__":
    import sys
    from src.processors.story_selector import StorySelector

    generator = VideoGenerator()

    # Check if backgrounds exist
    if not generator.get_random_background():
        print("ERROR: No background videos found!")
        print(f"Please download videos to: {generator.backgrounds_dir}")
        print("\n1. Go to https://www.pexels.com/search/videos/minecraft%20parkour/")
        print("2. Download 1-2 videos (1080p or higher)")
        print(f"3. Save to: {generator.backgrounds_dir}/minecraft_parkour_01.mp4")
        sys.exit(1)

    # Get story ID from command line or select top story
    if len(sys.argv) > 1:
        story_id = sys.argv[1]
        selector = StorySelector()
        story = selector.get_story_by_id(story_id)
        if not story:
            print(f"ERROR: Story {story_id} not found")
            sys.exit(1)
    else:
        # Select top story
        print("No story ID provided, selecting top story...")
        selector = StorySelector()
        stories = selector.select_top_stories(count=1)

        if not stories:
            print("ERROR: No stories available. Run reddit_scraper.py first.")
            sys.exit(1)

        story = stories[0]

    print(f"\nGenerating video for: {story['title'][:50]}...")
    print(f"Story ID: {story['id']}")

    video_path = generator.generate_video(story)

    if video_path:
        print(f"\nVideo generated successfully!")
        print(f"Location: {video_path}")
        print(f"\nPlay the video to verify quality.")
    else:
        print("\nERROR: Video generation failed. Check logs for details.")
