# Project Setup & Usage Guide ⚙️

This guide will walk you through setting up and running the project for the first time.

---

##  Prerequisites

Before you begin, you must have [Git](https://git-scm.com/downloads) installed on your system.

> **Why Git?** It's a version control system that allows you to clone (download) this project's source code directly from GitHub.

---

## 🛠️ One-Time Installation

Follow these steps to get the project set up on your local machine.

### 1. Open Your Terminal
Open a command-line interface. On Windows, **Git Bash** is highly recommended as it comes with Git and provides a Unix-like environment.

### 2. Clone the Repository
Run the following command to download the project files and navigate into the newly created directory:

```bash
git clone [https://github.com/Brianthe2nd/wayback_scraper_V2.git](https://github.com/Brianthe2nd/wayback_scraper_V2.git)
cd wayback_scraper_V2
```

### 3. Run the Setup Script
Execute the setup script to install all necessary dependencies (like Python packages) automatically.

```bash
./setup.sh
```
> **Note:** If you encounter a permission error on macOS or Linux, you may need to make the script executable first by running `chmod +x setup.sh`.

---

## ▶️ Running the Application

Once the one-time setup is complete, follow these simple steps every time you want to run the application.

1.  **Navigate to the project directory** (if you're not already there):
    ```bash
    cd wayback_scraper_V2
    ```

2.  **Run the main script**:
    ```bash
    python main.py
    ```
    *(Note: Depending on your system's configuration, you may need to use `python3` instead of `python`.)*
