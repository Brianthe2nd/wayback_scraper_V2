import re

def emoji_decode(text):
    if text != None:
        decoded = text.encode("utf-16", "surrogatepass").decode("utf-16")
    else :
        return text
    return decoded

from datetime import datetime

def convert_twitter_date(date_str: str) -> str:
    """
    Convert a Twitter-style date string to 'YYYY-MM-DD HH:MM:SS' format.

    Args:
        date_str (str): Date string like "Thu Aug 29 00:54:31 +0000 2019".

    Returns:
        str: Converted date string in "YYYY-MM-DD HH:MM:SS".
    """
    # Parse the Twitter format
    dt = datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
    # Convert to UTC naive datetime
    dt_utc = dt.astimezone(datetime.utcnow().astimezone().tzinfo)
    # Return in desired format
    return dt_utc.strftime("%Y-%m-%d %H:%M:%S")




def parse_tweet_json(tweet_json: dict,timestamp) -> dict:
    # Tweet text (prefer extended_tweet if available)
    if tweet_json.get("truncated") and "extended_tweet" in tweet_json:
        text = tweet_json["extended_tweet"].get("full_text", tweet_json.get("text", ""))
        entities = tweet_json["extended_tweet"].get("entities", {})
    else:
        text = tweet_json.get("text", "")
        entities = tweet_json.get("entities", {})

    # Username (Twitter's "name", not @handle)
    username = tweet_json["user"]["name"]
    text = text.strip().replace('\n', '')
    text = re.sub(r"\s+", " ", text).strip()

    # Mentions (collect @usernames)
    mentions = [m["screen_name"] for m in entities.get("user_mentions", [])]
    mentions_str = ", ".join(mentions) if mentions else None

    # Check for image/media
    image = False
    if "media" in entities:
        for m in entities["media"]:
            if m.get("type") == "photo":
                image = True
                break
    if "extended_entities" in tweet_json and "media" in tweet_json["extended_entities"]:
        for m in tweet_json["extended_entities"]["media"]:
            if m.get("type") == "photo":
                image = True
                break

    # Tweet link (build archive-style or fallback to Twitter URL)
    tweet_id = tweet_json["id_str"]
    screen_name = tweet_json["user"]["screen_name"]
    link = f"https://twitter.com/{screen_name}/status/{tweet_id}"
    link = f"https://web.archive.org/web/{timestamp}/{link}" 

    # Quote + Reply flags
    quote = tweet_json.get("is_quote_status", False)
    reply = bool(tweet_json.get("in_reply_to_status_id"))

    return {
        "tweet_text": emoji_decode(text),
        "username": emoji_decode(username),
        "mentions": emoji_decode(mentions_str),
        "date": convert_twitter_date(tweet_json.get("created_at","Thu Aug 29 00:54:31 +0000 2019")),
        "image": image,
        "link": link,
        "quote": quote,
        "reply": reply,
        "retweet": ""
    }
