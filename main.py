from links import get_links
from downloads import process_json_file
import os
import sys
import datetime

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
    output_file,username = get_links()
    archive_folder = os.path.join(username,"archives")
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)
    show_tqdm = input("Show progress bar instead of logs [y/n]: ")
    logs_folder = os.path.join(username,"logs")
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    log_file = os.path.join(logs_folder,f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{username}_process.log")
    if show_tqdm == "y":
        with open(log_file, "w", encoding="utf-8") as f:
            # Redirect stdout and stderr to the log file
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            sys.stdout = f
            sys.stderr = f

            try:
                process_json_file(
                    json_path=output_file,
                    project_dir=username,
                    output_dir=archive_folder,
                    show_tqdm = True
                )
            finally:
                # Restore stdout and stderr back to normal
                sys.stdout = original_stdout
                sys.stderr = original_stderr

        print(f"📜 Logs saved to {log_file}")
    else:
        # process_json_file(json_path=output_file,project_dir=username,output_dir=archive_folder)
        with open(log_file, "w", encoding="utf-8") as f:
            # Redirect stdout and stderr to both terminal and file
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            sys.stdout = Tee(original_stdout, f)
            sys.stderr = Tee(original_stderr, f)

            try:
                process_json_file(
                    json_path=output_file,
                    project_dir=username,
                    output_dir=archive_folder,
                    show_tqdm=False
                )
            finally:
                # Restore stdout and stderr
                sys.stdout = original_stdout
                sys.stderr = original_stderr