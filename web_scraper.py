import os
import time
import random
import requests
from googlesearch import search
from bs4 import BeautifulSoup
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def create_temp_folder():
    """Create a temporary folder for storing files."""
    if not os.path.exists('temp'):
        os.makedirs('temp')

def delete_temp_files():
    """Delete all files in the temp folder after processing."""
    for filename in os.listdir('temp'):
        file_path = os.path.join('temp', filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Error deleting {file_path}: {e}')
# old code
# def google_search(query, num_results=5, retries=3):
#     """Perform Google search with retries to avoid failures."""
#     for _ in range(retries):
#         try:
#             return list(search(query, num_results=num_results))
#         except Exception as e:
#             print(f"Search failed (retry {_+1}/{retries}): {str(e)}")
#             time.sleep(random.uniform(2, 5))  # Wait before retrying
#     return []

# def google_search(query, num_results=5, retries=3):
#     """Perform Google search with retries."""
#     for _ in range(retries):
#         try:
#             # Use the correct syntax for `googlesearch.search()`
#             results = list(search(query, num=5))  # FIXED: Changed `num_results` to `num`
#             return results
#         except Exception as e:
#             print(f"Search failed (retry {_+1}/{retries}): {str(e)}")
#             time.sleep(random.uniform(2, 5))  # Wait before retrying
#     return []

def google_search(query, num_results=5, retries=3):
    """Perform Google search with a limit of 5 results."""
    for attempt in range(retries):
        try:
            print(f"🔍 Attempt {attempt+1}: Searching Google for '{query}'")

            # Use `stop=5` to limit results
            results = list(search(query, stop=num_results))

            print(f"✅ Found {len(results)} results: {results}")
            return results
        except Exception as e:
            print(f"⚠️ Google Search failed (retry {attempt+1}/{retries}): {e}")
            time.sleep(random.uniform(2, 5))  # Wait before retrying
    return []

def fetch_web_content(url):
    """Fetch webpage content using requests."""
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'AppleWebKit/537.36 (KHTML, like Gecko)',
            'Chrome/Safari/537.36'
        ])
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def extract_structured_sections(html):
    """Extract structured content (headings and paragraphs) from HTML."""
    soup = BeautifulSoup(html, 'html.parser')

    # Remove unnecessary tags
    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript', 'button', 'option', 'aside']):
        tag.decompose()

    sections = []
    current_heading = None
    current_content = []

    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        if element.name.startswith('h'):
            if current_heading is not None or current_content:
                sections.append({
                    'heading': current_heading.strip() if current_heading else '',
                    'content': ' '.join(current_content).strip()
                })
                current_content = []
            current_heading = element.get_text(strip=True)
        else:
            text = element.get_text(strip=True)
            if text:
                current_content.append(text)

    if current_heading is not None or current_content:
        sections.append({
            'heading': current_heading.strip() if current_heading else '',
            'content': ' '.join(current_content).strip()
        })

    return sections

def rank_and_select_content(query, all_pages_sections, successful_urls):
    """Use ML techniques to rank and extract the most relevant content."""
    corpus = []
    page_indices = []
    all_sections_list = []

    for page_idx, sections in enumerate(all_pages_sections):
        for section in sections:
            if len(section['content']) < 50:  # Filter short content
                continue
            combined_text = f"{section['heading']} {section['heading']} {section['content']}"
            corpus.append(combined_text)
            page_indices.append(page_idx)
            all_sections_list.append(section)

    if not corpus:
        return None, None

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(corpus)
        query_vec = vectorizer.transform([query])

        similarities = cosine_similarity(query_vec, X).flatten()
        page_scores = defaultdict(list)

        for idx, page_idx in enumerate(page_indices):
            page_scores[page_idx].append(similarities[idx])

        ranked_pages = {}
        for page_idx, scores in page_scores.items():
            ranked_pages[page_idx] = sum(sorted(scores, reverse=True)[:2])

        if not ranked_pages:
            return None, None

        best_page_idx = max(ranked_pages, key=ranked_pages.get)
        best_url = successful_urls[best_page_idx]

        best_sections = []
        for idx, page_idx in enumerate(page_indices):
            if page_idx == best_page_idx:
                best_sections.append((similarities[idx], all_sections_list[idx]))

        best_sections.sort(reverse=True, key=lambda x: x[0])
        selected_content = [section for score, section in best_sections[:2] if section['content']]
        # this best_sections will increate points
        return selected_content, best_url

    except Exception as e:
        print(f"Content analysis error: {e}")
        return None, None

def process_results(query):
    """Process a query and return structured search results."""
    create_temp_folder()
    print("🔍 Searching Google...")
    search_results = google_search(query)

    if not search_results:
        print("❌ No search results found")
        return {
            "error": "No relevant results found",
            "query": query,
            "best_url": "",
            "headlines": [],
            "contents": []
        }

    print(f"✅ Found {len(search_results)} results: {search_results}")

    successful_urls = []
    all_pages_sections = []

    for url in search_results:
        print(f"🌍 Fetching content from: {url}")
        html = fetch_web_content(url)

        if not html:
            print(f"⚠️ Skipping {url} (No content found)")
            continue

        sections = extract_structured_sections(html)
        if not sections:
            print(f"⚠️ Skipping {url} (No relevant sections found)")
            continue

        all_pages_sections.append(sections)
        successful_urls.append(url)

    if not successful_urls:
        print("❌ No valid pages found")
        return {
            "error": "No relevant results found",
            "query": query,
            "best_url": "",
            "headlines": [],
            "contents": []
        }

    selected_content, best_url = rank_and_select_content(query, all_pages_sections, successful_urls)

    if not selected_content or not best_url:
        print("❌ No relevant content found")
        return {
            "error": "No relevant results found",
            "query": query,
            "best_url": "",
            "headlines": [],
            "contents": []
        }

    print(f"✅ Best Result from: {best_url}")

    return {
        "query": query,
        "best_url": best_url,
        "headlines": [f"**{section['heading']}**" for section in selected_content if section['content']],

        "contents": [" ".join(section['content'].split()[:300]) + "..." for section in selected_content if section['content']]
        # "contents": [section['content'] for section in selected_content if section['content']]
    }


    # Prepare structured JSON output
    output = {
        "best_url": best_url,
        "headlines": [f"**{section['heading']}**" for section in selected_content if section['content']],
        "contents": [section['content'] for section in selected_content if section['content']]
    }

    delete_temp_files()
    return output
