import os
import base64
import requests

INPUT_FILE = "inputs.txt"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "merged.txt")


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


def main():
    # اگر output وجود داره ولی فایل هست، پاکش کن
    if os.path.exists(OUTPUT_DIR) and not os.path.isdir(OUTPUT_DIR):
        os.remove(OUTPUT_DIR)

    # ساخت پوشه اگر نبود
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    merged_lines = []

    with open(INPUT_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        print(f"Fetching: {url}")
        content = fetch_url(url)
        if not content:
            continue

        # اگر Base64 بود decode کن
        if is_base64(content):
            try:
                content = base64.b64decode(content).decode("utf-8")
            except:
                pass

        lines = content.splitlines()

        for line in lines:
            clean = line.strip()
            if clean:
                merged_lines.append(clean)

    # حذف موارد تکراری
    merged_lines = list(dict.fromkeys(merged_lines))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_lines))

    print(f"Done. {len(merged_lines)} lines saved.")


if __name__ == "__main__":
    main()
