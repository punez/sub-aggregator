import os
import base64
import json
import requests
from datetime import datetime

INPUT_FILE = "inputs.txt"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "merged.json")


def is_base64(data: str) -> bool:
    try:
        base64.b64decode(data, validate=True)
        return True
    except Exception:
        return False


def fetch_url(url):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return r.text.strip()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_content(content):
    # اگر Base64 بود decode کن
    if is_base64(content):
        try:
            content = base64.b64decode(content).decode("utf-8")
        except:
            pass

    # اگر JSON بود parse کن
    try:
        return json.loads(content)
    except:
        return {"raw_lines": content.splitlines()}


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    merged_data = {
        "updated_at": datetime.utcnow().isoformat(),
        "sources": []
    }

    with open(INPUT_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        content = fetch_url(url)
        if not content:
            continue

        parsed = parse_content(content)

        merged_data["sources"].append({
            "url": url,
            "data": parsed
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)

    print("Done. Merged output saved.")


if __name__ == "__main__":
    main()
