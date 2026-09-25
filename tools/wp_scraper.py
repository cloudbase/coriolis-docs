import os
import re
import requests
import html2text
from urllib.parse import urlparse, unquote

SITE_URL = "https://cloudbase.it/"
FILTER_KEYWORD = "coriolis"  # Only export pages containing this word
OUTPUT_DIR = "source"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "_static", "images")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Configure HTML to Markdown converter
converter = html2text.HTML2Text()
converter.ignore_links = False
converter.ignore_images = False
converter.body_width = 0  # Disable line wrapping inside paragraphs


def download_image(img_url):
    """Downloads an image locally and returns the relative path for Sphinx."""
    try:
        parsed_url = urlparse(img_url)
        filename = os.path.basename(unquote(parsed_url.path))
        
        if not filename:
            return img_url

        local_filepath = os.path.join(IMAGES_DIR, filename)

        if not os.path.exists(local_filepath):
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(img_url, headers=headers, stream=True, timeout=10)
            if response.status_code == 200:
                with open(local_filepath, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"  [Image] Downloaded: {filename}")
            else:
                print(f"  [Image] Failed ({response.status_code}): {img_url}")
                return img_url

        return f"_static/images/{filename}"
    except Exception as e:
        print(f"  [Image Error] {img_url}: {e}")
        return img_url


def fetch_all_pages():
    """Fetches pages using WP REST API search filter to reduce payload size."""
    pages = []
    page_num = 1
    per_page = 100

    while True:
        url = f"{SITE_URL}/wp-json/wp/v2/pages"
        # Search parameter queries WP backend directly for matching keyword
        params = {
            "search": FILTER_KEYWORD,
            "page": page_num,
            "per_page": per_page,
            "status": "publish",
        }
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            break
            
        data = response.json()
        if not data:
            break
            
        pages.extend(data)
        
        total_pages = int(response.headers.get("X-WP-TotalPages", 1))
        if page_num >= total_pages:
            break
            
        page_num += 1

    return pages


print(f"Fetching pages matching '{FILTER_KEYWORD}' from {SITE_URL}...")
matching_pages = fetch_all_pages()
print(f"Found {len(matching_pages)} potential pages. Filtering and converting...")

MD_IMAGE_REGEX = re.compile(r'!\[(.*?)\]\((https?://[^\s\)]+)\)')
saved_count = 0

for page in matching_pages:
    title = page["title"]["rendered"]
    slug = page["slug"]
    html_content = page["content"]["rendered"]
    
    # Double-check full text content (title + body) for exact keyword match
    full_text = f"{title} {html_content}".lower()
    if FILTER_KEYWORD.lower() not in full_text:
        print(f"Skipped (keyword not in body): {title}")
        continue

    # 1. Convert HTML content to standard Markdown
    markdown_content = converter.handle(html_content)
    
    # 2. Extract, download, and update image URLs
    def image_replacer(match):
        alt_text = match.group(1)
        original_url = match.group(2)
        local_rel_path = download_image(original_url)
        return f"![{alt_text}]({local_rel_path})"

    updated_markdown = MD_IMAGE_REGEX.sub(image_replacer, markdown_content)
    
    # 3. Attach MyST Front Matter metadata
    file_data = f"---\ntitle: \"{title}\"\nwp_id: {page['id']}\n---\n\n# {title}\n\n{updated_markdown}"
    
    filename = os.path.join(OUTPUT_DIR, f"{slug}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(file_data)
        
    print(f"Saved page: {filename}")
    saved_count += 1

print(f"\nDone! Saved {saved_count} pages matching '{FILTER_KEYWORD}' into '{OUTPUT_DIR}'")
