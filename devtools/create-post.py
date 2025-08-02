import os
import json
from datetime import date
import re

# Get absolute path to the script's directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, "posts")
JSON_PATH = os.path.join(POSTS_DIR, "posts.json")
NOTES_PATH = os.path.join(BASE_DIR, "promptnotes.txt")
TEMPLATE_PATH = os.path.join(BASE_DIR, "devtools", "post_template.html")


def get_next_post_number():
    existing = [f for f in os.listdir(POSTS_DIR) if re.match(r'post\d+\.html$', f)]
    numbers = [int(re.search(r'\d+', f).group()) for f in existing]
    return max(numbers, default=0) + 1

def update_posts_json(post_filename, title):
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    posts.append({
        "title": title,
        "url": f"posts/{post_filename}"
    })
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2)

def append_to_notes(title):
    with open(NOTES_PATH, 'a', encoding='utf-8') as f:
        f.write(f"\n\n## {title} ({date.today().isoformat()})\n\n")

def main():
    print("Let's create a new blog post.")
    title = input("Title: ").strip()
    subtitle = input("Subtitle (optional): ").strip()

    post_num = get_next_post_number()
    post_filename = f"post{post_num}.html"
    post_path = os.path.join(POSTS_DIR, post_filename)

    # Load and safely prepare template
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        raw_template = f.read()
        safe_template = raw_template.replace("{", "{{").replace("}", "}}")
        # Put real placeholders back
        safe_template = (
            safe_template
            .replace("{{title}}", "{title}")
            .replace("{{subtitle}}", "{subtitle}")
            .replace("{{year}}", "{year}")
        )

    html = safe_template.format(title=title, subtitle=subtitle, year=date.today().year)

    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(html)

    update_posts_json(post_filename, title)
    append_to_notes(title)

    print(f"\n✅ Created {post_filename}")
    print(f"📄 Post stub at: {post_path}")
    print(f"🧠 Notes added to: {NOTES_PATH}")
    print("✍️  Start writing and commit manually when ready.")

if __name__ == "__main__":
    main()
