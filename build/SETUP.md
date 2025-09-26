# Quick Setup Guide

## GitHub Repository Configuration

To complete the setup, you need to configure the Git settings to use your mywebsite GitHub account:

### 1. Set Local Git Configuration

```bash
cd /Users/steve/dev/mywebsite-blog-build

# Configure Git to use your mywebsite account (update the email)
git config user.name "My Website"
git config user.email "your-mywebsite-email@domain.com"  # REPLACE WITH YOUR ACTUAL EMAIL

# Check current configuration
git config --list --local
```

### 2. Create Private GitHub Repository

1. **Login to GitHub** with your mywebsite account
2. **Create new repository**: 
   - Name: `mywebsite-blog-build`
   - Visibility: **🔒 PRIVATE** (very important!)
   - Don't initialize with README (we already have one)
3. **Copy the SSH URL** (should be something like):
   ```
   github.com-mywebsite:mywebsite/mywebsite-blog-build.git
   ```

### 3. Connect Repository

```bash
cd /Users/steve/dev/mywebsite-blog-build

# Add the remote (replace with your actual SSH URL from GitHub)
git remote add origin github.com-mywebsite:mywebsite/mywebsite-blog-build.git

# Set main branch
git branch -M main

# Initial commit
git add .
git commit -m "Initial blog build system setup"

# Push to GitHub
git push -u origin main
```

## Verification

After setup, verify everything works:

```bash
# Test the build system
./deploy.sh

# Should output:
# ✅ Blog build completed!
# 📋 Manual next steps: ...

# Check that files were generated in public repo
ls -la static-website/blog/
```

## Daily Workflow

Once setup is complete, your daily workflow will be:

```bash
# 1. Create new blog post
cd /Users/steve/dev/mywebsite-blog-build
vim blog-content/2025-09-22-new-post.md

# 2. Add to index
vim blog-content/index.json

# 3. Deploy with automatic commit
./deploy.sh --commit "Add post about advanced pentesting"

# Or deploy without auto-commit (for review)
./deploy.sh
```

## Repository Security

✅ **Private repo** (`static-website`): Contains only generated HTML, safe for public access  
✅ **Cloudflare Pages**: Deploys from public repo only  

Your source code, build scripts, and markdown files are completely protected!