#!/bin/bash

set -e  # Exit on any error

# Show help if requested
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "🤖 Blog Deployment Script"
    echo ""
    echo "Usage:"
    echo "  ./deploy.sh                    # Build only (for testing/review)"
    echo "  ./deploy.sh --commit \"msg\"    # Build + commit + push both repos"
    echo "  ./deploy.sh --help             # Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh --commit \"Add new penetration testing guide\""
    echo "  ./deploy.sh --commit \"Fix typos in security best practices post\""
    echo ""
    echo "What it does:"
    echo "  ✅ Builds static HTML from markdown files"
    echo "  ✅ Deploys to public website repository"
    echo "  ✅ With --commit: automatically commits and pushes both repos"
    echo "  ✅ With --commit: triggers Cloudflare Pages deployment"
    echo ""
    echo "SSH Key Passwords:"
    echo "  • Script works with password-protected SSH keys"
    echo "  • Safe for multi-account setups (won't interfere with other GitHub accounts)"
    exit 0
fi

echo "🚀 Starting blog deployment..."

# Build the blog (outputs to public website directory)
echo "📝 Building blog..."
npm run build-blog

echo "✅ Blog build completed!"

# Check if we should commit automatically
if [ "$1" = "--commit" ]; then
    if [ -z "$2" ]; then
        echo "❌ Error: Commit message required when using --commit"
        echo "Usage: ./deploy.sh --commit \"Your commit message\""
        exit 1
    fi
    
    COMMIT_MSG="$2"
    
    echo "💾 Committing to consolidated repository..."
    cd ..
    git add content/blog/ content/sitemap.xml build/blog-content/
    git commit -m "Update blog: $COMMIT_MSG" || echo "No changes to commit"
    
    echo "📤 Pushing to repository..."
    git push
    
    echo "🌐 Deployment complete! Changes will be live on Cloudflare Pages shortly."
    
else
    echo ""
    echo "📋 Manual next steps:"
    echo "1. Review generated files in ../content/blog/"
    echo "2. Test locally: cd .. && python3 -m http.server 8000 -d content"
    echo "3. Commit all changes:"
    echo "   cd .. && git add content/blog/ content/sitemap.xml build/blog-content/"
    echo "   git commit -m 'Update blog: DESCRIPTION' && git push"
    echo ""
    echo "Or run: ./deploy.sh --commit \"Your commit message\" (to automate step 3)"
fi

echo "✨ Done!"