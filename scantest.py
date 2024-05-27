import http.client
import argparse
import urllib.parse
import threading

def fuzz(url, paths, payloads):
    vulnerable_urls_200 = []
    vulnerable_urls_301 = []
    vulnerable_urls_others = []

    for path in paths:
        for payload in payloads:
            try:
                full_url = url + path + payload
                connection = http.client.HTTPConnection(urllib.parse.urlparse(full_url).netloc)
                connection.request("GET", urllib.parse.urlparse(full_url).path)
                response = connection.getresponse()
                if response.status == 200:
                    vulnerable_urls_200.append(full_url)
                elif response.status == 301:
                    vulnerable_urls_301.append(full_url)
                else:
                    vulnerable_urls_others.append(full_url)
                connection.close()
            except Exception as e:
                print(f"Error with {full_url}: {e}")

    with open("vulnerable_urls_200.txt", 'w') as f:
        for url in vulnerable_urls_200:
            f.write(url + '\n')

    with open("vulnerable_urls_301.txt", 'w') as f:
        for url in vulnerable_urls_301:
            f.write(url + '\n')

    with open("vulnerable_urls_others.txt", 'w') as f:
        for url in vulnerable_urls_others:
            f.write(url + '\n')

    print("Vulnerable URLs saved to files.")

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
    parser.add_argument("--threads", type=int, default=20, help="Number of threads (default: 20)")

    args = parser.parse_args()

    url = args.url
    wordlist = args.wordlist

    paths = read_wordlist(wordlist)
    payloads = read_wordlist(wordlist)

    # Split paths into chunks for threading
    chunks = [paths[i::args.threads] for i in range(args.threads)]

    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=fuzz, args=(url, chunk, payloads))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
