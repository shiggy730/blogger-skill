#!/usr/bin/env python3
"""
Create or update Blogger posts
"""

import argparse
import sys
from pathlib import Path
import markdown

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from blogger_client import BloggerClient

def markdown_to_html(md_content):
    """Convert markdown to HTML"""
    return markdown.markdown(md_content, extensions=['extra', 'codehilite', 'tables'])

def main():
    parser = argparse.ArgumentParser(description='Create or update Blogger posts')
    parser.add_argument('--blog-id', required=True, help='Blog ID')
    parser.add_argument('--title', help='Post title')
    parser.add_argument('--content', help='Post content (HTML)')
    parser.add_argument('--markdown', help='Path to markdown file')
    parser.add_argument('--labels', help='Comma-separated labels/tags')
    parser.add_argument('--draft', action='store_true', help='Create as draft (default)')
    parser.add_argument('--publish', action='store_true', help='Publish immediately')
    parser.add_argument('--post-id', help='Post ID (for updating existing post)')
    parser.add_argument('--list', action='store_true', help='List recent posts')
    
    args = parser.parse_args()
    
    client = BloggerClient()
    
    # List posts
    if args.list:
        print(f"📝 Listing posts for blog: {args.blog_id}\n")
        posts = client.list_posts(args.blog_id)
        
        if 'items' in posts:
            for i, post in enumerate(posts['items'], 1):
                print(f"{i}. {post['title']}")
                print(f"   ID: {post['id']}")
                print(f"   URL: {post['url']}")
                print(f"   Status: {'DRAFT' if post.get('status') == 'DRAFT' else 'PUBLISHED'}")
                print()
        else:
            print("No posts found")
        return
    
    # Determine content
    content = None
    if args.markdown:
        with open(args.markdown, 'r') as f:
            md_content = f.read()
        content = markdown_to_html(md_content)
        print(f"📄 Converted markdown from: {args.markdown}")
    elif args.content:
        content = args.content
    else:
        print("❌ Error: Must provide --content or --markdown")
        sys.exit(1)
    
    # Update existing post
    if args.post_id:
        print(f"✏️  Updating post ID: {args.post_id}")
        result = client.update_post(
            args.blog_id,
            args.post_id,
            title=args.title,
            content=content,
            labels=args.labels
        )
        print(f"✅ Post updated: {result['url']}")
        return
    
    # Create new post
    if not args.title:
        print("❌ Error: --title required for new posts")
        sys.exit(1)
    
    is_draft = not args.publish  # Default to draft unless --publish
    
    print(f"📝 Creating {'draft' if is_draft else 'published'} post...")
    print(f"   Blog: {args.blog_id}")
    print(f"   Title: {args.title}")
    if args.labels:
        print(f"   Labels: {args.labels}")
    
    result = client.create_post(
        args.blog_id,
        args.title,
        content,
        labels=args.labels,
        is_draft=is_draft
    )
    
    print(f"\n✅ Post created successfully!")
    print(f"   ID: {result['id']}")
    print(f"   URL: {result['url']}")
    print(f"   Status: {result.get('status', 'UNKNOWN')}")

if __name__ == '__main__':
    main()
