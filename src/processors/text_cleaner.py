"""Text cleaning utilities for preparing Reddit stories for TTS."""

import re
from typing import Dict
from src.utils.logger import get_logger

logger = get_logger(__name__)

def clean_reddit_markdown(text: str) -> str:
    """Remove Reddit markdown formatting.

    Args:
        text: Raw Reddit post text

    Returns:
        Cleaned text without markdown
    """
    # Remove bold (**text**)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)

    # Remove italic (*text*)
    text = re.sub(r'\*(.+?)\*', r'\1', text)

    # Remove strikethrough (~~text~~)
    text = re.sub(r'~~(.+?)~~', r'\1', text)

    # Remove inline code (`code`)
    text = re.sub(r'`(.+?)`', r'\1', text)

    # Remove links [text](url)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)

    # Remove quotes (> text)
    text = re.sub(r'>\s?.+', '', text)

    # Remove headers (# Header)
    text = re.sub(r'#+\s+', '', text)

    return text

def fix_formatting_for_tts(text: str) -> str:
    """Fix text formatting for better TTS pronunciation.

    Args:
        text: Cleaned text

    Returns:
        TTS-optimized text
    """
    # Expand common contractions
    contractions = {
        "don't": "do not",
        "can't": "cannot",
        "won't": "will not",
        "it's": "it is",
        "i'm": "i am",
        "you're": "you are",
        "he's": "he is",
        "she's": "she is",
        "we're": "we are",
        "they're": "they are",
        "i've": "i have",
        "you've": "you have",
        "we've": "we have",
        "they've": "they have",
        "i'd": "i would",
        "you'd": "you would",
        "he'd": "he would",
        "she'd": "she would",
        "we'd": "we would",
        "they'd": "they would",
        "i'll": "i will",
        "you'll": "you will",
        "he'll": "he will",
        "she'll": "she will",
        "we'll": "we will",
        "they'll": "they will",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "hasn't": "has not",
        "haven't": "have not",
        "hadn't": "had not",
        "doesn't": "does not",
        "didn't": "did not",
        "couldn't": "could not",
        "shouldn't": "should not",
        "wouldn't": "would not",
        "mightn't": "might not",
        "mustn't": "must not",
    }

    for contraction, expansion in contractions.items():
        # Case-insensitive replacement
        pattern = re.compile(re.escape(contraction), re.IGNORECASE)
        text = pattern.sub(expansion, text)

    # Replace newlines with periods (adds pauses in TTS)
    text = re.sub(r'\n\n+', '. ', text)
    text = re.sub(r'\n', ' ', text)

    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)

    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Fix multiple punctuation
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'!{2,}', '!', text)
    text = re.sub(r'\?{2,}', '?', text)

    # Remove special characters that TTS struggles with
    text = re.sub(r'[^\w\s.,!?;\'-]', '', text)

    return text.strip()

def clean_story_for_video(title: str, body: str) -> Dict[str, str]:
    """Clean and prepare story for video creation.

    Args:
        title: Reddit post title
        body: Reddit post body

    Returns:
        Dictionary with cleaned title and body
    """
    # Clean markdown
    clean_title = clean_reddit_markdown(title)
    clean_body = clean_reddit_markdown(body)

    # Fix formatting for TTS
    tts_title = fix_formatting_for_tts(clean_title)
    tts_body = fix_formatting_for_tts(clean_body)

    # Combine title and body with separator
    full_text = f"{tts_title}. {tts_body}"

    logger.debug(f"Cleaned story: {len(full_text)} characters")

    return {
        "title": tts_title,
        "body": tts_body,
        "full_text": full_text,
        "word_count": len(full_text.split()),
        "char_count": len(full_text)
    }

__all__ = ["clean_reddit_markdown", "fix_formatting_for_tts", "clean_story_for_video"]
