import os 
from process_errors import process_errors

def find_error_tweets_files():
    """Walk through all folders in the CWD and return paths to files ending with 'error_tweets.txt'."""
    matches = []
    cwd = os.getcwd()
    
    for root, _, files in os.walk(cwd):
        for file in files:
            if file.endswith("error_tweets.txt"):
                matches.append(os.path.join(root, file))
    
    return matches


# def process_errors():
    


if __name__ == "__main__":
    matches = find_error_tweets_files()
    
    if not matches:
        print("No error_tweets.txt files found.")
    elif len(matches) == 1:
        file = matches[0]
        print(f"Only one match found: {file}")
    else:
        print("Multiple matches found:")
        for idx, path in enumerate(matches, start=1):
            print(f"{idx}. {path}")
        
        while True:
            try:
                choice = int(input(f"Select a file to process (1-{len(matches)}): "))
                if 1 <= choice <= len(matches):
                    file = matches[choice - 1]
                    print(f"You selected: {file}")
                    break
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    process_errors(file)

    # print(matches)