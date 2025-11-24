#!/usr/bin/env python
"""
Test script to verify articles functionality is working correctly
"""

import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
django.setup()

from articles.models import Article, ArticleCategory

def test_articles_api():
    print("🧪 Testing Articles API functionality...")

    # Test 1: Check database content
    total_articles = Article.objects.count()
    total_categories = ArticleCategory.objects.count()

    print(f"✅ Database check: {total_articles} articles, {total_categories} categories")

    if total_articles < 10:
        print("⚠️ Warning: Less than 10 articles found. Consider running populate_articles.py")
        return

    # Test 2: Test article retrieval
    try:
        articles = Article.objects.all()[:3]
        print(f"✅ Successfully retrieved {len(articles)} articles")

        for article in articles:
            print(f"  📖 {article.title}")
            print(f"     📂 Category: {article.category.name}")
            print(f"     ⭐ Featured: {article.is_featured}")
            print(f"     👁 Views: {article.view_count}")
            print()

    except Exception as e:
        print(f"❌ Error retrieving articles: {e}")
        return

    # Test 3: Test category filtering
    try:
        categories = ArticleCategory.objects.all()
        if categories:
            category = categories.first()
            category_articles = Article.objects.filter(category=category)
            print(f"✅ Category filtering works: {category.name} has {category_articles.count()} articles")
    except Exception as e:
        print(f"❌ Error with category filtering: {e}")

    # Test 4: Test search functionality
    try:
        search_results = Article.objects.filter(title__icontains='уход')[:2]
        print(f"✅ Search functionality works: found {len(search_results)} articles with 'уход'")
    except Exception as e:
        print(f"❌ Error with search: {e}")

    print("🎉 Articles functionality test completed!")

if __name__ == '__main__':
    test_articles_api()
