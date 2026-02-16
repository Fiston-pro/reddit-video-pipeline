"""Quick test of AI script enhancement without full video generation."""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# Test script (basic version)
test_script = """After all this time... After 4 years and a wedding, my partner left me for a guy on Discord.

I met my partner 4 years ago. Red flags were everywhere, but I ignored them thinking I could change her. We bought a condo together, got a dog, and built a life.

From January to April 2025, I took a second job to cover wedding expenses. She met someone through Discord and emotionally cheated on me.

April 2025, I return from my bachelor trip. She confesses she's having cold feet. I ask if she wants to break up or work on it—she chooses the latter.

October 2025, she takes a solo trip to Chicago. Turns out she's staying with this guy's family. By December, she's distancing herself more."""

print("=" * 70)
print("BASIC SCRIPT (from script_generator.py)")
print("=" * 70)
print(test_script)
print(f"\nWord count: {len(test_script.split())}")

print("\n" + "=" * 70)
print("ENHANCING WITH CLAUDE HAIKU AI...")
print("=" * 70)

# Initialize Claude
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# AI enhancement prompt
prompt = f"""You are a viral TikTok script writer. Transform this Reddit story into an engaging short-form video script.

ORIGINAL SCRIPT:
{test_script}

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

try:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Using latest Haiku 4.5 model
        max_tokens=500,
        temperature=0.7,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    enhanced = response.content[0].text.strip()

    print("\n" + "=" * 70)
    print("AI-ENHANCED SCRIPT (Claude Haiku 4)")
    print("=" * 70)
    print(enhanced)
    print(f"\nWord count: {len(enhanced.split())}")

    # Show cost
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    cost = (input_tokens * 0.0000008) + (output_tokens * 0.000004)

    print("\n" + "=" * 70)
    print("AI ENHANCEMENT STATS")
    print("=" * 70)
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Cost: ${cost:.4f} (~{cost * 100:.2f} cents)")
    print(f"\nFor 150 videos/month: ${cost * 150:.2f}/month")

    print("\n" + "=" * 70)
    print("COMPARISON")
    print("=" * 70)
    print("BEFORE: Starts with contextual hook")
    print("AFTER:  Dramatic, punchy, VIRAL hook")
    print("\nThe AI optimizes for:")
    print("  - Scroll-stopping first 3 seconds")
    print("  - Emotional impact and tension")
    print("  - Natural conversational flow")
    print("  - Cliffhangers and binge-worthiness")

except Exception as e:
    print(f"\nERROR: {e}")
    print("\nMake sure ANTHROPIC_API_KEY is set correctly in .env")
