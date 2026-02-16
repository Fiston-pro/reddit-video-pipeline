-- Automated Reddit-to-Social-Media Video Pipeline
-- Supabase PostgreSQL Database Setup
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- STORIES TABLE
-- Stores scraped Reddit stories with virality metrics
-- ============================================================================
CREATE TABLE IF NOT EXISTS stories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reddit_id VARCHAR(20) UNIQUE NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    author VARCHAR(100),
    created_utc TIMESTAMP NOT NULL,
    upvotes INT DEFAULT 0,
    comments INT DEFAULT 0,
    upvote_ratio FLOAT DEFAULT 0,
    awards INT DEFAULT 0,
    virality_score FLOAT DEFAULT 0,
    sentiment_score FLOAT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'scraped',
    scraped_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT valid_status CHECK (status IN ('scraped', 'selected', 'processed', 'rejected'))
);

-- Indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_stories_status ON stories(status);
CREATE INDEX IF NOT EXISTS idx_stories_virality_score ON stories(virality_score DESC);
CREATE INDEX IF NOT EXISTS idx_stories_scraped_at ON stories(scraped_at DESC);

-- ============================================================================
-- VIDEOS TABLE
-- Stores generated videos with approval status
-- ============================================================================
CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    story_id UUID REFERENCES stories(id) ON DELETE CASCADE,
    video_url TEXT NOT NULL,
    local_path TEXT,
    duration FLOAT,
    file_size_mb FLOAT,
    status VARCHAR(50) DEFAULT 'pending_approval',
    approved_at TIMESTAMP,
    approved_by VARCHAR(100),
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT valid_status CHECK (status IN ('pending_approval', 'approved', 'rejected'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_videos_status ON videos(status);
CREATE INDEX IF NOT EXISTS idx_videos_story_id ON videos(story_id);
CREATE INDEX IF NOT EXISTS idx_videos_created_at ON videos(created_at DESC);

-- ============================================================================
-- PLATFORM_POSTS TABLE
-- Tracks uploads to each social media platform
-- ============================================================================
CREATE TABLE IF NOT EXISTS platform_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    post_id VARCHAR(100),
    post_url TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    published_at TIMESTAMP,
    error_message TEXT,
    retry_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT valid_platform CHECK (platform IN ('youtube', 'instagram', 'tiktok')),
    CONSTRAINT valid_status CHECK (status IN ('pending', 'published', 'failed'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_platform_posts_video_id ON platform_posts(video_id);
CREATE INDEX IF NOT EXISTS idx_platform_posts_platform ON platform_posts(platform);
CREATE INDEX IF NOT EXISTS idx_platform_posts_status ON platform_posts(status);

-- ============================================================================
-- PLATFORM_METRICS TABLE
-- Stores performance metrics from each platform
-- ============================================================================
CREATE TABLE IF NOT EXISTS platform_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    post_id UUID REFERENCES platform_posts(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    comments INT DEFAULT 0,
    shares INT DEFAULT 0,
    saves INT DEFAULT 0,
    watch_time_minutes FLOAT DEFAULT 0,
    engagement_rate FLOAT DEFAULT 0,
    recorded_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT valid_platform CHECK (platform IN ('youtube', 'instagram', 'tiktok'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_platform_metrics_post_id ON platform_metrics(post_id);
CREATE INDEX IF NOT EXISTS idx_platform_metrics_recorded_at ON platform_metrics(recorded_at DESC);

-- ============================================================================
-- UPLOAD_ERRORS TABLE
-- Logs upload failures for debugging
-- ============================================================================
CREATE TABLE IF NOT EXISTS upload_errors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    platform VARCHAR(50),
    error_type VARCHAR(100),
    error_message TEXT,
    stack_trace TEXT,
    retry_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_upload_errors_video_id ON upload_errors(video_id);
CREATE INDEX IF NOT EXISTS idx_upload_errors_created_at ON upload_errors(created_at DESC);

-- ============================================================================
-- VIEWS FOR ANALYTICS
-- ============================================================================

-- View: Top performing videos across all platforms
CREATE OR REPLACE VIEW top_performing_videos AS
SELECT
    v.id as video_id,
    s.title as story_title,
    s.virality_score,
    v.duration,
    v.created_at,
    COUNT(DISTINCT pp.platform) as platforms_posted,
    SUM(pm.views) as total_views,
    SUM(pm.likes) as total_likes,
    SUM(pm.comments) as total_comments,
    SUM(pm.shares) as total_shares,
    AVG(pm.engagement_rate) as avg_engagement_rate
FROM videos v
JOIN stories s ON v.story_id = s.id
LEFT JOIN platform_posts pp ON v.id = pp.video_id
LEFT JOIN platform_metrics pm ON pp.id = pm.post_id
WHERE v.status = 'approved' AND pp.status = 'published'
GROUP BY v.id, s.title, s.virality_score, v.duration, v.created_at
ORDER BY total_views DESC;

-- View: Platform performance comparison
CREATE OR REPLACE VIEW platform_performance AS
SELECT
    platform,
    COUNT(*) as total_posts,
    AVG(views) as avg_views,
    AVG(likes) as avg_likes,
    AVG(comments) as avg_comments,
    AVG(shares) as avg_shares,
    AVG(engagement_rate) as avg_engagement_rate,
    MAX(views) as max_views,
    SUM(views) as total_views
FROM platform_metrics
GROUP BY platform
ORDER BY total_views DESC;

-- View: Daily pipeline status
CREATE OR REPLACE VIEW daily_pipeline_status AS
SELECT
    DATE(scraped_at) as date,
    COUNT(*) as stories_scraped,
    SUM(CASE WHEN status = 'selected' THEN 1 ELSE 0 END) as stories_selected,
    SUM(CASE WHEN virality_score > 50 THEN 1 ELSE 0 END) as high_virality_stories
FROM stories
GROUP BY DATE(scraped_at)
ORDER BY date DESC;

-- ============================================================================
-- SAMPLE DATA (Optional - for testing)
-- ============================================================================
/*
INSERT INTO stories (reddit_id, title, body, author, created_utc, upvotes, comments, upvote_ratio, virality_score, status)
VALUES (
    'test123',
    'Test Story - My Wife Cheated',
    'This is a test story body with enough content to be processed...',
    'test_user',
    NOW() - INTERVAL '2 hours',
    500,
    45,
    0.95,
    75.5,
    'scraped'
);
*/

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'Database setup complete!';
    RAISE NOTICE 'Tables created: stories, videos, platform_posts, platform_metrics, upload_errors';
    RAISE NOTICE 'Views created: top_performing_videos, platform_performance, daily_pipeline_status';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '1. Copy your Supabase URL and anon key to .env file';
    RAISE NOTICE '2. Test connection with: python src/database/supabase_client.py';
END $$;
