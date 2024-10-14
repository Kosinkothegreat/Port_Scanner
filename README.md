# Port_Scanner
A python script that scans for open ports and gives feedback


# How to Use the Port Scanner

Run the Script: Open your terminal or command prompt and navigate to the directory containing port_scanner.py. 
Use the following command structure to run the script:
python port_scanner.py target_ip [options]
target_ip: The IP address or hostname of the target you want to scan.
Options:
-s or --start: Specify the starting port number (default is 1).
-e or --end: Specify the ending port number (default is 1024).

# Example:
To scan all ports:
python port_scanner.py 192.168.1.1

To scan from ports 80 to 100 on a hostname:
python port_scanner.py example.com -s 80 -e 100

# Understanding the Output
Open Ports: The script will print messages like [+] Port 80 is open for each open port found.

Final Summary: After completing the scan, it will list all open ports along with their common service names (if known).




