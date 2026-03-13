# Blogger API Skill

Create and manage Blogger posts via Google's Blogger API v3.

## Features

- ✅ Create draft or published posts
- ✅ Convert markdown to HTML automatically
- ✅ Add labels/tags
- ✅ Update existing posts
- ✅ List recent posts
- ✅ OAuth 2.0 authentication with auto-refresh
- ✅ Schedule posts for future publication

## Quick Start

### 1. Initial Setup (One-Time)

**Prerequisites:**
- Google Cloud project with Blogger API enabled
- OAuth 2.0 credentials saved to `~/Documents/blogger_credentials.json`

**Authorize:**
```bash
cd ~/projects/blogger-skill
python3 scripts/blogger_auth.py
```

This opens your browser for Google authorization and saves tokens to `~/Documents/blogger_token.json`.

### 2. Create Your First Post

**Simple draft post:**
```bash
python3 scripts/blogger_post.py \
  --blog-id "natsu-research" \
  --title "My First Post" \
  --content "<p>Hello World!</p>" \
  --draft
```

**From markdown file:**
```bash
python3 scripts/blogger_post.py \
  --blog-id "natsu-research" \
  --title "Deep Research Report" \
  --markdown ~/path/to/report.md \
  --labels "research,deep-dive" \
  --draft
```

**Publish immediately:**
```bash
python3 scripts/blogger_post.py \
  --blog-id "natsu-research" \
  --title "Published Post" \
  --content "<p>Content here</p>" \
  --publish
```

### 3. List Posts

```bash
python3 scripts/blogger_post.py --blog-id "natsu-research" --list
```

### 4. Update Existing Post

```bash
python3 scripts/blogger_post.py \
  --blog-id "natsu-research" \
  --post-id "1234567890" \
  --title "Updated Title" \
  --content "<p>Updated content</p>"
```

## File Structure

```
blogger-skill/
├── SKILL.md                 # Skill definition for OpenClaw
├── README.md                # This file
├── scripts/
│   ├── blogger_auth.py      # OAuth authorization flow
│   ├── blogger_client.py    # API client (authentication, requests)
│   └── blogger_post.py      # CLI for creating/managing posts
└── examples/
    └── sample_post.md       # Example markdown post
```

## Credentials & Tokens

**Location:** `~/Documents/` (outside git repo)
- `blogger_credentials.json` - OAuth client credentials (from Google Cloud)
- `blogger_token.json` - Access & refresh tokens (auto-generated)

**Security:**
- Never commit credentials/tokens to git
- Tokens auto-refresh when expired
- Re-run `blogger_auth.py` if refresh fails

## Usage from OpenClaw Agent

The agent can use this skill automatically when you ask to post to Blogger:

```
"Create a blog post from today's fountain pen research"
"Post this as a draft to my blog"
"Convert this markdown to a Blogger post"
```

The agent will:
1. Read the skill (SKILL.md)
2. Use blogger_post.py to create the post
3. Return the draft URL for review

## Common Workflows

### Convert Deep Research Report to Blog Post

```bash
python3 scripts/blogger_post.py \
  --blog-id "natsu-research" \
  --title "Japanese Fountain Pens: Deep Research" \
  --markdown ~/projects/deep-research-skill/reports/2026-03-12-japanese-fountain-pens-hard-to-get-us.md \
  --labels "research,fountain-pens,japan" \
  --draft
```

### Batch Create Posts from Directory

```bash
for file in ~/projects/deep-research-skill/reports/*.md; do
  title=$(basename "$file" .md)
  python3 scripts/blogger_post.py \
    --blog-id "natsu-research" \
    --title "$title" \
    --markdown "$file" \
    --labels "research" \
    --draft
done
```

## Troubleshooting

**"Invalid credentials" error:**
```bash
# Re-authorize
python3 scripts/blogger_auth.py
```

**"Blog not found" error:**
- Verify blog ID in Blogger settings
- Check blog is accessible (not private)

**"ModuleNotFoundError: markdown" error:**
```bash
pip3 install markdown
```

## Development

**Install dependencies:**
```bash
pip3 install markdown requests
```

**Test API client:**
```python
from scripts.blogger_client import BloggerClient

client = BloggerClient()
posts = client.list_posts('natsu-research')
print(posts)
```

## License

MIT
