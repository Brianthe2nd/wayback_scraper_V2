import time
import requests
import traceback
import json
from bs4 import BeautifulSoup
import os
import re


def fetch_html_after_delay(url: str, delay: int = 10) -> str:
    """
    Fetch HTML content from a given URL after waiting a specified delay.

    Args:
        url (str): The URL to fetch.
        delay (int): Delay in seconds before fetching (default: 10s).

    Returns:
        str: The HTML content of the page.
    """
    # Wait before making request
    time.sleep(delay)
    
    # Fetch HTML
    response = requests.get(url, timeout=20)  # 20s timeout safeguard
    print(response.status_code)
    response.raise_for_status()  # Raise exception if request failed
    
    return response.text


def extract_redirect_on_302(html: str) -> str | None:
    """
    Checks for 'Got an HTTP 302 response at crawl time' and 'Redirecting to...'
    inside <div id="error">. If both exist, return the redirect link.
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
        error_div = soup.find("div", id="error")
        if not error_div:
            return None

        # Look for the two messages
        has_302 = error_div.find("p", class_="code shift red", string="Got an HTTP 302 response at crawl time")
        has_redirecting = error_div.find("p", class_="code", string="Redirecting to...")

        if not (has_302 and has_redirecting):
            return None

        # Try extracting from <script>
        script = error_div.find("script", text=re.compile(r'document\.location\.href'))
        if script:
            match = re.search(r'document\.location\.href\s*=\s*"([^"]+)"', script.string)
            if match:
                return match.group(1)

        # Fallback: impatient link
        impatient_link = error_div.select_one("p.impatient a")
        if impatient_link and impatient_link.get("href"):
            return impatient_link["href"]

        return None
    except:
        return None



if __name__ == "__main__":
    html = fetch_html_after_delay(url = "https://web.archive.org/web/20201207053725/https://twitter.com/SketchyJagger/status/1335801367563173892",delay=1)
    with open("index.html","w",encoding="utf-8")as file:
        file.write(html)