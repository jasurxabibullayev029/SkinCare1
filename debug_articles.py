#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincare_ai.settings')
django.setup()

from articles.models import Article

print('=== Articles Debug ===')
print(f'Total articles: {Article.objects.count()}')

articles = Article.objects.all()[:5]
for article in articles:
    print(f'ID: {article.id}')
    print(f'Title: {article.title}')
    print(f'Slug: {article.slug}')
    print(f'Has featured_image: {bool(article.featured_image)}')
    print(f'Category: {article.category.name if article.category else "None"}')
    print('---')

# Test slug existence
test_slug = 'test'
try:
    test_article = Article.objects.get(slug=test_slug)
    print(f'Found article with slug "{test_slug}": {test_article.title}')
except Article.DoesNotExist:
    print(f'No article found with slug "{test_slug}"')

# Show all slugs
print('\nAll slugs:')
slugs = [a.slug for a in Article.objects.all()]
print(slugs)
