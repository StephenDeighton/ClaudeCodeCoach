"""
Knowledge Service for Claude Code Coach
Provides search and retrieval of knowledge base topics
"""

import sqlite3
import json
from typing import List, Optional, Dict
from dataclasses import dataclass
from pathlib import Path

from services.database import get_db


@dataclass
class Topic:
    """Knowledge base topic"""
    id: int
    slug: str
    title: str
    category: str
    summary: str
    content: str
    commands: List[str]  # Commands and shortcuts
    keywords: List[str]  # Search boost terms
    related_topics: List[str]  # Related topic slugs
    difficulty: str  # beginner, intermediate, advanced
    created_at: str
    updated_at: str

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Topic":
        """Create Topic from database row"""
        return cls(
            id=row["id"],
            slug=row["slug"],
            title=row["title"],
            category=row["category"],
            summary=row["summary"],
            content=row["content"],
            commands=json.loads(row["commands"]) if row["commands"] else [],
            keywords=row["keywords"].split() if row["keywords"] else [],
            related_topics=json.loads(row["related_topics"]) if row["related_topics"] else [],
            difficulty=row["difficulty"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )


@dataclass
class SearchResult:
    """Search result with ranking"""
    topic: Topic
    rank: float  # BM25 rank score
    snippet: str  # Highlighted snippet from content


@dataclass
class Category:
    """Knowledge base category"""
    id: int
    slug: str
    name: str
    description: str
    sort_order: int
    topic_count: int = 0

    @classmethod
    def from_row(cls, row: sqlite3.Row, topic_count: int = 0) -> "Category":
        """Create Category from database row"""
        return cls(
            id=row["id"],
            slug=row["slug"],
            name=row["name"],
            description=row["description"] if row["description"] else "",
            sort_order=row["sort_order"],
            topic_count=topic_count,
        )


class KnowledgeService:
    """Service for knowledge base operations"""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def search(self, query: str, limit: int = 20) -> List[SearchResult]:
        """
        Search knowledge base using FTS5 full-text search with BM25 ranking.

        Args:
            query: Search query string
            limit: Maximum results to return

        Returns:
            List of SearchResult ordered by relevance (BM25 rank)
        """
        if not query or not query.strip():
            return []

        cursor = self.conn.cursor()

        # FTS5 search with BM25 ranking
        # Use snippet() to generate highlighted excerpts
        cursor.execute(
            """
            SELECT
                t.*,
                topics_fts.rank as search_rank,
                snippet(topics_fts, 2, '**', '**', '...', 32) as snippet
            FROM topics_fts
            JOIN topics t ON topics_fts.rowid = t.id
            WHERE topics_fts MATCH ?
            ORDER BY topics_fts.rank
            LIMIT ?
            """,
            (query, limit),
        )

        results = []
        for row in cursor.fetchall():
            topic = Topic.from_row(row)
            results.append(
                SearchResult(
                    topic=topic,
                    rank=row["search_rank"],
                    snippet=row["snippet"],
                )
            )

        return results

    def get_topic_by_slug(self, slug: str) -> Optional[Topic]:
        """
        Get a topic by its slug.

        Args:
            slug: Topic slug (URL-friendly identifier)

        Returns:
            Topic if found, None otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE slug = ?", (slug,))
        row = cursor.fetchone()

        if row:
            return Topic.from_row(row)
        return None

    def get_topics_by_category(self, category_slug: str) -> List[Topic]:
        """
        Get all topics in a category.

        Args:
            category_slug: Category slug

        Returns:
            List of topics in the category, ordered by title
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM topics
            WHERE category = ?
            ORDER BY title
            """,
            (category_slug,),
        )

        return [Topic.from_row(row) for row in cursor.fetchall()]

    def get_all_categories(self) -> List[Category]:
        """
        Get all categories with topic counts.

        Returns:
            List of categories ordered by sort_order
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT
                c.*,
                COUNT(t.id) as topic_count
            FROM categories c
            LEFT JOIN topics t ON c.slug = t.category
            GROUP BY c.id
            ORDER BY c.sort_order
            """
        )

        return [Category.from_row(row, row["topic_count"]) for row in cursor.fetchall()]

    def get_related_topics(self, topic_slug: str) -> List[Topic]:
        """
        Get related topics for a given topic.

        Args:
            topic_slug: Slug of the source topic

        Returns:
            List of related topics
        """
        topic = self.get_topic_by_slug(topic_slug)
        if not topic or not topic.related_topics:
            return []

        # Get all related topics in a single query
        placeholders = ",".join("?" * len(topic.related_topics))
        cursor = self.conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM topics
            WHERE slug IN ({placeholders})
            ORDER BY title
            """,
            topic.related_topics,
        )

        return [Topic.from_row(row) for row in cursor.fetchall()]

    def get_topics_for_issue(self, issue_rule_id: str) -> List[Topic]:
        """
        Get knowledge topics linked to a health check issue.

        Args:
            issue_rule_id: Health check rule ID (e.g., 'no-claude-md')

        Returns:
            List of topics related to this issue type
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT t.*
            FROM topics t
            JOIN issue_topic_links itl ON t.slug = itl.topic_slug
            WHERE itl.issue_rule_id = ?
            ORDER BY t.title
            """,
            (issue_rule_id,),
        )

        return [Topic.from_row(row) for row in cursor.fetchall()]

    def get_recent_topics(self, limit: int = 10) -> List[Topic]:
        """
        Get recently created or updated topics.

        Args:
            limit: Maximum topics to return

        Returns:
            List of recent topics ordered by updated_at descending
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM topics
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (limit,),
        )

        return [Topic.from_row(row) for row in cursor.fetchall()]

    def get_topics_by_difficulty(self, difficulty: str) -> List[Topic]:
        """
        Get topics by difficulty level.

        Args:
            difficulty: Difficulty level (beginner, intermediate, advanced)

        Returns:
            List of topics with the specified difficulty
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM topics
            WHERE difficulty = ?
            ORDER BY category, title
            """,
            (difficulty,),
        )

        return [Topic.from_row(row) for row in cursor.fetchall()]

    def get_topic_count(self) -> int:
        """
        Get total count of topics in knowledge base.

        Returns:
            Total number of topics
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM topics")
        return cursor.fetchone()["count"]

    def get_category_by_slug(self, slug: str) -> Optional[Category]:
        """
        Get a category by its slug.

        Args:
            slug: Category slug

        Returns:
            Category if found, None otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT
                c.*,
                COUNT(t.id) as topic_count
            FROM categories c
            LEFT JOIN topics t ON c.slug = t.category
            WHERE c.slug = ?
            GROUP BY c.id
            """,
            (slug,),
        )
        row = cursor.fetchone()

        if row:
            return Category.from_row(row, row["topic_count"])
        return None


# Singleton instance
_knowledge_service: Optional[KnowledgeService] = None


def get_knowledge_service() -> KnowledgeService:
    """
    Get singleton KnowledgeService instance.

    Returns:
        KnowledgeService instance
    """
    global _knowledge_service

    if _knowledge_service is None:
        conn = get_db()
        _knowledge_service = KnowledgeService(conn)

    return _knowledge_service
