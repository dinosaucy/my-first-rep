# Hash Cracker (Dictionary Attack Demo)

An educational dictionary-attack tool that demonstrates why unsalted password hashes and weak/common passwords are dangerous.

## What it does

- Takes a target hash and a wordlist file
- Hashes each word in the wordlist using the same algorithm and compares it to the target
- Reports the matching password (if found), number of attempts, and time taken
- Supports MD5, SHA-1, SHA-256, and SHA-512

## Why I built it

This demonstrates the core weakness that makes password breaches so damaging: if a password is common enough to be in a wordlist, and the hash isn't salted, cracking it is just a matter of hashing every candidate and comparing — no "hacking" required, just brute computation. It's the same principle tools like Hashcat and John the Ripper use at massive scale.

## Usage

```bash
python3 hash_cracker.py <hash> <wordlist> -a <algorithm>
```

### Example (included wordlist and demo hash)

```bash
# This MD5 hash corresponds to a word in sample_wordlist.txt
python3 hash_cracker.py 7fc8baba8e7696d6c3b286f738245592 sample_wordlist.txt -a md5
```

Output:
```
Attempting to crack MD5 hash using 'sample_wordlist.txt'...

Attempts made: 20
Time elapsed: 0.0001 seconds

[MATCH FOUND] Password: 'dragonfly'
```

You can generate your own test hash to try against the wordlist:

```bash
python3 -c "import hashlib; print(hashlib.md5('yourword'.encode()).hexdigest())"
```

## Tech used

- Python 3
- `hashlib` (MD5/SHA family hashing)

## ⚠️ Legal / ethical note

Only use this against hashes you generate yourself for learning purposes. Attempting to crack credentials you don't own or don't have explicit permission to test is illegal. This tool is intentionally simple and slow (no GPU acceleration, no rainbow tables) — real attackers use far more sophisticated tooling, which is exactly why weak/reused passwords and unsalted hashing are considered serious security failures.

## Possible improvements

- Add salted-hash support (demonstrate why salting defeats simple dictionary attacks)
- Add multiprocessing for faster cracking on large wordlists
- Add a bcrypt/argon2 comparison mode to show why modern hashing is intentionally slow
