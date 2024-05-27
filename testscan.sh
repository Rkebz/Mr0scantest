#!/bin/bash

# Get the website URL from the user
read -p "Please enter the website URL: " target_site

# Start scanning
echo "Starting security scan for website: $target_site"

# Use Nikto tool to perform security scan
nikto_results=$(nikto -h $target_site)

# Check if Nikto found any vulnerabilities
if [[ $nikto_results == *"No vulnerabilities found"* ]]; then
    echo "No vulnerabilities found by Nikto."
else
    echo "Vulnerabilities found by Nikto:"
    echo "$nikto_results"
fi

# Use Nmap tool to perform directory scan
nmap_results=$(nmap --script=http-enum $target_site)

# Check if Nmap found any exposed paths
if [[ $nmap_results == *"Paths discovered"* ]]; then
    echo "Exposed paths found by Nmap:"
    echo "$nmap_results"
else
    echo "No exposed paths found by Nmap."
fi

# Use Dirb tool to perform directory bruteforcing
dirb_results=$(dirb $target_site)

# Check if Dirb found any additional paths
if [[ $dirb_results == *"COMMON"* ]]; then
    echo "Additional paths found by Dirb:"
    echo "$dirb_results"
else
    echo "No additional paths found by Dirb."
fi

# Use Wpscan tool to scan for Wordpress vulnerabilities
wpscan_results=$(wpscan --url $target_site)

# Check if Wpscan found any Wordpress vulnerabilities
if [[ $wpscan_results == *"No vulnerabilities found"* ]]; then
    echo "No Wordpress vulnerabilities found by Wpscan."
else
    echo "Wordpress vulnerabilities found by Wpscan:"
    echo "$wpscan_results"
fi

# Finish scanning
echo "Security scan completed."
