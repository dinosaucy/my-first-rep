#!/usr/bin/env python3
"""
Log File Analyzer
------------------
Parses web server access logs (Common Log Format) and flags
suspicious activity: repeated failed logins, high request rates
from a single IP, and known attack-pattern strings in requests.
"""

import re
import argparse
from collections import defaultdict, Counter

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d{3}) (?P<size>\S+)'
)

SUSPICIOUS_PATTERNS = [
    (re.compile(r"\.\./"), "Directory traversal attempt"),
    (re.compile(r"(?i)union\s+select"), "Possible SQL injection"),
    (re.compile(r"(?i)<script"), "Possible XSS attempt"),
    (re.compile(r"(?i)/etc/passwd"), "Attempt to access sensitive file"),
    (re.compile(r"(?i)wp-admin|phpmyadmin"), "Common admin-panel probing"),
]

FAILED_STATUS_CODES = {"401", "403"}
REQUEST_RATE_THRESHOLD = 50  # requests from a single IP to flag as high volume


def parse_log_line(line: str):
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    return match.groupdict()


def analyze_log(filepath: str):
    ip_request_counts = Counter()
    ip_failed_counts = defaultdict(int)
    suspicious_hits = []

    total_lines = 0
    parsed_lines = 0

    with open(filepath, "r") as f:
        for line in f:
            total_lines += 1
            entry = parse_log_line(line)
            if not entry:
                continue
            parsed_lines += 1

            ip = entry["ip"]
            path = entry["path"]
            status = entry["status"]

            ip_request_counts[ip] += 1

            if status in FAILED_STATUS_CODES:
                ip_failed_counts[ip] += 1

            for pattern, description in SUSPICIOUS_PATTERNS:
                if pattern.search(path):
                    suspicious_hits.append((ip, path, description))

    return {
        "total_lines": total_lines,
        "parsed_lines": parsed_lines,
        "ip_request_counts": ip_request_counts,
        "ip_failed_counts": ip_failed_counts,
        "suspicious_hits": suspicious_hits,
    }


def print_report(results: dict):
    print("\n--- Log Analysis Report ---")
    print(f"Total lines read: {results['total_lines']}")
    print(f"Successfully parsed: {results['parsed_lines']}")

    print("\nTop 5 requesting IPs:")
    for ip, count in results["ip_request_counts"].most_common(5):
        flag = " [HIGH VOLUME]" if count >= REQUEST_RATE_THRESHOLD else ""
        print(f"  {ip:<16} {count} requests{flag}")

    print("\nIPs with repeated failed/forbidden requests (401/403):")
    repeat_failures = {ip: c for ip, c in results["ip_failed_counts"].items() if c >= 3}
    if repeat_failures:
        for ip, count in sorted(repeat_failures.items(), key=lambda x: -x[1]):
            print(f"  {ip:<16} {count} failed attempts")
    else:
        print("  None found")

    print("\nSuspicious request patterns detected:")
    if results["suspicious_hits"]:
        for ip, path, description in results["suspicious_hits"][:20]:
            print(f"  [{description}] {ip} -> {path}")
        if len(results["suspicious_hits"]) > 20:
            print(f"  ...and {len(results['suspicious_hits']) - 20} more")
    else:
        print("  None found")

    print()


def main():
    parser = argparse.ArgumentParser(description="Analyze a web server access log for suspicious activity.")
    parser.add_argument("logfile", help="Path to the log file (Common Log Format)")
    args = parser.parse_args()

    results = analyze_log(args.logfile)
    print_report(results)


if __name__ == "__main__":
    main()
