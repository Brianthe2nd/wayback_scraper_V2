import re
from typing import List, Dict, Optional
import os
import json
from tqdm import tqdm
import sys
import traceback
from parse_html import parse_html
from downloads import update_xlsx,update_errors_xlsx,process_errors_tweets
from contextlib import redirect_stdout, redirect_stderr
from bs4 import BeautifulSoup

TWITTER_STATUS_RE = re.compile(r'https?://(?:www\.)?twitter\.com/[^/\s]+/status/\d+')
ERROR_RE = re.compile(r'Date format not recognized\s*:?\s*(.*)', re.IGNORECASE)


def get_all_twitter_links(file_path):
    """
    Extract all Twitter status links from the given txt file.
    
    Returns a list of links as strings.
    """
    links = []
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            match = TWITTER_STATUS_RE.match(line)
            if match:
                links.append(match.group(0))
    return links

def get_links_with_datetime_errors(file_path: str) -> List[Dict[str, Optional[str]]]:
    """
    Read the file and return a list of dicts for twitter status links that have
    a following "Date format not recognized" ValueError in the subsequent lines.
    
    Each dict has keys:
      - 'link' : the twitter status URL (string)
      - 'error_line' : the full line that contains "Date format not recognized" (string) or None
      - 'unrecognized_datetime' : the datetime text after the colon in that error line (string) or None
    """
    results = []
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        m = TWITTER_STATUS_RE.match(line)
        if m:
            link = m.group(0)
            # look forward until next twitter status link or EOF
            j = i + 1
            found_error_line = None
            found_dt = None
            while j < n:
                nxt = lines[j].strip()
                # stop if we encounter another twitter status link (stop searching for this link)
                if TWITTER_STATUS_RE.match(nxt):
                    break
                # check for the date-format error line
                m_err = ERROR_RE.search(nxt)
                if m_err:
                    found_error_line = nxt
                    # group(1) is what's after the colon, may be empty
                    dt_text = m_err.group(1).strip()
                    found_dt = dt_text if dt_text else None
                    break
                j += 1

            if found_error_line:
                results.append(link)

            # advance i to j (so we don't re-scan the same traceback lines)
            i = j
        else:
            i += 1

    return results

def get_tweet_array(tweet_link,path):
    # print("tHE path is ",path)
    path_parts = path.split("\\")
    folder =path_parts[-2]
    error_tweets_name_parts = path_parts[-1].split("_")
    error_tweets_name = error_tweets_name_parts[0]
    
    json_captures_path = os.path.join(folder,error_tweets_name+"_captures.json")
    with open (json_captures_path,"r") as file:
        json_captures = json.load(file)
    
    for array in json_captures:
        if array[0] == tweet_link:
            return array,error_tweets_name

def get_html_file_path(folder_name , link):
    # https://twitter.com/ThisBeNekro/status/1335786644541120513
    link_id = link.split("/")[-1]
    archives_path = os.path.join(folder_name,folder_name+"_archive")
    html_files = os.listdir(archives_path)
    for html in html_files:
        if link_id in html:
            return os.path.join(archives_path,html)
    




def process_errors(error_path):
    date_errors = get_links_with_datetime_errors(error_path)

    for link in tqdm(date_errors, desc="Processing datetime errors", unit="tweet"):
        try:
            array, folder_name = get_tweet_array(link, error_path)
            html_file_path = get_html_file_path(folder_name, link)

            with open(html_file_path, "r", encoding="utf-8") as file:
                html_text = file.read()

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_text, "html.parser")
            # print("\n")
            # print("The html file path is :")
            # print(html_file_path)
            html_file_path = html_file_path.split("\\")[-1]
            
            tweet = parse_html(soup, html_file_path)

            update_xlsx(project_dir=folder_name, tweet=tweet)
            update_errors_xlsx(project_dir=folder_name, tweet=tweet)
            print("\n")

        except Exception as e:
            print(f"Error processing datetime error link {link}: {e}")
            traceback.print_exc()

    all_errors = get_all_twitter_links(error_path)
    other_errors =[]
    for error in all_errors:
        if error not in date_errors:
            other_errors.append(error)
    
    for link in tqdm(other_errors, desc="Processing all errors", unit="tweet"):
        try:
            array, folder_name = get_tweet_array(link,error_path)
            process_errors_tweets(array, folder_name, os.path.join(folder_name,folder_name+"_archive"))
        except Exception as e:
            print(f"Error processing general error link {link}: {e}")
            traceback.print_exc()
        print("\n")


# Example usage:
if __name__ == "__main__":
    date_errors = get_links_with_datetime_errors("voltfolf_error_tweets.txt")
    error_path = "voltfolf\\voltfolf_error_tweets.txt"
    import sys
    
    for link in tqdm(date_errors, desc="Processing",file=sys.stderr):
        array,folder_name = get_tweet_array(link,error_path)
        html_file_path = get_html_file_path(folder_name,link)
        # print("The html file path is : ",html_file_path)
        
        with open(html_file_path,"r",encoding="utf-8") as file:
            html_text = file.read()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_text,"html.parser")
        tweet = parse_html(soup,html_file_path)
        update_xlsx(project_dir=folder_name,tweet=tweet)
        update_errors_xlsx(project_dir=folder_name,tweet=tweet)
        print("\n")
        
        
        # print("Error line:", m["error_line"])
        # print("Unrecognized datetime:", m["unrecognized_datetime"])
        # print("-" * 60)
    all_errors = get_all_twitter_links("voltfolf_error_tweets.txt")
    for link in all_errors:
        if link not in date_errors:
            array,folder_name = get_tweet_array(link)
            process_errors_tweets(array,folder_name,folder_name)
            
            
