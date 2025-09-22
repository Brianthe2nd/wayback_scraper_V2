# from parse_html import parse_html
from bs4 import BeautifulSoup
import re
from datetime import datetime
import traceback


def get_archive_link(soup):
    href_value2 = soup.select_one('link[rel="canonical"]')["href"]
    
    return href_value2

def parse_twitter_datetime(date_str: str) -> datetime:
    try:
        formats = [
            "%I:%M %p - %d %b %Y",     # e.g. "9:14 PM - 28 Sep 2020"
            "%H:%M - %d. %b %Y",       # e.g. "21:14 - 28. Sep 2020"
            "%H.%M - %d. %b %Y",       # e.g. "14.06 - 30. Sep 2020" (Finnish style)
        ]
        
        # Normalize localized month abbreviations (German, Finnish etc.)
        replacements = {
            # German
            "Jan.": "Jan", "Feb.": "Feb", "März": "Mar", "Apr.": "Apr",
            "Mai": "May", "Juni": "Jun", "Juli": "Jul", "Aug.": "Aug",
            "Sept.": "Sep", "Okt.": "Oct", "Nov.": "Nov", "Dez.": "Dec",
            # Finnish
            "tammi": "Jan", "helmi": "Feb", "maalis": "Mar", "huhti": "Apr",
            "touko": "May", "kesä": "Jun", "heinä": "Jul", "elo": "Aug",
            "syysk.": "Sep", "lokak.": "Oct", "marras": "Nov", "joulu": "Dec",
        }
        for de, en in replacements.items():
            if de in date_str:
                date_str = date_str.replace(de, en)
                break
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
    except:
        error = traceback.format_exc
        print("Error while processing date")
        print(error)
        return None
        
    # raise ValueError(f"Date format not recognized: {date_str}")


# Example
# print(parse_twitter_datetime("14.06 - 30. syysk. 2020"))
# # → datetime.datetime(2020, 9, 30, 14, 6)

def parse_username(strong_tag):
    parts = []
    for child in strong_tag.children:
        # If it's plain text, keep it
        if child.name is None:
            if child.strip():
                parts.append(child.strip())
        # If it's the hidden span (contains real emoji)
        elif child.get("class") and "visuallyhidden" in child["class"]:
            emoji = child.get_text(strip=True)
            if emoji:
                parts.append(emoji)
        # Ignore the image-based emoji spans (duplicates)
        else:
            continue

    # Join all pieces together
    username = "".join(parts)
    return username



def parse_mobile_html(soup,title="none",title_passed = False,retweet = False):
 

    link_container = soup.select_one("div#react-root")
    tweet_text_elem = link_container.select_one('div[itemprop="articleBody"]')


    # Replace emoji <img> tags with their alt text (the actual emoji character)
    for img in tweet_text_elem.find_all("img", class_="Emoji"):
        if img.has_attr("alt"):
            img.replace_with(img["alt"])

    # Now extract cleaned text
    tweet_text = tweet_text_elem.get_text().strip().replace('\n', '')
    tweet_text = re.sub(r"\s+", " ", tweet_text).strip()

    
    time_elem = soup.select_one("meta[itemprop='datePublished']")
    time_text = time_elem.get("content")
    time_text = datetime.strptime(time_text, "%Y-%m-%dT%H:%M:%S.%fZ")
    # username = parse_username(link_container.select_one("strong.fullname"))
    username_elem = soup.select_one("meta[itemprop='givenName']")
    username = username_elem.get("content")
    if retweet:
        retweet_username = link_container.select_one("span.username > b").get_text().strip()
    else:
        retweet_username = ""
    
    mentions = None
    # if True:
    #     reply = False
    # else:
    #     reply = True
    #     mentions = link_container.select_one("div.ReplyingToContextBelowAuthor span.username > b")
    #     if mentions is None:
    #         mentions_container = link_container.select_one("span.username > b")
    #         if mentions_container != None:
    #             mentions = mentions_container.get_text().strip()
    #         else:
    #             mentions = username
            
    #     else:
    #         mentions = mentions.get_text().strip()
        
    # quote_container = link_container.select_one("div.QuoteTweet")
    # if quote_container is None:
    #     quote = False
    # else:
    #     quote = True
    #     mentions = quote_container.select_one("span.username > b")
    #     if mentions == None:
    #         mentions_container = link_container.select_one("span.username > b")
    #         if mentions_container != None:
    #             mentions = mentions_container.get_text().strip()
    #         else:
    #             mentions = username
            
    #     else:
    #         mentions = mentions.get_text().strip()
        
    author_elem = soup.select_one("meta[itemprop='additionalName']")
    author = author_elem.get("content")
    # link = get_archive_link(soup)
    # # print("The title is: ",title)
    # if not title_passed:
    #     if  "web.archive.org" not in link and "twitter" in link:
            
    #         timeline = title.split("_")[0]
    #         link = f"https://web.archive.org/web/{timeline}/{link}"
    # else :
    #     link = title   
    link_elem = soup.select_one("meta[itemprop='url']")
    link = link_elem.get("content")     
        
        
    
    image_container = soup.select_one("div[itemprop ='sharedContent']")
    
    if image_container is None:
        image = False
    else:
        image = True
    print("Tweet text:", tweet_text)
    print("Username:", username)
    print("Mentions:",mentions)
    print("Date:",time_text)
    print("Image:",image)
    print("Link:",link)
    print("Quote:",False)
    print("Reply:",False)
    print("Author:",author)
    
    tweet_obj = {
        "tweet_text": tweet_text,
        "username": username,
        "mentions": mentions,
        "date": time_text,
        "image": image,
        "link": link,
        "quote": False,
        "reply": False,
        "retweet": retweet_username,
        "author":author
    }
    
    return tweet_obj

if __name__ == "__main__":
    with open("mobile.html" , "r" ,encoding="utf-8") as file:
        text = file.read()
        
    soup = BeautifulSoup(text,"html.parser")
    tweet = parse_mobile_html(soup,"milf")
