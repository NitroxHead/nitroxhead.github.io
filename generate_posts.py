#!/usr/bin/env python3
"""
Script to automatically generate the recent posts section for the blog landing page.
Scans the book/ directory for markdown files and extracts metadata to create post listings.
"""

import os
import re
from datetime import datetime
from pathlib import Path

def extract_post_metadata(file_path):
    """Extract title, date, and description from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title (first # heading)
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else Path(file_path).stem.replace('-', ' ').title()

    # Extract date (look for *Published: DATE* pattern)
    date_match = re.search(r'\*Published: (.+?)\*', content)
    date_str = date_match.group(1) if date_match else "Unknown date"

    # Extract description (first paragraph after title and date)
    # Split content into lines and find the first substantial paragraph
    lines = content.split('\n')
    description = ""

    # Skip title, date, and empty lines to find first paragraph
    start_looking = False
    for line in lines:
        line = line.strip()
        if start_looking and line and not line.startswith('#') and not line.startswith('*Published:'):
            # Take first sentence or first 150 characters
            description = line
            if '.' in description:
                description = description.split('.')[0] + '.'
            elif len(description) > 150:
                description = description[:150] + '...'
            break
        elif line.startswith('# '):
            start_looking = True

    # If no description found, create a generic one
    if not description:
        description = f"Explore insights about {title.lower()}."

    return {
        'title': title,
        'date': date_str,
        'description': description,
        'file_path': file_path
    }

def parse_date(date_str):
    """Parse date string to datetime object for sorting."""
    try:
        return datetime.strptime(date_str, "%B %d, %Y")
    except:
        return datetime.min

def generate_posts_section():
    """Generate the recent posts section markdown."""
    book_dir = Path('book')
    posts = []

    # Scan for markdown files in book directory
    for file_path in book_dir.glob('*.md'):
        if file_path.name != 'references.md':  # Skip reference files
            metadata = extract_post_metadata(file_path)
            posts.append(metadata)

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: parse_date(x['date']), reverse=True)

    # Generate markdown
    posts_md = "## Recent Posts\n\n"

    for post in posts:
        relative_path = f"book/{Path(post['file_path']).name}"
        posts_md += f"### [{post['title']}]({relative_path})\n"
        posts_md += f"*{post['date']}*\n\n"
        posts_md += f"{post['description']}\n\n"
        posts_md += "---\n\n"

    return posts_md.rstrip('---\n\n') + "\n\n"

def update_index_md():
    """Update index.md with automatically generated posts section."""
    index_path = Path('index.md')

    # Read current index.md
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the posts section and replace it
    # Look for "## Recent Posts" section
    posts_section = generate_posts_section()

    # Replace everything from "## Recent Posts" to the final thanks message
    pattern = r'(# NitroxHead\'s Tech Blog\n\n.*?\n\n)(## Recent Posts.*?)(\*Thanks for stopping by!.*)'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        new_content = match.group(1) + posts_section + match.group(3)
    else:
        # If pattern doesn't match, append posts section before thanks message
        thanks_pattern = r'(\*Thanks for stopping by!.*)'
        thanks_match = re.search(thanks_pattern, content, re.DOTALL)
        if thanks_match:
            new_content = content.replace(thanks_match.group(1), posts_section + thanks_match.group(1))
        else:
            # If no thanks message, just append
            new_content = content + "\n" + posts_section

    # Write updated content
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("✅ Updated index.md with automatically generated posts section")

if __name__ == "__main__":
    update_index_md()