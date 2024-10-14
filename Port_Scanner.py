import socket
import threading
import argparse
from queue import Queue

# Number of threads
MAX_THREADS = 100

# Create a queue to hold the ports to scan
port_queue = Queue()

# List to store open ports
open_ports = []

# Lock for thread-safe operations
print_lock = threading.Lock()

def scan_port(target_ip, port):
    """
    Attempts to connect to the target IP and port.
    If successful, appends the port to open_ports.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout for the connection attempt
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            with print_lock:
                print(f"[+] Port {port} is open")
            open_ports.append(port)
        sock.close()
    except Exception as e:
        with print_lock:
            print(f"[-] Error scanning port {port}: {e}")

def worker(target_ip):
    """
    Worker thread function that scans ports from the queue.
    """
    while True:
        port = port_queue.get()
        if port is None:
            break
        scan_port(target_ip, port)
        port_queue.task_done()

def main():
    parser = argparse.ArgumentParser(description="Simple Python Port Scanner")
    parser.add_argument("target", help="Target IP or hostname to scan")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    args = parser.parse_args()

    target = args.target
    start_port = args.start
    end_port = args.end

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[-] Could not resolve hostname: {target}")
        return

    print(f"[*] Starting scan on host: {target_ip}")
    print(f"[*] Scanning ports from {start_port} to {end_port}\n")

    # Start worker threads
    threads = []
    for _ in range(MAX_THREADS):
        t = threading.Thread(target=worker, args=(target_ip,))
        t.daemon = True
        t.start()
        threads.append(t)

    # Enqueue ports
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Wait until all ports are scanned
    port_queue.join()

    # Stop workers
    for _ in range(MAX_THREADS):
        port_queue.put(None)
    for t in threads:
        t.join()

    print("\nScan completed.")
    if open_ports:
        print(f"Open ports on {target_ip}:")
        for port in sorted(open_ports):
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            print(f"Port {port}: {service}")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
