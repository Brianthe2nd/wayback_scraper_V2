import time
import requests
import traceback
import json
from bs4 import BeautifulSoup
import os

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
    response.raise_for_status()  # Raise exception if request failed
    
    return response.text

