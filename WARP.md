# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a **static website template** with an integrated blog build system using a consolidated repository structure:

- **`content/`** - Static website files deployed by Cloudflare Pages (public)
- **`build/`** - Private build system with blog source files and scripts (ignored by deployment)

## Architecture

### Repository Structure
```
static-website-template/
├── content/                 # Deployed static files
│   ├── blog/               # Generated blog HTML
│   ├── *.html              # Static pages
│   ├── images/             # Assets
│   └── sitemap.xml         # Generated sitemap
└── build/                  # Build system (private)
    ├── blog-content/       # Markdown source files
    ├── scripts/            # Node.js build scripts
    │   └── build-blog.js   # BlogBuilder class
    ├── templates/          # HTML templates
    ├── deploy.sh           # Deployment script
    └── package.json        # Dependencies
```

### Build System Components

- **BlogBuilder Class** (`build/scripts/build-blog.js`): Main engine for processing markdown files with frontmatter, generating SEO-optimized HTML, and creating sitemaps
- **Template System**: Uses `{{PLACEHOLDER}}` replacement in HTML templates (`build/templates/`)
- **Deployment Script** (`build/deploy.sh`): Orchestrates build process with optional git automation

### Blog Post Processing Pipeline

1. **Source Loading**: Reads markdown files from `build/blog-content/` with YAML frontmatter
2. **URL Generation**: Creates `/blog/YYYY/MM/DD/slug/` structure from filename `YYYY-MM-DD-slug.md`
3. **HTML Generation**: Uses templates with placeholder replacement, adds structured data (JSON-LD)
4. **Output**: Static HTML files in `content/blog/` with breadcrumbs and SEO optimization

## Common Development Commands

### Building the Blog
```bash
cd build

# Build blog posts from markdown (most common)
npm run build-blog

# OR use deployment script for build only
./deploy.sh

# Install dependencies (first time only)
npm install
```

### Blog Management
```bash
# Create new blog post (follow naming convention)
vim build/blog-content/YYYY-MM-DD-post-title.md

# Add frontmatter to new posts:
# ---
# title: "Post Title"
# description: "SEO description (160 chars max)"
# author: "Author Name"
# tags: ["tag1", "tag2"]
# date: YYYY-MM-DD
# ---

# Build and commit (automated deployment)
cd build && ./deploy.sh --commit "Add new blog post"
```

### Local Testing
```bash
# Start local server for testing
cd content && python3 -m http.server 8000
# Visit http://localhost:8000
```

### File Operations
```bash
# Check build output
ls -la content/blog/

# View generated sitemap
cat content/sitemap.xml

# Find blog template files
find build/templates/ -name "*.html"
```

## Blog Post Requirements

### File Naming
- **Format**: `YYYY-MM-DD-post-slug.md`
- **Location**: `build/blog-content/`

### Frontmatter Structure
```yaml
---
title: "Your Post Title"
description: "SEO description (160 chars max)"
author: "Author Name"
tags: ["cybersecurity", "tutorial"]
date: YYYY-MM-DD
image: /images/featured.jpg  # Optional
---
```

### URL Structure
- **Input**: `2025-09-26-example-post.md`
- **Output**: `/blog/2025/09/26/example-post/index.html`

## Deployment Workflows

### Option 1: Build Only (Testing)
```bash
cd build && ./deploy.sh
# Review generated files, test locally, then commit manually
```

### Option 2: Automated (Production)
```bash
cd build && ./deploy.sh --commit "Descriptive commit message"
# Builds, commits, and pushes automatically
```

## Dependencies

- **marked**: Markdown to HTML conversion
- **gray-matter**: YAML frontmatter parsing
- **fs-extra**: Enhanced filesystem operations
- **Node.js**: Runtime for build scripts

## Important Paths

- **Blog Source**: `build/blog-content/`
- **Build Scripts**: `build/scripts/`
- **Templates**: `build/templates/`
- **Generated Output**: `content/blog/`
- **Static Assets**: `content/images/`

## Security Model

- Build system and source files remain in private `build/` directory
- Only generated static HTML files are deployed from `content/`
- Cloudflare Pages deploys only from `content/` directory, ignoring `build/`
- No sensitive build data or source code exposed in deployment