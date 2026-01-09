#!/usr/bin/env python3
"""
Test script to verify "Learn More" functionality
Demonstrates which health check issues have linked knowledge topics
"""

from services.knowledge_service import get_knowledge_service
from services.database import get_db

# Get all issue-topic links
conn = get_db()
cursor = conn.cursor()

cursor.execute("""
    SELECT DISTINCT issue_rule_id
    FROM issue_topic_links
    ORDER BY issue_rule_id
""")

issue_ids = [row[0] for row in cursor.fetchall()]
conn.close()

# Check which issues have topics
service = get_knowledge_service()

print("🔗 Health Check Issues with Knowledge Topics")
print("=" * 70)
print()

for issue_id in issue_ids:
    topics = service.get_topics_for_issue(issue_id)

    if topics:
        print(f"✅ {issue_id}")
        for topic in topics:
            print(f"   → {topic.title} ({topic.category})")
        print()

print("=" * 70)
print(f"Total: {len(issue_ids)} health check rules have linked knowledge topics")
print()
print("💡 To see \"Learn More\" buttons:")
print("   1. Go to Health Scan page")
print("   2. Select a Claude Code project folder")
print("   3. Run the scan")
print("   4. View issues on the Fix page")
print("   5. Issues with linked topics will show a \"Learn More\" button")
