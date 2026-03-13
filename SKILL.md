---
name: blogger
description: Create, edit, and manage Blogger posts via Google Blogger API v3. Use when user wants to post content to Blogger, create blog posts, publish drafts, or manage their blog. Supports markdown-to-HTML conversion, image uploads, labels/tags, and scheduling.
---

# Blogger API Skill

Create and manage Blogger posts programmatically using Google's Blogger API v3.

## When to Use

Use this skill when:
- User asks to post to Blogger or their blog
- Converting content (markdown, research reports) to blog posts
- Creating drafts for review
- Scheduling blog posts
- Managing blog content (list, edit, delete posts)

## Prerequisites

**Required files:**
- `~/.blogger-skill/blogger_credentials.json` - OAuth 2.0 client credentials
- `~/.blogger-skill/blogger_token.json` - Access/refresh tokens (generated via auth flow)

**Required info:**
- Blog ID (e.g., "natsu-research" or numeric ID)

## First-Time Setup

If token doesn't exist, run authorization flow:

```bash
cd ~/projects/blogger-skill
python3 scripts/blogger_auth.py
```

This will:
1. Open browser for Google authorization
2. Capture OAuth code via localhost redirect
3. Exchange code for access + refresh tokens
4. Save to `~/Documents/blogger_token.json`

## Creating Posts

### Basic Post Creation

```bash
python3 scripts/blogger_post.py \
  --blog-id "natsu-research" \
  --title "My Post Title" \
  --content "Post content here" \
  --draft
```

### From Markdown File

```bash
python3 scripts/blogger_post.py \
  --blog-id "natsu-research" \
  --title "Deep Research: Japanese Fountain Pens" \
  --markdown ~/path/to/report.md \
  --labels "research,japan,fountain-pens" \
  --draft
```

### Publishing Immediately

```bash
python3 scripts/blogger_post.py \
  --blog-id "natsu-research" \
  --title "Published Post" \
  --content "Content" \
  --publish
```

## Token Refresh

Tokens expire after 1 hour. The script automatically refreshes using the refresh token.

If refresh fails, re-run `blogger_auth.py` to get new tokens.

## API Endpoints Used

- `POST /blogger/v3/blogs/{blogId}/posts` - Create post
- `GET /blogger/v3/blogs/{blogId}/posts` - List posts
- `PATCH /blogger/v3/blogs/{blogId}/posts/{postId}` - Update post
- `DELETE /blogger/v3/blogs/{blogId}/posts/{postId}` - Delete post

## Common Workflows

### Convert Deep Research Report to Blog Post

1. Read the markdown report
2. Extract title from first heading
3. Convert markdown to HTML
4. Create draft post with labels
5. Return draft URL for review

### Schedule Post for Future

```python
# In post creation, add:
{
  "published": "2026-03-15T09:00:00-07:00"  # ISO 8601 format
}
```

### Update Existing Post

```bash
python3 scripts/blogger_post.py \
  --blog-id "natsu-research" \
  --post-id "1234567890" \
  --title "Updated Title" \
  --content "Updated content"
```

## Important Notes

**Security:**
- Credentials stored in `~/.blogger-skill/` (not in skill directory)
- `.gitignore` excludes credentials
- Never commit tokens to git

**Token expiry:**
- Access tokens last 1 hour
- Refresh tokens last until revoked
- Script auto-refreshes when needed

**Blog ID:**
- Can be blog name (e.g., "natsu-research")
- Or numeric ID (check Blogger settings)
- Use `--blog-id` parameter or set default in script

**Content format:**
- Accepts HTML or markdown
- Markdown converted to HTML automatically
- Images via URLs (must be hosted elsewhere)

## Troubleshooting

**"Invalid credentials" error:**
- Re-run `blogger_auth.py` to get fresh tokens

**"Blog not found" error:**
- Verify blog ID is correct
- Check blog privacy settings (must be accessible)

**"Insufficient permissions" error:**
- Ensure OAuth scope includes `https://www.googleapis.com/auth/blogger`
- Re-authorize with correct scope
