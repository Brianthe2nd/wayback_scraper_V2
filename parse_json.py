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
        "retweet": "",
        "author":tweet_json.get("user").get("screen_name") 
    }

json_str =json_str = r'''{
  "contributors": null,
  "coordinates": null,
  "created_at": "Sat Jun 20 16:49:45 +0000 2020",
  "display_text_range": [27, 76],
  "entities": {
    "hashtags": [],
    "symbols": [],
    "urls": [],
    "user_mentions": [
      {
        "id": 1183184898070405120,
        "id_str": "1183184898070405120",
        "indices": [0, 15],
        "name": "\ud83c\udff3\ufe0f\u200d\ud83c\udf08 Soap \ud83c\udff3\ufe0f\u200d\ud83c\udf08",
        "screen_name": "Soap_The_Scrub"
      },
      {
        "id": 1269340565050703873,
        "id_str": "1269340565050703873",
        "indices": [16, 26],
        "name": "Justin",
        "screen_name": "PocoRolve"
      }
    ]
  },
  "favorite_count": 0,
  "favorited": false,
  "filter_level": "low",
  "geo": null,
  "id": 1274383951738503169,
  "id_str": "1274383951738503169",
  "in_reply_to_screen_name": "Soap_The_Scrub",
  "in_reply_to_status_id": 1274382689483841536,
  "in_reply_to_status_id_str": "1274382689483841536",
  "in_reply_to_user_id": 1183184898070405120,
  "in_reply_to_user_id_str": "1183184898070405120",
  "is_quote_status": false,
  "lang": "en",
  "place": null,
  "quote_count": 0,
  "reply_count": 0,
  "retweet_count": 0,
  "retweeted": false,
  "source": "Twitter Web App",
  "text": "@Soap_The_Scrub @PocoRolve \u201cI don\u2019t know any of them so fuck you\u201d\n\n?????????",
  "timestamp_ms": "1592671785660",
  "truncated": false,
  "user": {
    "contributors_enabled": false,
    "created_at": "Fri Mar 23 20:26:52 +0000 2018",
    "default_profile": false,
    "default_profile_image": false,
    "description": "\ud83c\udf1fHyena\ud83c\udf1fMINOR\ud83c\udf1fBLM\ud83c\udf1fACAB\ud83c\udf1fPFP: @Blu_Folf\ud83c\udf1fHe/They NB\ud83c\udf1fCo-Owner of @DailyYeens\ud83c\udf1fBanner: @BirdWithThWord\ud83c\udf1f",
    "favourites_count": 24005,
    "followers_count": 2878,
    "friends_count": 397,
    "geo_enabled": false,
    "id": 977280541316628480,
    "id_str": "977280541316628480",
    "lang": null,
    "listed_count": 39,
    "location": "potoe",
    "name": "\ud83c\udf1fNEKRO\ud83c\udf1f",
    "profile_background_color": "000000",
    "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
    "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
    "profile_banner_url": "https://pbs.twimg.com/profile_banners/977280541316628480/1592429715",
    "profile_image_url": "http://pbs.twimg.com/profile_images/1272335858163544066/-s0Zpzi5_normal.jpg",
    "profile_image_url_https": "https://pbs.twimg.com/profile_images/1272335858163544066/-s0Zpzi5_normal.jpg",
    "profile_link_color": "981CEB",
    "protected": false,
    "screen_name": "NekroVEVO",
    "statuses_count": 12218,
    "translator_type": "none",
    "url": "https://www.youtube.com/channel/UC8Kg_ZpkoMvJzOAGuzyeq6A?view_as=subscriber",
    "verified": false
  }
}'''

if __name__ == "__main__":
    import json
    
    json_data = json.loads(json_str)
    tweet = parse_tweet_json(json_data,245271)
    print(tweet)