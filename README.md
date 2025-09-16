# NitroxHead's Tech Blog

A personal blog built with Jupyter Book, automatically deployed to GitHub Pages.

## 🚀 Automatic Blog System

This blog features an **automatic post generation system**:
- Add new blog posts to the `book/` directory
- Push to GitHub
- The site automatically rebuilds and updates the landing page

## ✍️ Adding New Posts

1. Create a new `.md` file in the `book/` directory
2. Use this format:

```markdown
# Your Post Title

*Published: March 30, 2024*

Your post content here...
```

3. Update `_toc.yml` to include your new post
4. Push to GitHub - everything else is automatic!

## 🛠️ Manual Development

To work locally:

```bash
# Generate the post listings
python3 generate_posts.py

# Build the site
jupyter-book build .

# Serve locally
python3 -m http.server 8080 --directory _build/html
```

## 📁 Project Structure

- `book/` - Blog posts (markdown files)
- `generate_posts.py` - Script to auto-generate post listings
- `_config.yml` - Jupyter Book configuration
- `_toc.yml` - Table of contents
- `.github/workflows/deploy.yml` - GitHub Actions for auto-deployment

## 🌐 Live Site

The blog is automatically deployed to: https://nitroxhead.github.io

---

*Built with ❤️ using Jupyter Book and GitHub Actions*
