from links import get_links
from downloads import process_json_file
import os
import sys
from datetime import datetime
import sys, os, json, traceback
from contextlib import redirect_stdout, redirect_stderr

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()  # ensure real-time writing

    def flush(self):
        for f in self.files:
            f.flush()



if __name__ == "__main__":
    output_file, username = get_links()
    archive_folder = os.path.join(username, "archives")
    os.makedirs(archive_folder, exist_ok=True)

    show_tqdm = input("Show progress bar instead of logs [y/n]: ").lower().strip()

    logs_folder = os.path.join(username, "logs")
    os.makedirs(logs_folder, exist_ok=True)

    log_file = os.path.join(
        logs_folder, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{username}_process.log"
    )

    if show_tqdm == "y":
        with open(log_file, "w", encoding="utf-8") as f:
            # Redirect only stdout into file
            with redirect_stdout(f):
                try:
                    process_json_file(
                        json_path=output_file,
                        project_dir=username,
                        output_dir=archive_folder,
                        show_tqdm=True,
                    )
                except Exception as e:
                    # Explicitly write error to both terminal and log
                    err_msg = traceback.format_exc()
                    sys.stderr.write(err_msg)   # show in terminal
                    f.write(err_msg)            # save in log

        print(f"📜 Logs + errors saved to {log_file}")

    else:
        with open(log_file, "w", encoding="utf-8") as f, redirect_stdout(f), redirect_stderr(f):
            process_json_file(
                json_path=output_file,
                project_dir=username,
                output_dir=archive_folder,
                show_tqdm=False,
            )

        print(f"📜 Logs saved to {log_file}")
