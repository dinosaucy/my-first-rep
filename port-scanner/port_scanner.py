#!/usr/bin/env python3
"""
Simple TCP Port Scanner
------------------------
Educational tool to scan a host for open TCP ports.
Only use this against systems you own or have explicit permission to test.
"""

import socket
import sys
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt",
}


def scan_port(target: str, port: int, timeout: float = 1.0):
    """Attempt to connect to a single TCP port. Returns (port, is_open)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            return port, result == 0
    except socket.error:
        return port, False


def scan_range(target: str, start_port: int, end_port: int, max_threads: int = 100):
    """Scan a range of ports concurrently using a thread pool."""
    open_ports = []
    ports = range(start_port, end_port + 1)

    print(f"\nScanning {target} — ports {start_port}-{end_port}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, target, p): p for p in ports}
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                service = COMMON_PORTS.get(port, "Unknown")
                print(f"[OPEN] Port {port:<6} ({service})")
                open_ports.append(port)

    return sorted(open_ports)


def resolve_target(target: str) -> str:
    """Resolve a hostname to an IP address."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Error: could not resolve host '{target}'")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Simple multithreaded TCP port scanner (for authorized use only)."
    )
    parser.add_argument("target", help="Hostname or IP address to scan")
    parser.add_argument("-p", "--ports", default="1-1024",
                         help="Port range to scan, e.g. 1-1024 (default: 1-1024)")
    parser.add_argument("-t", "--threads", type=int, default=100,
                         help="Number of concurrent threads (default: 100)")
    args = parser.parse_args()

    start_port, end_port = map(int, args.ports.split("-"))
    ip = resolve_target(args.target)

    open_ports = scan_range(ip, start_port, end_port, args.threads)

    print(f"\nScan complete. {len(open_ports)} open port(s) found.")
    if open_ports:
        print("Open ports:", ", ".join(str(p) for p in open_ports))


if __name__ == "__main__":
    main()
