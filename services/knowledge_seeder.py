"""
Knowledge Base Seeder
Parses markdown files and populates knowledge base tables
"""

import sqlite3
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

import yaml


def parse_frontmatter(content: str) -> tuple[Optional[Dict[str, Any]], str]:
    """
    Parse YAML frontmatter from markdown content.

    Expected format:
    ---
    title: Topic Title
    category: category-slug
    commands: ["/command", "Ctrl+K"]
    keywords: keyword1 keyword2
    related_topics: [slug1, slug2]
    difficulty: intermediate
    ---
    # Content here

    Args:
        content: Full markdown file content

    Returns:
        Tuple of (frontmatter dict, remaining content)
        If no frontmatter, returns (None, original content)
    """
    # Match YAML frontmatter at start of file
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None, content

    frontmatter_yaml = match.group(1)
    remaining_content = match.group(2)

    try:
        frontmatter = yaml.safe_load(frontmatter_yaml)
        return frontmatter, remaining_content
    except yaml.YAMLError as e:
        print(f"⚠️ Error parsing YAML frontmatter: {e}")
        return None, content


def extract_summary(content: str) -> str:
    """
    Extract summary from markdown content.
    Tries these strategies in order:
    1. Look for ## Summary section
    2. Take first paragraph after title
    3. Take first 200 characters

    Args:
        content: Markdown content (without frontmatter)

    Returns:
        Summary text
    """
    lines = content.strip().split('\n')

    # Strategy 1: Look for ## Summary section
    summary_section = []
    in_summary = False
    for line in lines:
        if line.strip().startswith('## Summary'):
            in_summary = True
            continue
        if in_summary:
            if line.strip().startswith('##'):  # Next section
                break
            if line.strip():
                summary_section.append(line.strip())

    if summary_section:
        return ' '.join(summary_section)

    # Strategy 2: First paragraph after title
    paragraphs = []
    current_paragraph = []
    skip_title = True

    for line in lines:
        stripped = line.strip()

        # Skip first heading (title)
        if stripped.startswith('#') and skip_title:
            skip_title = False
            continue

        # Start of new section - stop
        if stripped.startswith('#'):
            break

        # Empty line marks paragraph boundary
        if not stripped:
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
        else:
            current_paragraph.append(stripped)

    # Add last paragraph if any
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))

    if paragraphs:
        # Return first substantial paragraph
        for para in paragraphs:
            if len(para) > 20:  # At least 20 chars
                return para

    # Strategy 3: First 200 characters
    text = ' '.join(line.strip() for line in lines if line.strip() and not line.strip().startswith('#'))
    return text[:200] + '...' if len(text) > 200 else text


def seed_categories(conn: sqlite3.Connection) -> None:
    """
    Seed predefined categories into the database.

    Args:
        conn: Database connection
    """
    categories = [
        {
            "slug": "context-efficiency",
            "name": "Context Efficiency",
            "description": "Optimizing token usage and context window management",
            "sort_order": 1,
        },
        {
            "slug": "project-setup",
            "name": "Project Setup",
            "description": "Setting up and configuring Claude Code projects",
            "sort_order": 2,
        },
        {
            "slug": "psb-workflow",
            "name": "PSB Workflow",
            "description": "Plan-Scan-Build and other workflow patterns",
            "sort_order": 3,
        },
        {
            "slug": "feature-selection",
            "name": "Feature Selection",
            "description": "Choosing and using Claude Code features effectively",
            "sort_order": 4,
        },
        {
            "slug": "models",
            "name": "Models & Performance",
            "description": "Understanding and selecting Claude models",
            "sort_order": 5,
        },
        {
            "slug": "advanced-patterns",
            "name": "Advanced Patterns",
            "description": "Advanced techniques for experienced users",
            "sort_order": 6,
        },
        {
            "slug": "troubleshooting",
            "name": "Troubleshooting",
            "description": "Solving common problems and errors",
            "sort_order": 7,
        },
        {
            "slug": "best-practices",
            "name": "Best Practices",
            "description": "Recommended approaches and conventions",
            "sort_order": 8,
        },
    ]

    cursor = conn.cursor()

    for cat in categories:
        cursor.execute(
            """
            INSERT OR REPLACE INTO categories (slug, name, description, sort_order)
            VALUES (?, ?, ?, ?)
            """,
            (cat["slug"], cat["name"], cat["description"], cat["sort_order"]),
        )

    conn.commit()
    print(f"✅ Seeded {len(categories)} categories")


def seed_topic(conn: sqlite3.Connection, slug: str, frontmatter: Dict[str, Any],
               content: str, summary: str) -> None:
    """
    Insert or update a single topic in the database.

    Args:
        conn: Database connection
        slug: Topic slug (from filename)
        frontmatter: Parsed frontmatter dict
        content: Full markdown content (without frontmatter)
        summary: Extracted summary text
    """
    cursor = conn.cursor()

    # Extract fields with defaults
    title = frontmatter.get("title", slug.replace("-", " ").title())
    category = frontmatter.get("category", "best-practices")
    commands = frontmatter.get("commands", [])
    keywords = frontmatter.get("keywords", "")
    related_topics = frontmatter.get("related_topics", [])
    difficulty = frontmatter.get("difficulty", "intermediate")

    # Ensure lists are JSON
    commands_json = json.dumps(commands) if commands else None
    related_json = json.dumps(related_topics) if related_topics else None

    # Ensure keywords is a string
    if isinstance(keywords, list):
        keywords = " ".join(keywords)

    cursor.execute(
        """
        INSERT OR REPLACE INTO topics
        (slug, title, category, summary, content, commands, keywords, related_topics, difficulty, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (slug, title, category, summary, content, commands_json, keywords, related_json, difficulty),
    )

    conn.commit()


def seed_from_markdown_dir(conn: sqlite3.Connection, directory: Path) -> int:
    """
    Parse all markdown files in directory and seed topics.

    Args:
        conn: Database connection
        directory: Path to directory containing markdown files

    Returns:
        Number of topics seeded
    """
    if not directory.exists():
        print(f"⚠️ Directory not found: {directory}")
        return 0

    count = 0
    md_files = sorted(directory.glob("*.md"))

    for md_file in md_files:
        try:
            # Read file
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse frontmatter
            frontmatter, remaining_content = parse_frontmatter(content)

            if not frontmatter:
                print(f"⚠️ Skipping {md_file.name} - no frontmatter found")
                continue

            # Extract summary
            summary = extract_summary(remaining_content)

            # Use filename as slug (without .md extension)
            slug = md_file.stem

            # Seed topic
            seed_topic(conn, slug, frontmatter, remaining_content.strip(), summary)

            print(f"✓ Seeded topic: {slug}")
            count += 1

        except Exception as e:
            print(f"❌ Error processing {md_file.name}: {e}")
            continue

    return count


def seed_issue_links(conn: sqlite3.Connection) -> None:
    """
    Seed mappings between health check issues and knowledge topics.

    This creates the relationship table that allows the Fix page to
    link "Learn More" buttons to relevant knowledge topics.

    Args:
        conn: Database connection
    """
    # Map health check rule IDs to topic slugs
    issue_links = [
        ("no-claude-md", "claude-md-basics"),
        ("no-claude-md", "project-setup-guide"),
        ("empty-claude-md", "claude-md-best-practices"),
        ("skills-without-claude-md", "skills-vs-claude-md"),
        ("no-gitignore", "gitignore-setup"),
        ("claude-cache-not-ignored", "gitignore-setup"),
        ("no-model-config", "model-selection"),
        ("model-config-invalid", "model-selection"),
        ("anthropic-xml-in-md", "xml-tags-guide"),
        ("no-task-breakdown", "task-breakdown-strategies"),
        ("vague-instructions", "writing-clear-instructions"),
        ("missing-examples", "providing-examples"),
        ("no-file-conventions", "file-conventions"),
        ("no-code-style", "code-style-guide"),
        ("overly-long-md", "context-efficiency"),
        ("large-files-in-project", "managing-large-files"),
        ("no-test-guidance", "test-guidance"),
        ("missing-context-in-skills", "skill-context-patterns"),
        ("recursive-skill-calls", "skill-antipatterns"),
        ("skill-without-description", "skill-best-practices"),
        ("deprecated-features", "migration-guides"),
    ]

    cursor = conn.cursor()

    for rule_id, topic_slug in issue_links:
        try:
            cursor.execute(
                """
                INSERT OR IGNORE INTO issue_topic_links (issue_rule_id, topic_slug)
                VALUES (?, ?)
                """,
                (rule_id, topic_slug),
            )
        except sqlite3.IntegrityError:
            # Topic doesn't exist yet - skip
            pass

    conn.commit()
    print(f"✅ Seeded {len(issue_links)} issue-topic links")


def seed_knowledge_base(conn: sqlite3.Connection, knowledge_dir: Path) -> Dict[str, int]:
    """
    Full knowledge base seeding - categories, topics, and issue links.

    Args:
        conn: Database connection
        knowledge_dir: Path to directory containing markdown topic files

    Returns:
        Dictionary with counts of seeded items
    """
    print("📚 Seeding knowledge base...")

    # Seed categories
    seed_categories(conn)

    # Seed topics from markdown files
    topic_count = seed_from_markdown_dir(conn, knowledge_dir)

    # Seed issue links
    seed_issue_links(conn)

    print(f"✅ Knowledge base seeding complete!")

    return {
        "categories": 8,
        "topics": topic_count,
        "issue_links": 21,
    }
