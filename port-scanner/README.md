# TCP Port Scanner

A multithreaded TCP port scanner written in Python. Scans a target host for open ports and identifies common services.

## What it does

- Resolves a hostname to an IP address
- Scans a specified port range concurrently (using a thread pool)
- Flags open ports and matches them against a list of common services (SSH, HTTP, RDP, etc.)
- Reports scan duration and a summary of open ports

## Why I built it

Understanding how port scanning works under the hood — raw TCP connect scans — helped me understand what tools like Nmap are actually doing, and gave me hands-on practice with Python sockets, concurrency, and CLI tool design.

## Usage

```bash
python3 port_scanner.py <target> -p <start-end> -t <threads>
```

### Examples

```bash
# Scan the default range (1-1024) on localhost
python3 port_scanner.py 127.0.0.1

# Scan a custom range with more threads
python3 port_scanner.py scanme.nmap.org -p 1-500 -t 200
```

## Tech used

- Python 3
- `socket` (raw TCP connections)
- `concurrent.futures.ThreadPoolExecutor` (concurrency)
- `argparse` (CLI interface)

## ⚠️ Legal / ethical note

Only run this against hosts you own or have explicit written permission to test (e.g. [scanme.nmap.org](https://scanme.nmap.org), which is provided by the Nmap project specifically for testing). Scanning systems without authorization is illegal in most jurisdictions.

## Possible improvements

- Add UDP scanning
- Add banner grabbing for service version detection
- Export results to JSON/CSV
