-- Claude Code Coach Database Schema
-- SQLite database for knowledge base and application data

-- Knowledge Base Topics
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    summary TEXT NOT NULL,
    content TEXT NOT NULL,
    commands TEXT,              -- JSON array: ["/model", "Shift+Tab"]
    keywords TEXT,              -- Space-separated boost terms
    related_topics TEXT,        -- JSON array: ["slug1", "slug2"]
    difficulty TEXT DEFAULT 'intermediate',  -- beginner, intermediate, advanced
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FTS5 Virtual Table for full-text search
CREATE VIRTUAL TABLE IF NOT EXISTS topics_fts USING fts5(
    title,
    summary,
    content,
    keywords,
    content='topics',
    content_rowid='id',
    tokenize='porter unicode61'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS topics_ai AFTER INSERT ON topics BEGIN
    INSERT INTO topics_fts(rowid, title, summary, content, keywords)
    VALUES (new.id, new.title, new.summary, new.content, new.keywords);
END;

CREATE TRIGGER IF NOT EXISTS topics_ad AFTER DELETE ON topics BEGIN
    INSERT INTO topics_fts(topics_fts, rowid, title, summary, content, keywords)
    VALUES('delete', old.id, old.title, old.summary, old.content, old.keywords);
END;

CREATE TRIGGER IF NOT EXISTS topics_au AFTER UPDATE ON topics BEGIN
    INSERT INTO topics_fts(topics_fts, rowid, title, summary, content, keywords)
    VALUES('delete', old.id, old.title, old.summary, old.content, old.keywords);
    INSERT INTO topics_fts(rowid, title, summary, content, keywords)
    VALUES (new.id, new.title, new.summary, new.content, new.keywords);
END;

-- Link health issues to knowledge topics
CREATE TABLE IF NOT EXISTS issue_topic_links (
    issue_rule_id TEXT NOT NULL,
    topic_slug TEXT NOT NULL,
    PRIMARY KEY (issue_rule_id, topic_slug),
    FOREIGN KEY (topic_slug) REFERENCES topics(slug)
);

-- Categories for organization
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    sort_order INTEGER DEFAULT 0
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_topics_category ON topics(category);
CREATE INDEX IF NOT EXISTS idx_topics_slug ON topics(slug);
CREATE INDEX IF NOT EXISTS idx_categories_sort ON categories(sort_order);
