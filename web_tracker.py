import requests
from bs4 import BeautifulSoup
import hashlib
import difflib

def fetch_website_content(url):
    """Fetches and returns the text content of a website."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def generate_content_hash(content):
    """Generates a SHA256 hash of the given content."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def has_website_updated(url, old_hash):
    """Checks if the website content has changed by comparing hashes."""
    current_content = fetch_website_content(url)
    current_hash = generate_content_hash(current_content)
    return current_hash != old_hash, current_hash, current_content

def find_content_differences(old_content, new_content):
    """Finds differences between the old and new content."""
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()
    diff = difflib.unified_diff(old_lines, new_lines, fromfile='old', tofile='new', lineterm='')
    differences = '\n'.join(diff)
    return differences
