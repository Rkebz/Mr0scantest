import http.client
import argparse
import urllib.parse
import threading

def fuzz(url, paths, payloads):
    for path in paths:
        for payload in payloads:
            try:
                full_url = url + path + payload
                connection = http.client.HTTPConnection(urllib.parse.urlparse(full_url).netloc)
                connection.request("GET", urllib.parse.urlparse(full_url).path)
                response = connection.getresponse()
                if response.status != 404:  # Check if the response is not a "Not Found" error
                    print(f"Vulnerable URL: {full_url} - Status Code: {response.status}")
                connection.close()
            except Exception as e:
                print(f"Error with {full_url}: {e}")

def read_wordlist(wordlist):
    try:
        with open(wordlist, 'r') as f:
            paths = f.read().splitlines()
    except Exception as e:
        print(f"Error reading wordlist: {e}")
        return []
    return paths

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple HTTP Fuzzer with Multithreading")
    parser.add_argument("url", help="Target URL (e.g., http://example.com/)")
    parser.add_argument("wordlist", help="Path to wordlist file for paths")
    parser.add_argument("payloads", help="Path to wordlist file for payloads")
    parser.add_argument("--threads", type=int, default=20, help="Number of threads (default: 20)")

    args = parser.parse_args()

    url = args.url
    paths = read_wordlist(args.wordlist)
    payloads = read_wordlist(args.payloads)

    # Split paths into chunks for threading
    chunks = [paths[i::args.threads] for i in range(args.threads)]

    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=fuzz, args=(url, chunk, payloads))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
