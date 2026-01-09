"""
Database utilities for Claude Code Coach
Ported from Deep_Me4 app_minimal.py
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import html
import re
import sys

from .platform_utils import get_default_db_path
from .database_history import DatabaseHistory


def _get_schema_file_path() -> Path:
    """Get path to schema file (handles both dev and packaged apps)"""
    import platform

    # Check if running as packaged app
    is_packaged = False
    if getattr(sys, 'frozen', False):
        is_packaged = True
    elif platform.system() == "Darwin":
        exe_path = Path(sys.executable)
        # Only consider it packaged if it's specifically in ClaudeCodeCoach.app
        is_packaged = any(p == 'ClaudeCodeCoach.app' for p in exe_path.parts)
    else:
        is_packaged = False

    if is_packaged:
        # Packaged app - schema is in bundled assets
        # On macOS: Claude Code Coach.app/Contents/Resources/flutter_assets/assets/
        if platform.system() == "Darwin":
            # Navigate from executable to assets directory in bundle
            exe_path = Path(sys.executable)
            # Find the .app directory
            app_path = None
            for i, part in enumerate(exe_path.parts):
                if part.endswith('.app'):
                    app_path = Path(*exe_path.parts[:i+1])
                    break
            if app_path:
                schema_path = app_path / "Contents" / "Resources" / "flutter_assets" / "assets" / "coach_schema.sql"
                if schema_path.exists():
                    return schema_path
        # Fallback for other platforms or if path detection fails
        # Try relative to executable
        schema_path = Path(sys.executable).parent / "assets" / "coach_schema.sql"
        if schema_path.exists():
            return schema_path

    # Development mode - look in project assets directory
    project_root = Path(__file__).parent.parent
    schema_path = project_root / "assets" / "coach_schema.sql"
    if schema_path.exists():
        return schema_path

    # Fallback to old location (for backwards compatibility)
    return project_root / "coach_schema.sql"


def initialize_database_schema() -> bool:
    """
    Initialize database schema from coach_schema.sql

    Returns:
        True if schema was initialized, False if already exists
    """
    db_path = get_default_db_path()
    conn = sqlite3.connect(str(db_path), timeout=30.0)

    try:
        # Check if schema already exists by looking for topics table
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='topics'")
        if cursor.fetchone():
            print("✓ Database schema already exists")
            return False

        # Read and execute schema SQL
        schema_file = _get_schema_file_path()
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_file}")

        print(f"📊 Initializing database schema from {schema_file.name}...")
        with open(schema_file, 'r') as f:
            schema_sql = f.read()

        # Execute schema creation
        conn.executescript(schema_sql)
        conn.commit()

        # Initialize database history tracking
        history = DatabaseHistory(conn)
        print("✅ Database schema initialized successfully")
        print("✅ Database history tracking initialized")

        return True

    except Exception as e:
        print(f"❌ Error initializing database schema: {e}")
        raise
    finally:
        conn.close()


def get_database_stats() -> dict:
    """
    Get database statistics including size, row counts, and FTS index info

    Returns:
        Dictionary with database statistics
    """
    db_path = get_default_db_path()

    stats = {
        'db_size': db_path.stat().st_size if db_path.exists() else 0,
        'content_count': 0,
        'fts_indexed_count': 0,
        'email_count': 0,
        'file_count': 0,
        'page_count': 0,
        'page_size': 0,
    }

    try:
        conn = get_db()
        cursor = conn.cursor()

        # Get page count and size for database size info
        cursor.execute("PRAGMA page_count")
        stats['page_count'] = cursor.fetchone()[0]

        cursor.execute("PRAGMA page_size")
        stats['page_size'] = cursor.fetchone()[0]

        # Get content counts
        cursor.execute("SELECT COUNT(*) FROM content")
        stats['content_count'] = cursor.fetchone()[0]

        # Get FTS indexed count - query content_fts directly for accuracy
        cursor.execute("SELECT COUNT(*) FROM content_fts")
        stats['fts_indexed_count'] = cursor.fetchone()[0]

        # Get email count
        cursor.execute("SELECT COUNT(*) FROM emails")
        stats['email_count'] = cursor.fetchone()[0]

        # Get local file count
        cursor.execute("SELECT COUNT(*) FROM content WHERE source_type = 'local_file'")
        stats['file_count'] = cursor.fetchone()[0]

        conn.close()

    except Exception as e:
        print(f"⚠️ Error getting database stats: {e}")

    return stats


def get_db() -> sqlite3.Connection:
    """Get database connection with WAL mode for better concurrency"""
    db_path = get_default_db_path()

    # SQLite will create the database file if it doesn't exist
    # Set timeout to 30 seconds to handle concurrent access
    conn = sqlite3.connect(str(db_path), timeout=30.0)
    conn.row_factory = sqlite3.Row

    # Enable WAL (Write-Ahead Logging) for concurrent reads/writes
    # This allows multiple readers and one writer simultaneously
    conn.execute('PRAGMA journal_mode=WAL')

    return conn


def get_db_history(conn: sqlite3.Connection = None) -> DatabaseHistory:
    """
    Get DatabaseHistory instance for tracking database operations

    Args:
        conn: Optional database connection. If not provided, creates new connection.

    Returns:
        DatabaseHistory instance
    """
    if conn is None:
        conn = get_db()

    return DatabaseHistory(conn)


def format_date(timestamp) -> str:
    """Format unix timestamp to readable date"""
    if timestamp:
        try:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        except:
            return str(timestamp)
    return 'Unknown'


def format_datetime(timestamp) -> str:
    """Format unix timestamp to readable datetime"""
    if timestamp:
        try:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        except:
            return str(timestamp)
    return 'Unknown'


def format_size(size_bytes) -> str:
    """Format bytes to human readable size"""
    if not size_bytes:
        return "0 B"

    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def clean_email_body(text: str) -> str:
    """Clean HTML/CSS markup from email body text"""
    if not text:
        return text

    # Decode HTML entities
    text = html.unescape(text)

    # Remove CSS style blocks
    text = re.sub(r'[vow]\\:\*\s*\{[^}]+\}', '', text)
    text = re.sub(r'\.shape\s*\{[^}]+\}', '', text)
    text = re.sub(r'@font-face\s*\{[^}]+\}', '', text)
    text = re.sub(r'@page\s+\w+\s*\{[^}]+\}', '', text)
    text = re.sub(r'p\.\w+,\s*li\.\w+,\s*div\.\w+\s*\{[^}]+\}', '', text)
    text = re.sub(r'a:link,\s*span\.\w+\s*\{[^}]+\}', '', text)
    text = re.sub(r'span\.\w+\s*\{[^}]+\}', '', text)
    text = re.sub(r'\.\w+\s*\{[^}]+\}', '', text)
    text = re.sub(r'div\.\w+\s*\{[^}]+\}', '', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Clean up excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()


def get_email_details(content_id: str, conn: sqlite3.Connection) -> dict:
    """Get full email details for display"""
    cursor = conn.cursor()

    # Get email metadata
    cursor.execute("""
        SELECT e.subject, e.from_email, e.from_name,
               c.created_date, e.attachment_count
        FROM emails e
        JOIN content c ON e.content_id = c.id
        WHERE e.content_id = ?
    """, (content_id,))
    email = cursor.fetchone()

    if not email:
        return None

    # Get recipients
    cursor.execute("""
        SELECT email, name
        FROM content_participants
        WHERE content_id = ? AND role = 'participant'
        ORDER BY email
    """, (content_id,))
    recipients = cursor.fetchall()

    # Get email body
    cursor.execute("""
        SELECT body_plain, body_html FROM email_bodies WHERE content_id = ?
    """, (content_id,))
    body_row = cursor.fetchone()

    cursor.execute("""
        SELECT full_text, search_text FROM content_text WHERE content_id = ?
    """, (content_id,))
    text_row = cursor.fetchone()

    # Get attachments
    cursor.execute("""
        SELECT filename, size_bytes
        FROM email_attachments
        WHERE email_content_id = ?
    """, (content_id,))
    attachments = cursor.fetchall()

    # Determine body text
    body_text = None
    if body_row and body_row['body_plain']:
        body_text = clean_email_body(body_row['body_plain'])
    elif text_row and text_row['full_text']:
        body_text = clean_email_body(text_row['full_text'])
    elif text_row and text_row['search_text']:
        body_text = clean_email_body(text_row['search_text'])
    elif body_row and body_row['body_html']:
        body_text = clean_email_body(body_row['body_html'])

    return {
        'subject': email['subject'],
        'from_email': email['from_email'],
        'from_name': email['from_name'],
        'created_date': email['created_date'],
        'attachment_count': email['attachment_count'],
        'recipients': [dict(r) for r in recipients],
        'attachments': [dict(a) for a in attachments],
        'body_text': body_text or "No email body found"
    }


def get_document_details(content_id: str, conn: sqlite3.Connection) -> dict:
    """Get full document details for display"""
    cursor = conn.cursor()

    # Get document metadata
    cursor.execute("""
        SELECT c.id, c.title, c.content_class, c.content_subtype,
               c.created_date, c.size_bytes, c.source_type, c.source_id
        FROM content c
        WHERE c.id = ?
    """, (content_id,))
    doc = cursor.fetchone()

    if not doc:
        return None

    # Get document text content
    cursor.execute("""
        SELECT full_text, search_text FROM content_text WHERE content_id = ?
    """, (content_id,))
    text_row = cursor.fetchone()

    # Get the best available text
    content_text = None
    if text_row and text_row['full_text']:
        content_text = text_row['full_text']
    elif text_row and text_row['search_text']:
        content_text = text_row['search_text']

    # Get file path
    file_path = None
    if doc['source_type'] == 'local_file' and doc['source_id']:
        file_path = doc['source_id']
    elif doc['source_type'] in ('pst', 'gmail', 'email'):
        # For email attachments, check if this is an attachment
        cursor.execute("""
            SELECT file_path FROM email_attachments
            WHERE content_id = ?
            LIMIT 1
        """, (content_id,))
        attachment_row = cursor.fetchone()
        if attachment_row and attachment_row['file_path']:
            file_path = attachment_row['file_path']

    return {
        'id': doc['id'],
        'title': doc['title'],
        'content_class': doc['content_class'],
        'content_subtype': doc['content_subtype'],
        'created_date': doc['created_date'],
        'size_bytes': doc['size_bytes'],
        'source_type': doc['source_type'],
        'file_path': file_path,
        'content_text': content_text
    }
