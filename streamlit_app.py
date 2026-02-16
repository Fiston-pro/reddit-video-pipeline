"""Streamlit Dashboard for Video Approval (Vercel-compatible)."""

import os
import streamlit as st
from datetime import datetime

# Vercel doesn't need load_dotenv - environment variables are set directly
# from dotenv import load_dotenv
# load_dotenv()

# Import Supabase only when needed to avoid initialization issues
try:
    from supabase import create_client
except ImportError:
    st.error("Supabase library not installed. Run: pip install supabase")
    st.stop()

# Page config
st.set_page_config(
    page_title="Video Approval Dashboard",
    page_icon="🎬",
    layout="wide"
)

# Initialize Supabase (lazy connection)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

def get_supabase_client():
    """Get Supabase client with error handling."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("⚠️ Missing Supabase credentials!")
        st.info("Add these environment variables in your Vercel dashboard:")
        st.code("""
SUPABASE_URL=https://yourproject.supabase.co
SUPABASE_KEY=your_anon_key
DASHBOARD_PASSWORD=your_password
        """)
        st.stop()

    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"❌ Failed to connect to Supabase: {e}")
        st.info("Check that your Supabase credentials are correct.")
        st.stop()

# Only create client when actually needed (not on module load)
supabase = None

# Simple password protection
def check_password():
    """Simple password check."""
    def password_entered():
        if st.session_state["password"] == os.getenv("DASHBOARD_PASSWORD", "admin123"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Incorrect password")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Sidebar
st.sidebar.title("🎬 Video Dashboard")
page = st.sidebar.radio("Navigation", [
    "📥 Pending Approval",
    "✅ Approved Videos",
    "📊 Analytics",
    "⚙️ Settings"
])

# Helper functions
def get_pending_videos():
    """Get videos pending approval."""
    try:
        # Get Supabase client
        db = get_supabase_client()

        # Join videos with stories to get story details
        response = db.table('videos').select(
            'id, video_url, duration, created_at, status, story_id, '
            'stories(title, virality_score, body, reddit_id)'
        ).eq('status', 'pending_approval').order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching videos: {e}")
        return []

def get_approved_videos():
    """Get approved videos."""
    try:
        db = get_supabase_client()
        response = db.table('videos').select(
            'id, video_url, duration, created_at, approved_at, story_id, '
            'stories(title, virality_score)'
        ).eq('status', 'approved').order('approved_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching videos: {e}")
        return []

def approve_video(video_id):
    """Approve a video."""
    try:
        db = get_supabase_client()
        db.table('videos').update({
            'status': 'approved',
            'approved_at': datetime.now().isoformat()
        }).eq('id', video_id).execute()
        st.success("Video approved!")
        st.rerun()
    except Exception as e:
        st.error(f"Error approving video: {e}")

def reject_video(video_id):
    """Reject a video."""
    try:
        db = get_supabase_client()
        db.table('videos').update({
            'status': 'rejected'
        }).eq('id', video_id).execute()
        st.success("Video rejected!")
        st.rerun()
    except Exception as e:
        st.error(f"Error rejecting video: {e}")

# PAGE 1: Pending Approval
if page == "📥 Pending Approval":
    st.title("📥 Videos Pending Approval")

    videos = get_pending_videos()

    if not videos:
        st.info("No videos pending approval. Run the video generator to create new videos!")
    else:
        st.write(f"**{len(videos)} video(s) awaiting your review**")
        st.write("---")

        for video in videos:
            with st.container():
                col1, col2 = st.columns([2, 1])

                with col1:
                    # Video preview
                    st.subheader(f"🎬 {video['stories']['title'][:80]}...")

                    # Show video if URL is available
                    if video.get('video_url'):
                        # For Google Drive links, convert to embeddable format
                        video_url = video['video_url']
                        if 'drive.google.com' in video_url:
                            # Convert Google Drive link to direct playback
                            file_id = video_url.split('/d/')[1].split('/')[0] if '/d/' in video_url else None
                            if file_id:
                                video_url = f"https://drive.google.com/uc?export=download&id={file_id}"

                        try:
                            st.video(video_url)
                        except Exception as e:
                            st.warning(f"Could not load video preview. URL: {video['video_url']}")
                            st.caption(f"Error: {e}")
                    else:
                        st.warning("Video URL not available")

                    # Story preview (first 300 chars)
                    with st.expander("📖 View Story"):
                        st.write(video['stories']['body'][:500] + "..." if len(video['stories']['body']) > 500 else video['stories']['body'])

                with col2:
                    st.metric("Virality Score", f"{video['stories']['virality_score']:.1f}")
                    st.metric("Duration", f"{video.get('duration', 0):.1f}s")
                    st.caption(f"Created: {video['created_at'][:10]}")
                    st.caption(f"Reddit ID: {video['stories']['reddit_id']}")

                    st.write("")

                    # Action buttons
                    col_approve, col_reject = st.columns(2)
                    with col_approve:
                        if st.button("✅ Approve", key=f"approve_{video['id']}", use_container_width=True):
                            approve_video(video['id'])
                    with col_reject:
                        if st.button("❌ Reject", key=f"reject_{video['id']}", use_container_width=True):
                            reject_video(video['id'])

                st.write("---")

# PAGE 2: Approved Videos
elif page == "✅ Approved Videos":
    st.title("✅ Approved Videos")

    videos = get_approved_videos()

    if not videos:
        st.info("No approved videos yet. Approve some videos from the Pending Approval page!")
    else:
        st.write(f"**{len(videos)} approved video(s) ready for upload**")
        st.write("---")

        for video in videos:
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(f"**{video['stories']['title'][:60]}...**")
            with col2:
                st.caption(f"Approved: {video['approved_at'][:10] if video.get('approved_at') else 'N/A'}")
            with col3:
                # Check if already uploaded
                try:
                    db = get_supabase_client()
                    posts = db.table('platform_posts').select('platform, status').eq('video_id', video['id']).execute()
                    if posts.data:
                        platforms = [p['platform'] for p in posts.data if p['status'] == 'published']
                        if platforms:
                            st.success(f"Posted: {', '.join(platforms)}")
                        else:
                            st.info("Ready to upload")
                    else:
                        st.info("Ready to upload")
                except:
                    st.info("Ready to upload")

# PAGE 3: Analytics
elif page == "📊 Analytics":
    st.title("📊 Analytics Dashboard")

    # Get metrics
    try:
        db = get_supabase_client()
        total_stories = db.table('stories').select('id', count='exact').execute()
        total_videos = db.table('videos').select('id', count='exact').execute()
        approved_videos = db.table('videos').select('id', count='exact').eq('status', 'approved').execute()
        pending_videos = db.table('videos').select('id', count='exact').eq('status', 'pending_approval').execute()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Stories", total_stories.count if total_stories.count else 0)
        with col2:
            st.metric("Total Videos", total_videos.count if total_videos.count else 0)
        with col3:
            st.metric("Approved", approved_videos.count if approved_videos.count else 0)
        with col4:
            st.metric("Pending", pending_videos.count if pending_videos.count else 0)

        st.write("---")

        # Recent stories
        st.subheader("📈 Recent Stories")
        stories = db.table('stories').select('title, virality_score, created_utc, status').order('created_utc', desc=True).limit(10).execute()

        if stories.data:
            import pandas as pd
            df = pd.DataFrame(stories.data)
            df = df[['title', 'virality_score', 'status', 'created_utc']]
            df.columns = ['Story Title', 'Virality', 'Status', 'Date']
            df['Story Title'] = df['Story Title'].str[:60] + '...'
            df['Virality'] = df['Virality'].round(1)
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error loading analytics: {e}")

# PAGE 4: Settings
elif page == "⚙️ Settings":
    st.title("⚙️ Dashboard Settings")

    st.info("Settings will be implemented in the next phase. For now, you can:")
    st.write("- Configure environment variables in Vercel dashboard")
    st.write("- Update config.yaml in the repository")
    st.write("- Manage API credentials in the .env file")

    st.write("---")
    st.subheader("Environment Status")

    st.write(f"**Supabase URL:** {SUPABASE_URL}")
    st.write(f"**Supabase Key:** {'✅ Set' if SUPABASE_KEY else '❌ Missing'}")
    st.write(f"**Dashboard Password:** {'✅ Set' if os.getenv('DASHBOARD_PASSWORD') else '❌ Using default (admin123)'}")

# Footer
st.sidebar.write("---")
st.sidebar.caption("Built with Streamlit + Vercel")
st.sidebar.caption("Connected to Supabase")
