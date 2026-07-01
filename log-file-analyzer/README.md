# Log File Analyzer

A Python tool that parses web server access logs (Common Log Format) and flags suspicious activity — the kind of first-pass triage a blue team analyst does before digging deeper.

## What it does

- Parses standard access log lines (IP, timestamp, method, path, status code, size)
- Identifies the top requesting IPs and flags high-volume sources
- Flags IPs with repeated 401/403 (failed/forbidden) responses — a sign of brute-forcing or scanning
- Detects known attack patterns in request paths:
  - Directory traversal (`../`)
  - SQL injection attempts (`UNION SELECT`)
  - XSS attempts (`<script>`)
  - Sensitive file access attempts (`/etc/passwd`)
  - Common admin-panel probing (`/wp-admin`, `/phpmyadmin`)

## Why I built it

Log analysis is one of the most practical blue-team skills — most real attacks leave traces in access logs before anyone notices anything is wrong. Building this from scratch (rather than just running a SIEM) helped me understand what patterns actually indicate malicious intent versus normal traffic.

## Usage

```bash
python3 log_analyzer.py sample_access.log
```

A sample log (`sample_access.log`) is included with a mix of normal traffic and simulated attack patterns, so you can run it immediately without needing a real server.

### Example output

```
--- Log Analysis Report ---
Total lines read: 11
Successfully parsed: 10

Top 5 requesting IPs:
  203.0.113.55     6 requests
  192.168.1.10     3 requests
  198.51.100.23    1 requests

IPs with repeated failed/forbidden requests (401/403):
  203.0.113.55     4 failed attempts

Suspicious request patterns detected:
  [Directory traversal attempt] 203.0.113.55 -> /../../etc/passwd
  [Possible XSS attempt] 198.51.100.23 -> /search?q=<script>alert(1)</script>
  [Common admin-panel probing] 203.0.113.55 -> /wp-admin/
```

## Tech used

- Python 3
- `re` (regex log parsing and pattern matching)
- `collections.Counter` / `defaultdict` (traffic aggregation)

## Possible improvements

- Support additional log formats (JSON logs, syslog, nginx combined format)
- Add a time-window analysis (e.g. requests per minute) for better brute-force detection
- Export findings to CSV/JSON for use in other tools
- Add GeoIP lookups for suspicious IPs
