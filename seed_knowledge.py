#!/usr/bin/env python3
"""
Knowledge Base Seeding Script
Indexes all markdown files from data/knowledge/ into the database
"""

from pathlib import Path
from services.database import get_db
from services.knowledge_seeder import seed_categories, seed_from_markdown_dir, seed_issue_links


def seed_all_topics():
    """Seed topics from both root and category subdirectories"""

    knowledge_dir = Path(__file__).parent / "data" / "knowledge"

    if not knowledge_dir.exists():
        print(f"❌ Knowledge directory not found: {knowledge_dir}")
        return

    print("📚 Starting knowledge base indexing...")
    print(f"📁 Knowledge directory: {knowledge_dir}\n")

    # Get database connection
    conn = get_db()

    # Seed categories first
    print("1️⃣ Seeding categories...")
    seed_categories(conn)
    print()

    # Seed topics from root directory (original topics)
    print("2️⃣ Seeding topics from root directory...")
    root_count = seed_from_markdown_dir(conn, knowledge_dir)
    print(f"   ✓ Indexed {root_count} topics from root\n")

    # Seed topics from category subdirectories (new topics)
    print("3️⃣ Seeding topics from category subdirectories...")
    subdirectory_count = 0

    # Get all subdirectories
    subdirs = [d for d in knowledge_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    subdirs.sort()

    for subdir in subdirs:
        print(f"   📂 Processing {subdir.name}/")
        count = seed_from_markdown_dir(conn, subdir)
        subdirectory_count += count
        if count > 0:
            print(f"      ✓ Indexed {count} topics")

    print(f"   ✓ Indexed {subdirectory_count} topics from subdirectories\n")

    # Seed issue-topic links
    print("4️⃣ Seeding issue-topic links...")
    seed_issue_links(conn)
    print()

    # Summary
    total_topics = root_count + subdirectory_count
    print("=" * 60)
    print(f"✅ Knowledge base indexing complete!")
    print(f"   📊 Total topics indexed: {total_topics}")
    print(f"   📊 Categories: 8")
    print(f"   📊 Issue links: 21")
    print("=" * 60)

    # Verify database state
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM topics")
    db_count = cursor.fetchone()[0]
    print(f"\n✓ Database verification: {db_count} topics in database")

    conn.close()


if __name__ == "__main__":
    seed_all_topics()
