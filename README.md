# Static Website Template

Easy-peasy and free static website hosting via Cloudflare pages with blogging support. This is what was used to build the [CylentSec website](https://www.cylentsec.com).

The benefits are:
- No hosting costs (depending on Cloudflare's terms and conditions)
- No CMS security updates
- Supports easily creating new blog posts in Markdown format

Note: You'll have to use search in your editor to replace all occurrences of "My Website" (copyright notices) and similar text for personalizing the branding, and also replace the header image with your own. 

## Repository Structure

```
static-website/
├── content/                 # 🌐 DEPLOYED CONTENT (Cloudflare Pages deploys from here)
│   ├── index.html          # Website homepage
│   ├── services.html       # Services page  
│   ├── contact.html        # Contact page
│   ├── blog/               # Generated blog posts
│   │   ├── index.html      # Blog index page
│   │   └── YYYY/MM/DD/     # Individual blog posts
│   ├── images/             # Website assets
│   └── sitemap.xml         # Generated sitemap
├── build/                  # 🔨 BUILD SYSTEM (ignored by Cloudflare Pages)
│   ├── blog-content/       # Markdown source files for blog posts
│   ├── scripts/            # Node.js build scripts
│   │   └── build-blog.js   # Main blog builder
│   ├── templates/          # HTML templates for blog
│   ├── deploy.sh           # Deployment automation
│   ├── package.json        # Build dependencies
│   └── documentation/      # Build system docs
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Cloudflare Pages Configuration

**Important**: Configure your Cloudflare Pages project with:
- **Build output directory**: `content`
- **Build command**: None (or leave empty)
- The `build/` directory is automatically ignored by Cloudflare Pages

## Quick Start

### 1. Building Blog Content

```bash
cd build
npm install                    # Install dependencies (first time only)
npm run build-blog            # Build blog posts from markdown
```

### 2. Adding New Blog Posts

1. Create a new markdown file in `build/blog-content/`:
   ```bash
   # File format: YYYY-MM-DD-post-title.md
   vim build/blog-content/2025-09-25-new-post.md
   ```

2. Add frontmatter to your post:
   ```markdown
   ---
   title: "Your Post Title"
   description: "SEO description (160 chars max)"
   author: "Author Name" 
   tags: ["cybersecurity", "pentesting"]
   date: 2025-09-25
   ---

   # Your Content Here
   
   Your blog post content in markdown...
   ```

3. Build and deploy:
   ```bash
   cd build
   ./deploy.sh --commit "Add new security analysis post"
   ```

### 3. Local Development

```bash
# Build the blog
cd build && npm run build-blog

# Test locally  
cd ../content
python3 -m http.server 8000

# Visit http://localhost:8000
```

## Deployment Workflows

### Automated Deployment (Recommended)
```bash
cd build
./deploy.sh --commit "Your commit message"
```

This will:
1. Build all blog posts from markdown
2. Update the sitemap
3. Commit all changes to the repository
4. Push to GitHub (triggering Cloudflare Pages deployment)

### Manual Deployment
```bash
cd build
npm run build-blog              # Build only

# Review changes in ../content/blog/
# Test locally if desired

# Commit manually
git add ../content/blog/ ../content/sitemap.xml blog-content/
git commit -m "Update blog: Your description"
git push
```

## Repository Benefits

### ✅ Single Repository Management
- One repository to clone, manage, and maintain
- Simplified permissions and access control
- Unified git history for both content and build system

### ✅ Cloudflare Pages Integration
- Cloudflare Pages deploys only the `content/` directory
- Build system in `build/` directory is ignored by deployment
- No additional build commands needed on Cloudflare Pages

### ✅ Security Through Separation
- Build scripts and source content remain in private repository
- Only generated static content is deployed publicly
- No sensitive build data exposed in deployment

### ✅ Developer Experience
- All tools and content in one place
- Consistent workflow for website and blog updates
- Easy local testing and development
