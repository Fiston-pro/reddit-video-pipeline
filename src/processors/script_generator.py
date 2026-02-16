"""Script generator for creating engaging video narratives from stories."""

import re
from typing import Dict, List, Tuple
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ScriptGenerator:
    """Generate engaging video scripts from Reddit stories."""

    def __init__(self, max_words_per_video: int = 300):
        """Initialize script generator.

        Args:
            max_words_per_video: Maximum words per video (default ~2 min)
        """
        self.max_words_per_video = max_words_per_video
        logger.info(f"Script generator initialized (max {max_words_per_video} words/video)")

    def extract_hook(self, story: str) -> str:
        """Extract the most engaging hook from the story.

        Args:
            story: Full story text

        Returns:
            Engaging hook sentence
        """
        # Common hook patterns
        hook_patterns = [
            r"(After \d+ years[^.]+\.)(?=\s)",  # "After X years..."
            r"(I (?:just|never) (?:found out|discovered|learned)[^.]+\.)(?=\s)",  # "I just found out..."
            r"(My (?:wife|husband|partner|girlfriend|boyfriend)[^.]+(?:cheated|left)[^.]+\.)(?=\s)",  # "My wife cheated..."
            r"(Everything (?:changed|fell apart|was ruined)[^.]+\.)(?=\s)",  # "Everything changed..."
        ]

        # Try to find a hook
        for pattern in hook_patterns:
            match = re.search(pattern, story, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # If no pattern matches, use first sentence
        sentences = re.split(r'[.!?]+\s+', story)
        if sentences:
            first = sentences[0].strip()
            # Make sure it ends with punctuation
            if not first.endswith(('.', '!', '?')):
                first += '.'
            return first

        return ""

    def create_engaging_intro(self, hook: str) -> str:
        """Create an engaging intro with the hook.

        Args:
            hook: The extracted hook

        Returns:
            Engaging intro text
        """
        intros = [
            f"You won't believe what just happened. {hook}",
            f"This story is insane. {hook}",
            f"So this just happened to me. {hook}",
            f"I need to tell you this story. {hook}",
            f"Listen to this. {hook}",
        ]

        # Pick based on hook content
        if "after" in hook.lower() and "year" in hook.lower():
            return f"After all this time... {hook}"
        elif "found out" in hook.lower() or "discovered" in hook.lower():
            return f"I just found out something devastating. {hook}"
        elif "cheated" in hook.lower():
            return f"I never thought this would happen to me. {hook}"
        else:
            return intros[0]  # Default

    def split_into_parts(self, story: str, title: str = "") -> List[Dict[str, str]]:
        """Split a long story into multiple parts.

        Args:
            story: Full story text
            title: Story title (optional, won't be used in script)

        Returns:
            List of parts, each with 'script', 'part_number', 'total_parts'
        """
        # Remove TL;DR and metadata
        story = re.sub(r'TL;DR:.*?(?=\n\n|\Z)', '', story, flags=re.DOTALL | re.IGNORECASE)
        story = re.sub(r'⸻+', '', story)
        story = story.strip()

        # Count words
        words = story.split()
        total_words = len(words)

        logger.info(f"Story has {total_words} words")

        # If story is short enough for one video
        if total_words <= self.max_words_per_video:
            hook = self.extract_hook(story)
            intro = self.create_engaging_intro(hook)

            # Remove the hook from the main story to avoid repetition
            story_without_hook = story.replace(hook, "", 1).strip()

            script = f"{intro}\n\n{story_without_hook}"

            return [{
                'script': script,
                'part_number': 1,
                'total_parts': 1,
                'word_count': len(script.split())
            }]

        # Split into multiple parts
        paragraphs = [p.strip() for p in story.split('\n\n') if p.strip()]
        parts = []
        current_part = []
        current_word_count = 0
        part_num = 1

        # First part gets the hook
        hook = self.extract_hook(story)
        intro = self.create_engaging_intro(hook)
        current_part.append(intro)
        current_word_count += len(intro.split())

        # Remove hook from first paragraph if it's there
        if paragraphs and hook in paragraphs[0]:
            paragraphs[0] = paragraphs[0].replace(hook, "", 1).strip()

        for para in paragraphs:
            para_words = len(para.split())

            # If adding this paragraph exceeds limit, save current part
            if current_word_count + para_words > self.max_words_per_video and current_part:
                parts.append({
                    'script': '\n\n'.join(current_part),
                    'part_number': part_num,
                    'total_parts': 0,  # Will update later
                    'word_count': current_word_count
                })

                # Start new part
                part_num += 1
                current_part = []
                current_word_count = 0

            current_part.append(para)
            current_word_count += para_words

        # Add remaining content
        if current_part:
            parts.append({
                'script': '\n\n'.join(current_part),
                'part_number': part_num,
                'total_parts': 0,
                'word_count': current_word_count
            })

        # Update total_parts
        total = len(parts)
        for part in parts:
            part['total_parts'] = total

        logger.info(f"Split story into {total} parts")

        return parts

    def generate_script(self, story: str, title: str = "", max_duration: int = 180) -> str:
        """Generate an engaging script from a story.

        Args:
            story: Full story text
            title: Story title (won't be read)
            max_duration: Maximum video duration in seconds (default 180s = 3 min)

        Returns:
            Engaging script ready for TTS with hook at start
        """
        # Remove TL;DR and metadata
        story = re.sub(r'TL;DR:.*?(?=\n\n|\Z)', '', story, flags=re.DOTALL | re.IGNORECASE)
        story = re.sub(r'⸻+', '', story)
        story = story.strip()

        # Extract hook for engaging opening
        hook = self.extract_hook(story)
        intro = self.create_engaging_intro(hook)

        # Remove the hook from the main story to avoid repetition
        story_without_hook = story.replace(hook, "", 1).strip()

        # Combine intro + story
        full_script = f"{intro}\n\n{story_without_hook}"

        # If script is too long (estimate ~150 words per minute for TTS)
        words = full_script.split()
        estimated_duration = (len(words) / 150) * 60  # seconds

        if estimated_duration > max_duration:
            # Trim to fit max duration
            max_words = int((max_duration / 60) * 150)
            words = words[:max_words]
            full_script = ' '.join(words)
            logger.info(f"Trimmed script from {len(full_script.split())} to {max_words} words to fit {max_duration}s")

        return full_script

# CLI test
if __name__ == "__main__":
    generator = ScriptGenerator(max_words_per_video=300)

    test_story = """After 4 years and a wedding, my partner left me for a guy on Discord.

I met my partner 4 years ago. Red flags were everywhere, but I ignored them thinking I could change her. We bought a condo together, got a dog, and built a life.

From January to April 2025, I took a second job to cover wedding expenses. She met someone through Discord and emotionally cheated on me.

April 2025, I return from my bachelor trip. She confesses she's having cold feet. I ask if she wants to break up or work on it—she chooses the latter.

October 2025, she takes a solo trip to Chicago. Turns out she's staying with this guy's family. By December, she's distancing herself more.

January 2026, I find lingerie in her luggage—proof of her cheating. She's been planning a future with him.

Now, I'm sitting here with my dog, starting the healing process."""

    script = generator.generate_script(test_story, "My partner left me")
    print("=== GENERATED SCRIPT ===")
    print(script)
    print(f"\nWord count: {len(script.split())}")
