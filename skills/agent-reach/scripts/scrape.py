import os
import sys
import argparse
import requests

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def fetch_via_jina(url):
    jina_url = f"https://r.jina.ai/{url}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(jina_url, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.text
        else:
            return f"Error: Jina Reader returned status code {r.status_code}"
    except Exception as e:
        return f"Network error fetching URL: {e}"

def main():
    parser = argparse.ArgumentParser(description="Custom Scraping Extension for Agent-Reach")
    parser.add_argument("--reddit", type=str, help="Reddit thread URL or query")
    parser.add_argument("--linkedin", type=str, help="LinkedIn profile URL")
    args = parser.parse_args()
    
    if args.reddit:
        url = args.reddit
        if not url.startswith("http"):
            url = f"https://www.reddit.com/r/all/search/?q={url}"
        print(f"Scraping Reddit context via Jina Reader...")
        result = fetch_via_jina(url)
        print(result[:6000])
        
    elif args.linkedin:
        url = args.linkedin
        print(f"Scraping LinkedIn profile context via Jina Reader...")
        result = fetch_via_jina(url)
        print(result[:6000])
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
