"""AI-powered script enhancer using Claude Haiku for viral TikTok scripts."""

import os
from typing import Dict
from anthropic import Anthropic
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AIScriptEnhancer:
    """Enhance scripts using Claude Haiku for maximum virality."""

    def __init__(self):
        """Initialize AI script enhancer."""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not found - AI enhancement disabled")
            self.client = None
        else:
            self.client = Anthropic(api_key=self.api_key)
            logger.info("AI Script Enhancer initialized with Claude Haiku")

    def enhance_script(self, raw_script: str, story_title: str = "") -> str:
        """Enhance a script using AI to make it more viral.

        Args:
            raw_script: The basic script from script_generator
            story_title: Story title for context

        Returns:
            Enhanced script optimized for TikTok/Shorts virality
        """
        if not self.client:
            logger.info("AI enhancement disabled - returning original script")
            return raw_script

        try:
            prompt = f"""You are a viral TikTok script writer. Transform this Reddit story into an engaging short-form video script.

ORIGINAL SCRIPT:
{raw_script}

YOUR TASK:
1. Create a POWERFUL hook in the first 3 seconds that makes people STOP scrolling
2. Use dramatic pacing - short punchy sentences for impact
3. Add natural pauses (use "..." for dramatic effect)
4. Build tension and emotional peaks
5. Use conversational language (contractions, informal tone)
6. End with a cliffhanger if this is part 1 of a series
7. Keep it under 300 words
8. Make it BINGE-WORTHY - people should NEED to know what happens next

RULES:
- NO meta-commentary ("let me tell you", "this is crazy")
- Start IMMEDIATELY with the hook
- Use first-person perspective
- Sound natural, like you're telling a friend
- Short sentences for TTS clarity
- Emotional, raw, authentic

OUTPUT ONLY THE ENHANCED SCRIPT - NO EXPLANATIONS."""

            response = self.client.messages.create(
                model="claude-haiku-4-5-20251001",  # Updated to correct model name
                max_tokens=500,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            enhanced = response.content[0].text.strip()

            logger.info(f"Script enhanced by AI ({len(raw_script.split())} -> {len(enhanced.split())} words)")
            logger.info(f"API cost: ${response.usage.input_tokens * 0.0000008 + response.usage.output_tokens * 0.000004:.4f}")

            return enhanced

        except Exception as e:
            logger.error(f"AI enhancement failed: {e}")
            logger.info("Falling back to original script")
            return raw_script

    def generate_hook_options(self, story: str, count: int = 3) -> list:
        """Generate multiple hook options and pick the best.

        Args:
            story: Full story text
            count: Number of hook options to generate

        Returns:
            List of hook options, best first
        """
        if not self.client:
            return []

        try:
            prompt = f"""Generate {count} different VIRAL hooks for this story. Each hook should:
- Be 1-2 sentences max
- Make people STOP scrolling
- Create curiosity/shock/emotion
- Work in first 3 seconds of video

STORY:
{story[:500]}

OUTPUT FORMAT (one per line):
1. [hook]
2. [hook]
3. [hook]"""

            response = self.client.messages.create(
                model="claude-haiku-4.5-20250929",
                max_tokens=300,
                temperature=0.9,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            hooks_text = response.content[0].text.strip()
            hooks = [line.split(". ", 1)[1] if ". " in line else line
                    for line in hooks_text.split("\n") if line.strip()]

            logger.info(f"Generated {len(hooks)} hook options")
            return hooks

        except Exception as e:
            logger.error(f"Hook generation failed: {e}")
            return []

# CLI test
if __name__ == "__main__":
    import sys
    from pathlib import Path
    from dotenv import load_dotenv

    # Add parent directory to path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    # Load environment variables
    load_dotenv()

    enhancer = AIScriptEnhancer()

    test_script = """After all this time... After 4 years and a wedding, my partner left me for a guy on Discord.

I met my partner 4 years ago. Red flags were everywhere, but I ignored them thinking I could change her. We bought a condo together, got a dog, and built a life.

From January to April 2025, I took a second job to cover wedding expenses. She met someone through Discord and emotionally cheated on me."""

    print("=== ORIGINAL SCRIPT ===")
    print(test_script)
    print(f"\nWord count: {len(test_script.split())}")

    print("\n" + "=" * 60)
    print("ENHANCING WITH AI...")
    print("=" * 60)

    enhanced = enhancer.enhance_script(test_script)

    print("\n=== AI-ENHANCED SCRIPT ===")
    print(enhanced)
    print(f"\nWord count: {len(enhanced.split())}")

    print("\n" + "=" * 60)
    print("GENERATING HOOK OPTIONS...")
    print("=" * 60)

    hooks = enhancer.generate_hook_options(test_script)
    for i, hook in enumerate(hooks, 1):
        print(f"{i}. {hook}")
