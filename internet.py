import socket

def has_internet(host="8.8.8.8", port=53, timeout=3) -> bool:
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except OSError:
        return False


# Example usage:
if __name__ == "__main__":
    if has_internet():
        print("Internet connection is available ✅")
    else:
        print("No internet connection ❌")
