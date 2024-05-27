#!/bin/bash

# Get the website URL from the user
read -p "Please enter the website URL: " target_site

# Start scanning
echo "Starting security scan for website: $target_site"

# Use Nikto tool to perform security scan
echo "Nikto scan results:"
nikto -h $target_site

# Use Nmap tool to perform directory and vulnerability scan
echo "Nmap scan results:"
nmap -p 80 --script=http-enum $target_site

# Use Dirb tool to perform directory bruteforcing
echo "Dirb scan results:"
dirb $target_site

# Use Gobuster tool to perform directory bruteforcing
echo "Gobuster scan results:"
gobuster dir -u $target_site -w /usr/share/wordlists/dirb/common.txt

# Finish scanning
echo "Security scan completed."
