import json
import os
import hashlib


class URLShortener:
    def __init__(self, db_file="short_urls.json"):
        self.db_file = db_file
        self.urls = self._load()

    def _load(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.db_file, "w") as f:
            json.dump(self.urls, f, indent=2)

    def _normalize(self, url):
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        return url

    def _generate_code(self, url, length=6):
        """Generate a code from a hash of the URL, so the same URL always gets the same code."""
        hash_object = hashlib.md5(url.encode())
        return hash_object.hexdigest()[:length]

    def shorten(self, long_url):
        long_url = self._normalize(long_url)
        code = self._generate_code(long_url)

        # handle rare hash collisions between different URLs
        while code in self.urls and self.urls[code]["original_url"] != long_url:
            long_url_variant = long_url + "#"
            code = self._generate_code(long_url_variant)

        if code not in self.urls:
            self.urls[code] = {"original_url": long_url, "clicks": 0}
            self._save()

        return code

    def expand(self, code):
        entry = self.urls.get(code)
        if entry:
            entry["clicks"] += 1
            self._save()
            return entry["original_url"]
        return None

    def get_clicks(self, code):
        entry = self.urls.get(code)
        return entry["clicks"] if entry else None

    def list_all(self):
        return self.urls


def main():
    shortener = URLShortener()

    while True:
        print("\n--- URL Shortener (OOP + hash-based codes) ---")
        print("1. Shorten a URL")
        print("2. Expand a short URL")
        print("3. Check click count")
        print("4. List all URLs")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            long_url = input("Enter the long URL: ").strip()
            code = shortener.shorten(long_url)
            print(f"Shortened URL: short.ly/{code}")

        elif choice == "2":
            code = input("Enter the short code: ").strip()
            original = shortener.expand(code)
            if original:
                print(f"Original URL: {original}")
            else:
                print("Short code not found.")

        elif choice == "3":
            code = input("Enter the short code: ").strip()
            clicks = shortener.get_clicks(code)
            if clicks is not None:
                print(f"Clicks: {clicks}")
            else:
                print("Short code not found.")

        elif choice == "4":
            urls = shortener.list_all()
            if not urls:
                print("No URLs shortened yet.")
            else:
                print("\nAll shortened URLs:")
                for code, info in urls.items():
                    print(f"short.ly/{code}  ->  {info['original_url']}  (clicks: {info['clicks']})")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()