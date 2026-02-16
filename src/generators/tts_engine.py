"""Text-to-Speech engine using gTTS (Google TTS) with edge-tts fallback."""

import asyncio
from pathlib import Path
from typing import Optional
from gtts import gTTS
import edge_tts
from src.utils.logger import get_logger
from src.utils.config_loader import config

logger = get_logger(__name__)

class TTSEngine:
    """Generate voiceovers using gTTS (primary) and edge-tts (fallback)."""

    def __init__(self):
        """Initialize TTS engine."""
        self.engine = "gtts"  # Use gTTS by default since edge-tts is blocked
        self.voice = config.get("tts.voice", "en-US-AriaNeural")
        self.fallback_voice = config.get("tts.fallback_voice", "en-US-GuyNeural")
        logger.info(f"TTS engine initialized (using gTTS)")

    def generate_with_gtts(self, text: str, output_path: str) -> bool:
        """Generate TTS using Google TTS.

        Args:
            text: Text to convert to speech
            output_path: Path to save MP3 file

        Returns:
            True if successful
        """
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            logger.info(f"Generated TTS audio with gTTS: {output_path}")
            return True
        except Exception as e:
            logger.error(f"gTTS generation failed: {e}")
            return False

    async def generate_async(self, text: str, output_path: str) -> bool:
        """Generate TTS audio asynchronously (tries gTTS first, then edge-tts).

        Args:
            text: Text to convert to speech
            output_path: Path to save MP3 file

        Returns:
            True if successful
        """
        # Try gTTS first (synchronous, so we run it directly)
        if self.generate_with_gtts(text, output_path):
            return True

        # If gTTS fails, try edge-tts as fallback
        logger.info("Trying edge-tts as fallback...")
        try:
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(output_path)
            logger.info(f"Generated TTS audio with edge-tts: {output_path}")
            return True
        except Exception as e:
            logger.error(f"edge-tts generation failed: {e}")
            return False

    def generate(self, text: str, output_path: str) -> bool:
        """Generate TTS audio (synchronous wrapper).

        Args:
            text: Text to convert to speech
            output_path: Path to save MP3 file

        Returns:
            True if successful
        """
        # For synchronous calls, just use gTTS directly
        return self.generate_with_gtts(text, output_path)

    async def list_voices_async(self) -> list:
        """List available voices asynchronously.

        Returns:
            List of available voice names
        """
        voices = await edge_tts.list_voices()
        return [v["Name"] for v in voices if v["Locale"].startswith("en")]

    def list_voices(self) -> list:
        """List available English voices (synchronous wrapper).

        Returns:
            List of available voice names
        """
        return asyncio.run(self.list_voices_async())

# Test if run directly
if __name__ == "__main__":
    import sys

    tts = TTSEngine()

    if "--list-voices" in sys.argv:
        print("Available English voices:")
        voices = tts.list_voices()
        for voice in voices[:10]:  # Show first 10
            print(f"  - {voice}")
        print(f"\n({len(voices)} total voices available)")
    else:
        # Test TTS generation
        test_text = "This is a test of the text to speech engine. If you can hear this clearly, it is working correctly."
        output = "test_voiceover.mp3"

        print(f"Generating TTS with voice: {tts.voice}")
        success = tts.generate(test_text, output)

        if success:
            print(f"✅ TTS generated successfully: {output}")
            print(f"Play the file to test audio quality.")
        else:
            print("❌ TTS generation failed")
