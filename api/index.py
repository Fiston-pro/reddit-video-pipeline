"""Simple Video Dashboard API for Vercel (Flask-based)."""

import os
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Try to import supabase
try:
    from supabase import create_client
except ImportError:
    create_client = None

class handler(BaseHTTPRequestHandler):
    """Handle HTTP requests for Vercel serverless."""

    def do_GET(self):
        """Handle GET requests."""

        # CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Check if Supabase credentials are set
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            self.wfile.write(self._error_page("Missing environment variables").encode())
            return

        if not create_client:
            self.wfile.write(self._error_page("Supabase library not installed").encode())
            return

        try:
            # Connect to Supabase
            supabase = create_client(supabase_url, supabase_key)

            # Get pending videos
            response = supabase.table('videos').select(
                'id, video_url, duration, created_at, status, story_id, '
                'stories(title, virality_score, body, reddit_id)'
            ).eq('status', 'pending_approval').order('created_at', desc=True).limit(10).execute()

            videos = response.data if response.data else []

            # Render HTML
            html = self._render_dashboard(videos)
            self.wfile.write(html.encode())

        except Exception as e:
            self.wfile.write(self._error_page(f"Error: {str(e)}").encode())

    def _render_dashboard(self, videos):
        """Render simple HTML dashboard."""
        videos_html = ""

        if not videos:
            videos_html = "<p>✅ No videos pending approval!</p>"
        else:
            for video in videos:
                story = video.get('stories', {})
                videos_html += f"""
                <div style="border: 1px solid #ddd; padding: 20px; margin: 20px 0; border-radius: 8px;">
                    <h3>🎬 {story.get('title', 'Unknown')[:80]}</h3>
                    <p><strong>Virality Score:</strong> {story.get('virality_score', 0):.1f}</p>
                    <p><strong>Duration:</strong> {video.get('duration', 0):.1f}s</p>
                    <p><strong>Created:</strong> {video.get('created_at', 'N/A')[:10]}</p>
                    <details>
                        <summary>📖 View Story</summary>
                        <p style="margin-top: 10px; padding: 10px; background: #f5f5f5; border-radius: 4px;">
                            {story.get('body', 'No content')[:500]}...
                        </p>
                    </details>
                    <p style="margin-top: 10px;">
                        <a href="/api/approve?id={video['id']}"
                           style="background: #4CAF50; color: white; padding: 10px 20px;
                                  text-decoration: none; border-radius: 4px; display: inline-block; margin-right: 10px;">
                            ✅ Approve
                        </a>
                        <a href="/api/reject?id={video['id']}"
                           style="background: #f44336; color: white; padding: 10px 20px;
                                  text-decoration: none; border-radius: 4px; display: inline-block;">
                            ❌ Reject
                        </a>
                    </p>
                </div>
                """

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Video Approval Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background: #f9f9f9;
                }}
                h1 {{
                    color: #333;
                }}
                .refresh {{
                    float: right;
                    background: #2196F3;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <h1>🎬 Video Approval Dashboard</h1>
            <a href="/" class="refresh">🔄 Refresh</a>
            <div style="clear: both;"></div>
            <hr>
            <h2>📥 Pending Videos ({len(videos)})</h2>
            {videos_html}
            <hr>
            <p style="text-align: center; color: #666;">
                ⚡ Powered by Vercel + Supabase<br>
                <small>Note: Approve/Reject functionality requires API endpoints. This is a read-only view.</small>
            </p>
        </body>
        </html>
        """

    def _error_page(self, error_msg):
        """Render error page."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard Error</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    text-align: center;
                }}
                .error {{
                    background: #ffebee;
                    color: #c62828;
                    padding: 20px;
                    border-radius: 8px;
                    border: 1px solid #ef5350;
                }}
            </style>
        </head>
        <body>
            <h1>⚠️ Dashboard Error</h1>
            <div class="error">
                <p><strong>Error:</strong> {error_msg}</p>
            </div>
            <h3>Required Environment Variables:</h3>
            <pre style="background: #f5f5f5; padding: 15px; border-radius: 4px; text-align: left;">
SUPABASE_URL=https://yourproject.supabase.co
SUPABASE_KEY=your_anon_key
DASHBOARD_PASSWORD=your_password
            </pre>
            <p>Add these in your Vercel dashboard: Settings → Environment Variables</p>
        </body>
        </html>
        """
