import sys
import json
import argparse
import requests

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def inspect_repo(repo_name):
    clean = repo_name.replace("https://github.com/", "").strip().strip("/")
    url = f"https://api.github.com/repos/{clean}"
    try:
        r = requests.get(url, headers={"User-Agent": "AntigravityStudio"}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            out = {
                "name": data.get("full_name"),
                "stars": data.get("stargazers_count"),
                "forks": data.get("forks_count"),
                "open_issues": data.get("open_issues_count"),
                "description": data.get("description"),
                "license": data.get("license", {}).get("name") if data.get("license") else "Not specified",
                "topics": data.get("topics", []),
                "clone_url": data.get("clone_url")
            }
            print(json.dumps(out, indent=2))
            return out
        else:
            print(f"Error {r.status_code}: Repository not found")
    except Exception as e:
        print(f"Network error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=str, required=True, help="Repo owner/name (e.g. ollama/ollama)")
    args = parser.parse_args()
    inspect_repo(args.repo)
