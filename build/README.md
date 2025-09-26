# Static Blog Build System (Private Repository)

## Overview

This is the **private development repository** for a blog build system. It contains source files, build scripts, and documentation that should NOT be exposed publicly.

## Directory Structure

```
static-website/ (PRIVATE REPO)
├── blog/                  # Generated static HTML (deployed by build script)
├── sitemap.xml            # Generated sitemap (deployed by build script)
├── index.html             # Static website files
├── contact.html           
└── images/                # Static assets
```

## Security Benefits

✅ **Source code protected** - Build scripts not exposed publicly
✅ **Markdown files secure** - Raw content not accessible via web
✅ **Dependencies hidden** - package.json and node_modules not deployed
✅ **Templates protected** - HTML templates not exposed
✅ **Clean deployment** - Only final static HTML reaches public

## Quick Start

### 1. Setup (First Time)

```bash
cd /Users/steve/dev/mywebsite-blog-build

# Install dependencies
npm install

# Set up Git configuration to use mywebsite account
git config user.name "My Website"
git config user.email "your-mywebsite-email@example.com"  # Update this

# Add remote (you'll create this private GitHub repo)
git remote add origin github.com-mywebsite:mywebsite/mywebsite-blog-build.git
```

### 2. Create New Blog Posts

```bash
# 1. Create markdown file
vim blog-content/2025-09-22-your-post-title.md

# 2. Add to index
vim blog-content/index.json

# 3. 🚀 AUTOMATED DEPLOYMENT (Recommended)
./deploy.sh --commit "Add new cybersecurity analysis post"

# OR manual process:
# 3a. Build only
./deploy.sh
# 3b. Review generated files
# 3c. Commit source files to private repo
git add . && git commit -m "Add new blog post: Your Title" && git push
# 3d. Commit generated files to public repo
cd ../content
git add blog/ sitemap.xml && git commit -m "Update blog: Your Title" && git push
```

## Available Commands

```bash
# 🚀 RECOMMENDED: Full automated deployment
./deploy.sh --commit "Your descriptive commit message"

# 🔨 Build only (for testing/review)
./deploy.sh

# ⚙️ Manual build (alternative method)
npm run build-blog

# 🖺 Start local development server
cd ../content && python3 -m http.server 8000
```

## Files Kept Private

The following files remain in this private repository and are never deployed publicly:

- 🔒 `scripts/` - Build system source code
- 🔒 `templates/` - HTML template files  
- 🔒 `blog-content/` - Raw markdown source files
- 🔒 `package.json` - Dependencies and build configuration
- 🔒 `node_modules/` - Installed dependencies
- 🔒 `BLOG_TUTORIAL.md` - Internal documentation
- 🔒 This `README.md` - Private setup instructions

## Files Deployed Publicly

Only these generated files are deployed to the public website:

- ✅ `blog/` - Generated static HTML pages
- ✅ `sitemap.xml` - Generated XML sitemap

## Workflow Summary

1. **Edit** markdown files in this private repo
2. **Build** with `npm run build-blog` (deploys to public repo)
3. **Commit** source changes to this private repo
4. **Commit** generated files in the public repo
5. **Cloudflare Pages** automatically deploys the public repo

## Security Notes

- Never commit sensitive information to markdown files
- Keep this repository PRIVATE on GitHub
- Only the public repository should be connected to Cloudflare Pages
- Generated HTML files contain no source code or build system details

## GitHub Repository Setup

To create the private GitHub repository:

1. Go to GitHub.com (logged in as mywebsite account)
2. Create new repository: `mywebsite-blog-build`
3. Set as **PRIVATE**
4. Don't initialize with README (we already have one)
5. Copy the SSH URL and add as remote:

```bash
git remote add origin github.com-mywebsite:mywebsite/mywebsite-blog-build.git
git branch -M main
git add .
git commit -m "Initial blog build system"
git push -u origin main
```