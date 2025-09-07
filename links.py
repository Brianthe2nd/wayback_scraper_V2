import os
import time
import urllib.parse
import requests
import json
import itertools
import sys
import time
import threading

headers = {
  'accept': 'application/json, text/javascript, */*; q=0.01',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'no-cache',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'referer': 'https://web.archive.org/web/202009*/twitter.com/NekroVevo*',
  'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest',
  'Cookie': 'wb-p-SERVER=wwwb-app224; wb-cdx-SERVER=wwwb-app208; donation-identifier=bea4320a4776fb2c84a3999cc69ec714; wb-cdx-ui-SERVER=wwwb-app205; view-search=tiles; showdetails-search=; abtest-identifier=aa344537511d7d4184bf39f0bc72bb24'
}


def build_timemap_url():
    """
    Prompt user for details and construct a Wayback Machine timemap URL.
    
    Returns:
        tuple: (Generated URL, username, output_file, mode)
        mode = "overwrite", "skip", or "append"
    """
    username = input("Enter the username (Twitter handle): ").strip()
    output_file = os.path.join(username,f"{username}_captures.json")

    # Check early if file exists
    if not os.path.exists(username):
        os.makedirs(username)

    
    if os.path.exists(output_file):
        print(f"\n⚠️ File '{output_file}' already exists.")
        choice = input("Do you want to (O)verwrite, (S)kip, or (A)ppend new data into it? [O/S/A]: ").strip().lower()
        
        if choice == "s":
            print("Skipping download. Using existing file.")
            return None, username, output_file, "skip"
        elif choice == "a":
            mode = "append"
            print(f"Appending new data into: {output_file}")
        else:
            mode = "overwrite"
            print("Overwriting existing file.")
    else:
        mode = "overwrite"

    # Only ask for date range if we’re actually downloading
    start_date = input("Enter start date (YYYYMM): ").strip()
    end_date = input("Enter end date (YYYYMM): ").strip()

    encoded_url = urllib.parse.quote(f"twitter.com/{username}")
    unique_param = str(int(time.time() * 1000))

    url = (
        f"https://web.archive.org/web/timemap/json"
        f"?url={encoded_url}"
        f"&matchType=prefix"
        f"&collapse=urlkey"
        f"&output=json"
        f"&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount"
        f"&filter=!statuscode%3A%5B45%5D.."
        f"&limit=10000000"
        f"&from={start_date}"
        f"&to={end_date}"
        f"&_={unique_param}"
    )

    print(f"\nGenerated URL for (@{username}):\n{url}\n")
    return url, username, output_file, mode


def spinner_task(stop_event):
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    while not stop_event.is_set():
        sys.stdout.write("\r⏳ Fetching data... " + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r✅ Done fetching data!   \n")

def get_links():
    while True:  # loop until successful
        url, username, output_file, mode = build_timemap_url()

        # If user chose skip
        if url is None and mode == "skip":
            try:
                with open(output_file, "r", encoding="utf-8") as f:
                    rows = json.load(f)
                print(f"📂 Loaded {len(rows)} entries from {output_file}")
                return rows
            except FileNotFoundError:
                print("⚠️ No saved data found. Please fetch data first.")
                continue

        # Start spinner
        stop_event = threading.Event()
        t = threading.Thread(target=spinner_task, args=(stop_event,))
        t.start()

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            new_rows = response.json()

            stop_event.set()
            t.join()

            if not new_rows:  # empty response
                print(f"⚠️ No data returned for @{username}. Please check the username.")
                confirm = input("Do you want to retry? (y/n): ").strip().lower()
                if confirm == "y":
                    continue
                else:
                    return []
            
        except requests.exceptions.RequestException as e:
            stop_event.set()
            t.join()
            print(f"\n❌ Error fetching data: {e}")
            confirm = input("Do you want to try again? (y/n): ").strip().lower()
            if confirm == "y":
                continue
            else:
                return []
        except ValueError:
            stop_event.set()
            t.join()
            print(f"⚠️ Invalid data returned for @{username}.")
            confirm = input("Do you want to try again? (y/n): ").strip().lower()
            if confirm == "y":
                continue
            else:
                return []

        # Merge or overwrite
        appended_count = 0
        if mode == "append" and os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                existing_rows = json.load(f)

            seen = set()
            merged = []
            for row in existing_rows + new_rows:
                key = (row[0], row[2]) if isinstance(row, list) and len(row) > 2 else tuple(row)
                if key not in seen:
                    seen.add(key)
                    merged.append(row)

            appended_count = len(merged) - len(existing_rows)
            rows = merged
        else:
            rows = new_rows
            appended_count = len(new_rows)

        # Save file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)

        print(f"📊 Total tweets: {len(rows)}")
        print(f"➕ New tweets added: {appended_count}")
        print(f"💾 Saved to {output_file}")

        return output_file,username
      
if __name__ == "__main__":
  get_links()