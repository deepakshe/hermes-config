import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def fetch_trending(topic=None, days=7, limit=10):
    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    query = f"pushed:>{since_date}"
    if topic:
        query += f" topic:{topic}"
    else:
        query += " stars:>100"
        
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}"
    
    try:
        r = requests.get(url, headers={"User-Agent": "AntigravityScout"}, timeout=15)
        if r.status_code == 200:
            items = r.json().get("items", [])
            repos = []
            
            print(f"\n=======================================================")
            print(f" 🔥 TOP TRENDING GITHUB REPOSITORIES (Past {days} Days)")
            if topic:
                print(f" 🎯 Topic Filter: '{topic}'")
            print(f"=======================================================\n")
            
            for i, item in enumerate(items, 1):
                lic = item.get("license")
                lic_name = lic.get("name") if lic else "No License (Check Repo)"
                is_free = lic and ("mit" in lic_name.lower() or "apache" in lic_name.lower() or "gpl" in lic_name.lower() or "bsd" in lic_name.lower())
                
                repo_info = {
                    "rank": i,
                    "name": item.get("full_name"),
                    "stars": item.get("stargazers_count"),
                    "forks": item.get("forks_count"),
                    "description": item.get("description"),
                    "license": lic_name,
                    "is_free_license": bool(is_free),
                    "url": item.get("html_url"),
                    "homepage": item.get("homepage"),
                    "language": item.get("language")
                }
                repos.append(repo_info)
                
                status_icon = "🟢 100% Free / Open Source" if is_free else "🟡 License: " + lic_name
                print(f"#{i} | ⭐ {repo_info['stars']:,} | {repo_info['name']}")
                print(f"    {status_icon} | Lang: {repo_info['language'] or 'Multi'}")
                print(f"    📖 {repo_info['description'] or 'No description'}")
                print(f"    🔗 {repo_info['url']}\n")
                
            return repos
        else:
            print(f"GitHub API Error: {r.status_code}")
    except Exception as e:
        print(f"Error fetching trending repos: {e}")
    return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Trending GitHub Repositories")
    parser.add_argument("--topic", type=str, help="Filter by topic (e.g. ai, video, llm, agent)")
    parser.add_argument("--days", type=int, default=7, help="Days range (default: 7)")
    parser.add_argument("--limit", type=int, default=5, help="Number of repos to fetch")
    args = parser.parse_args()
    
    fetch_trending(topic=args.topic, days=args.days, limit=args.limit)
