#!/usr/bin/env python3
"""
Hash Cracker (Dictionary Attack Demo)
---------------------------------------
Educational tool that demonstrates how dictionary attacks work against
unsalted password hashes. Given a hash and a wordlist, it hashes each
candidate word and checks for a match.

This is for learning purposes only - to understand why unsalted hashes
and weak/common passwords are dangerous. Only use against hashes you
created yourself for testing, never against real credentials without
authorization.
"""

import hashlib
import argparse
import time

SUPPORTED_ALGORITHMS = ["md5", "sha1", "sha256", "sha512"]


def hash_word(word: str, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    h.update(word.encode("utf-8"))
    return h.hexdigest()


def crack_hash(target_hash: str, wordlist_path: str, algorithm: str):
    target_hash = target_hash.strip().lower()
    attempts = 0
    start = time.time()

    with open(wordlist_path, "r", errors="ignore") as f:
        for line in f:
            word = line.strip()
            if not word:
                continue
            attempts += 1
            candidate_hash = hash_word(word, algorithm)

            if candidate_hash == target_hash:
                elapsed = time.time() - start
                return word, attempts, elapsed

    elapsed = time.time() - start
    return None, attempts, elapsed


def main():
    parser = argparse.ArgumentParser(
        description="Dictionary attack demo against a password hash (educational use only)."
    )
    parser.add_argument("hash", help="The target hash to crack")
    parser.add_argument("wordlist", help="Path to a wordlist file (one word per line)")
    parser.add_argument(
        "-a", "--algorithm", choices=SUPPORTED_ALGORITHMS, default="md5",
        help="Hash algorithm to use (default: md5)"
    )
    args = parser.parse_args()

    print(f"Attempting to crack {args.algorithm.upper()} hash using '{args.wordlist}'...")
    result, attempts, elapsed = crack_hash(args.hash, args.wordlist, args.algorithm)

    print(f"\nAttempts made: {attempts}")
    print(f"Time elapsed: {elapsed:.4f} seconds")

    if result:
        print(f"\n[MATCH FOUND] Password: '{result}'")
    else:
        print("\nNo match found in wordlist.")


if __name__ == "__main__":
    main()
