"""Download free background videos from Pexels."""

import requests
from pathlib import Path

# Free background video URLs from Pexels (no API key needed for these direct links)
BACKGROUND_VIDEOS = [
    {
        "name": "minecraft_parkour_01.mp4",
        "url": "https://player.vimeo.com/external/396304398.hd.mp4?s=c94e4f11e7b81f609d1e8e5e8c3b56c8f7a25e1f&profile_id=175",
        "description": "Minecraft parkour gameplay"
    },
    # Add more as we find good free ones
]

def download_video(url: str, output_path: Path) -> bool:
    """Download video from URL.

    Args:
        url: Video URL
        output_path: Path to save video

    Returns:
        True if successful
    """
    try:
        print(f"Downloading {output_path.name}...")

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"✅ Downloaded {output_path.name} ({file_size_mb:.1f}MB)")
        return True

    except Exception as e:
        print(f"❌ Failed to download {output_path.name}: {e}")
        return False

def main():
    """Download all background videos."""
    # Create backgrounds directory
    backgrounds_dir = Path(__file__).parent.parent / "assets" / "backgrounds"
    backgrounds_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading background videos to: {backgrounds_dir}\n")

    success_count = 0

    for video in BACKGROUND_VIDEOS:
        output_path = backgrounds_dir / video["name"]

        if output_path.exists():
            print(f"⏭️  Skipping {video['name']} (already exists)")
            success_count += 1
            continue

        if download_video(video["url"], output_path):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"Downloaded {success_count}/{len(BACKGROUND_VIDEOS)} videos")
    print(f"{'='*60}")

    if success_count < len(BACKGROUND_VIDEOS):
        print("\n⚠️  Some downloads failed. You can manually download from:")
        print("https://www.pexels.com/search/videos/minecraft%20parkour/")
        print("https://www.pexels.com/search/videos/subway%20surfer/")
        print(f"\nSave videos to: {backgrounds_dir}")
    else:
        print("\n✅ All background videos ready!")

if __name__ == "__main__":
    main()
