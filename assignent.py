import requests
import os
from urllib.parse import urlparse
import hashlib
os.makedirs("Fetched_Images", exist_ok=True)


def fetch_image(url):
    """Download an image from the web and save it in Fetched_Images folder."""
    try:
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)

        # Set headers to mimic a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/116.0.0.0 Safari/537.36"
        }

        # Fetch the image with timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes

        # Check if the response is an image
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type.lower():
            print(f"✗ The URL does not point to an image: {url}")
            return

        # Extract filename from URL or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename or "." not in filename:
            file_ext = content_type.split("/")[-1] if "/" in content_type else "jpg"
            filename = f"downloaded_{hashlib.md5(url.encode()).hexdigest()[:8]}.{file_ext}"

        filepath = os.path.join("Fetched_Images", filename)

        # Prevent duplicates
        if os.path.exists(filepath):
            print(f"✓ Skipped duplicate: {filename}")
            return

        # Save image
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Ask if user wants single or multiple URLs
    urls = input("Please enter one or more image URLs (separated by spaces): ").split()

    for url in urls:
        fetch_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()

