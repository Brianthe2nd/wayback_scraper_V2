# Twitter Wayback Capture Downloader 🕊️

A Python script to find and download historical captures of a Twitter profile from the [Internet Archive's Wayback Machine](https://web.archive.org/).

---

## ✨ Features

* **Targeted Downloads**: Fetch captures for any public Twitter handle.
* **Date Filtering**: Specify a start and end date (`YYYYMM`) to narrow your search.
* **Flexible Data Handling**: For existing data, choose to **(O)verwrite**, **(S)kip**, or **(A)ppend**.
* **Organized Output**: Automatically saves captures, logs, and data into a clean, user-specific directory structure.
* **User-Friendly Interface**: Choose between a clean progress bar (`tqdm`) or verbose terminal logging during the download process.

---

## 🚀 Setup

Before running, you need to install the required dependencies. Please follow one of the guides below:

* 📄 **[long_setup.md](long_setup.md)** — A detailed, step-by-step installation guide.
* ⚡ **[simple_setup.md](simple_setup.md)** — A quick-start guide for experienced users.

---

## ▶️ How to Run

1.  **Navigate to the project directory** in your terminal:
    ```bash
    cd path/to/your/project
    ```

2.  **Execute the script** using Python:
    ```bash
    python main.py
    ```

### Script Workflow

When you launch the script, it will guide you through the following steps:

1.  **Enter Inputs**: You'll be prompted to provide:
    * The Twitter **username** (without the `@` symbol).
    * A **start date** and **end date** in `YYYYMM` format.

2.  **Handle Existing Data**: The script checks if a capture file (`{username}/{username}_captures.json`) already exists. If it does, you'll be asked how to proceed:
    * `(O)verwrite`: Delete the existing file and create a new one.
    * `(S)kip`: Abort the operation and keep the existing file.
    * `(A)ppend`: Add new, unique captures to the existing file.

3.  **Fetch & Process**:
    * The script generates a timemap URL and fetches the capture data from the Wayback Machine.
    * It then asks if you want to display a **progress bar** (`y`) or see **live logs** (`n`) in the terminal while it downloads and processes the archives.
    * Regardless of your choice, all processing logs are saved to a timestamped file for later review.

---

## 📂 Output Structure

{username}/
├── archives/                    # Stores the downloaded archive files
├── logs/                        # Contains timestamped process logs
│   └── {YYYYMMDD_HHMMSS}_{username}_process.log
└── {username}_captures.json     # A JSON list of all captures from the Wayback Machine

The script organizes all generated files into a folder named after the Twitter handle:

The `{username}_captures.json` file contains metadata for each snapshot, including fields like `original`, `mimetype`, `timestamp`, and `uniqcount`.

---

## 📝 Example Run

Here’s what a typical session looks like:

```bash
$ python main.py

Enter the username (Twitter handle): Nekrovevo
⚠️ File 'Nekrovevo/Nekrovevo_captures.json' already exists.
Do you want to (O)verwrite, (S)kip, or (A)ppend new data into it? [O/S/A]: A
Enter start date (YYYYMM): 202001
Enter end date (YYYYMM): 202012

Generated URL for (@Nekrovevo):
[https://web.archive.org/web/timemap/json?url=twitter.com/Nekrovevo&from=202001&to=202012&matchType=prefix&output=json](https://web.archive.org/web/timemap/json?url=twitter.com/Nekrovevo&from=202001&to=202012&matchType=prefix&output=json)

Show progress bar instead of logs [y/n]: y
📜 Logs saved to Nekrovevo/logs/20250907_163544_Nekrovevo_process.log

Processing archives...
100%|█████████████████████████████████| 152/152 [01:12<00:00, 2.11it/s]

✅ Process complete.






