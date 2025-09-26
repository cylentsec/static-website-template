#!/usr/bin/env node

const fs = require('fs-extra');
const path = require('path');
const { marked } = require('marked');
const matter = require('gray-matter');

class BlogBuilder {
    constructor() {
        this.siteUrl = 'https://example.com'; // Update this to your actual domain
        this.siteName = 'My Blog';
        this.siteDescription = 'Cybersecurity Insights and Updates';
        
        this.baseDir = path.join(__dirname, '..');
        this.publicSiteDir = path.resolve(__dirname, '../../content'); // Public website deployment directory
        this.blogContentDir = path.join(this.baseDir, 'blog-content');
        this.templatesDir = path.join(this.baseDir, 'templates');
        this.blogOutputDir = path.join(this.publicSiteDir, 'blog');
        this.posts = [];
    }

    // Ensure all necessary directories exist
    async setupDirectories() {
        await fs.ensureDir(this.blogOutputDir);
        await fs.ensureDir(path.join(this.blogOutputDir, 'assets'));
    }

    // Load and parse all markdown files
    async loadPosts() {
        const files = await fs.readdir(this.blogContentDir);
        const markdownFiles = files.filter(file => file.endsWith('.md'));

        for (const filename of markdownFiles) {
            const filePath = path.join(this.blogContentDir, filename);
            const fileContent = await fs.readFile(filePath, 'utf8');
            
            // Parse frontmatter and content
            const parsed = matter(fileContent);
            const dateMatch = filename.match(/^(\d{4}-\d{2}-\d{2})-(.+)\.md$/);
            
            if (dateMatch) {
                const [, date, slug] = dateMatch;
                const post = {
                    filename,
                    slug,
                    date,
                    title: parsed.data.title || this.formatTitle(slug),
                    description: parsed.data.description || this.extractDescription(parsed.content),
                    author: parsed.data.author || 'Author',
                    tags: parsed.data.tags || ['cybersecurity'],
                    image: parsed.data.image || null,
                    content: parsed.content,
                    frontmatter: parsed.data,
                    url: this.generatePostUrl(date, slug)
                };
                
                this.posts.push(post);
            }
        }

        // Sort posts by date (newest first)
        this.posts.sort((a, b) => new Date(b.date) - new Date(a.date));
        console.log(`✓ Loaded ${this.posts.length} blog posts`);
    }

    // Generate URL structure for posts
    generatePostUrl(date, slug) {
        const [year, month, day] = date.split('-');
        return `/blog/${year}/${month}/${day}/${slug}/`;
    }

    // Format title from slug
    formatTitle(slug) {
        return slug
            .replace(/-/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());
    }

    // Extract description from content
    extractDescription(content) {
        const lines = content.split('\n');
        for (const line of lines) {
            const trimmed = line.trim();
            if (trimmed && !trimmed.startsWith('#')) {
                return trimmed.length > 160 ? trimmed.substring(0, 157) + '...' : trimmed;
            }
        }
        return 'Read more about cybersecurity insights and updates.';
    }

    // Generate individual post pages
    async generatePostPages() {
        const postTemplate = await this.loadTemplate('post.html');
        
        for (const post of this.posts) {
            const [year, month, day] = post.date.split('-');
            const postDir = path.join(this.blogOutputDir, year, month, day, post.slug);
            await fs.ensureDir(postDir);

            // Convert markdown to HTML
            const contentHtml = marked(post.content);
            
            // Generate breadcrumbs
            const breadcrumbs = [
                { name: 'Home', url: '/index.html' },
                { name: 'Blog', url: '/blog/' },
                { name: post.title, url: post.url }
            ];

            // Replace template variables
            const html = this.replacePlaceholders(postTemplate, {
                SITE_NAME: this.siteName,
                SITE_URL: this.siteUrl,
                POST_TITLE: post.title,
                POST_DESCRIPTION: post.description,
                POST_AUTHOR: post.author,
                POST_DATE: this.formatDate(post.date),
                POST_DATE_ISO: post.date,
                POST_URL: this.siteUrl + post.url,
                POST_CONTENT: contentHtml,
                POST_TAGS: post.tags.join(', '),
                BREADCRUMBS: this.generateBreadcrumbs(breadcrumbs),
                STRUCTURED_DATA: this.generateStructuredData(post)
            });

            await fs.writeFile(path.join(postDir, 'index.html'), html);
            console.log(`✓ Generated: ${post.url}`);
        }
    }

    // Generate blog index page
    async generateBlogIndex() {
        const indexTemplate = await this.loadTemplate('blog-index.html');
        
        // Generate post previews
        const postPreviews = this.posts.map(post => {
            return `
                <article class="blog-post-preview">
                    <h3 class="post-title">
                        <a href="${post.url}">${post.title}</a>
                    </h3>
                    <div class="post-meta">
                        <span class="post-date">${this.formatDate(post.date)}</span>
                        <span class="post-author">by ${post.author}</span>
                    </div>
                    <div class="post-preview">
                        <p>${post.description}</p>
                    </div>
                    <div class="post-actions">
                        <a href="${post.url}" class="read-more-btn">Read More →</a>
                    </div>
                </article>
            `;
        }).join('');

        const html = this.replacePlaceholders(indexTemplate, {
            SITE_NAME: this.siteName,
            SITE_URL: this.siteUrl,
            SITE_DESCRIPTION: this.siteDescription,
            POST_PREVIEWS: postPreviews,
            POSTS_COUNT: this.posts.length
        });

        await fs.writeFile(path.join(this.blogOutputDir, 'index.html'), html);
        console.log('✓ Generated blog index page');
    }

    // Generate XML sitemap
    async generateSitemap() {
        const urls = [
            { url: '/', priority: '1.0' },
            { url: '/services/', priority: '0.8' },
            { url: '/blog/', priority: '0.8' },
            { url: '/contact/', priority: '0.6' }
        ];

        // Add blog posts
        this.posts.forEach(post => {
            urls.push({
                url: post.url,
                lastmod: post.date,
                priority: '0.7'
            });
        });

        const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(item => `  <url>
    <loc>${this.siteUrl}${item.url}</loc>
    ${item.lastmod ? `<lastmod>${item.lastmod}</lastmod>` : ''}
    <priority>${item.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

        await fs.writeFile(path.join(this.publicSiteDir, 'sitemap.xml'), sitemap);
        console.log('✓ Generated sitemap.xml');
    }

    // Load HTML template
    async loadTemplate(templateName) {
        const templatePath = path.join(this.templatesDir, templateName);
        return await fs.readFile(templatePath, 'utf8');
    }

    // Replace template placeholders
    replacePlaceholders(template, replacements) {
        let result = template;
        for (const [key, value] of Object.entries(replacements)) {
            const regex = new RegExp(`{{${key}}}`, 'g');
            result = result.replace(regex, value || '');
        }
        return result;
    }

    // Format date for display
    formatDate(dateString) {
        const [year, month, day] = dateString.split('-').map(Number);
        const date = new Date(year, month - 1, day);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    // Generate breadcrumb navigation
    generateBreadcrumbs(breadcrumbs) {
        return breadcrumbs.map((crumb, index) => {
            const isLast = index === breadcrumbs.length - 1;
            return isLast 
                ? `<span class="breadcrumb-current">${crumb.name}</span>`
                : `<a href="${crumb.url}" class="breadcrumb-link">${crumb.name}</a>`;
        }).join(' <span class="breadcrumb-separator">›</span> ');
    }

    // Generate JSON-LD structured data
    generateStructuredData(post) {
        const structuredData = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post.title,
            "description": post.description,
            "author": {
                "@type": "Organization",
                "name": post.author
            },
            "publisher": {
                "@type": "Organization",
                "name": this.siteName,
                "url": this.siteUrl
            },
            "datePublished": post.date,
            "dateModified": post.date,
            "url": this.siteUrl + post.url,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": this.siteUrl + post.url
            }
        };

        if (post.image) {
            structuredData.image = post.image;
        }

        return JSON.stringify(structuredData, null, 2);
    }

    // Main build function
    async build() {
        try {
            console.log('🚀 Building static blog...');
            
            await this.setupDirectories();
            await this.loadPosts();
            
            if (this.posts.length === 0) {
                console.log('⚠️  No blog posts found. Create some .md files in blog-content/');
                return;
            }
            
            await this.generatePostPages();
            await this.generateBlogIndex();
            await this.generateSitemap();
            
            console.log('✅ Blog build completed successfully!');
            console.log(`📊 Generated ${this.posts.length} blog posts`);
            console.log('🌐 Blog available at /blog/');
            
        } catch (error) {
            console.error('❌ Build failed:', error);
            process.exit(1);
        }
    }
}

// Run the builder if called directly
if (require.main === module) {
    const builder = new BlogBuilder();
    builder.build();
}

module.exports = BlogBuilder;