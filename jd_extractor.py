import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        # Clean extra spaces
        cleaned_text = " ".join(text.split())

        return cleaned_text

    except Exception as e:
        print("JD URL extraction error:", e)
        return ""
