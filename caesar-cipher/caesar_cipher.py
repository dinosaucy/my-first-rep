#!/usr/bin/env python3
"""
Caesar Cipher Tool
-------------------
Classic substitution cipher: encrypts/decrypts text by shifting each
letter by a fixed number of positions in the alphabet. Also includes
a brute-force mode that tries all 25 possible shifts, and a basic
frequency-analysis mode to guess the shift on unknown ciphertext.
"""

import argparse
import string

ALPHABET_SIZE = 26

# Approximate relative frequency of letters in English text (%),
# used for frequency analysis to guess an unknown shift.
ENGLISH_FREQ_ORDER = "etaoinshrdlcumwfgypbvkjxqz"


def shift_char(char: str, shift: int) -> str:
    if char.isupper():
        base = ord('A')
    elif char.islower():
        base = ord('a')
    else:
        return char  # leave punctuation/spaces/numbers untouched

    shifted = (ord(char) - base + shift) % ALPHABET_SIZE
    return chr(shifted + base)


def caesar(text: str, shift: int) -> str:
    return "".join(shift_char(c, shift) for c in text)


def encrypt(text: str, shift: int) -> str:
    return caesar(text, shift)


def decrypt(text: str, shift: int) -> str:
    return caesar(text, -shift)


def brute_force(ciphertext: str):
    """Print all 25 possible shifts so a human can spot the readable one."""
    print("\n--- Brute Force: all possible shifts ---")
    for shift in range(1, ALPHABET_SIZE):
        print(f"Shift {shift:2}: {caesar(ciphertext, -shift)}")


def guess_shift_by_frequency(ciphertext: str) -> int:
    """
    Naive frequency analysis: find the most common letter in the
    ciphertext, assume it maps to 'e' (the most common English letter),
    and derive the shift from that.
    """
    letter_counts = {}
    for c in ciphertext.lower():
        if c in string.ascii_lowercase:
            letter_counts[c] = letter_counts.get(c, 0) + 1

    if not letter_counts:
        return 0

    most_common_letter = max(letter_counts, key=letter_counts.get)
    likely_shift = (ord(most_common_letter) - ord('e')) % ALPHABET_SIZE
    return likely_shift


def main():
    parser = argparse.ArgumentParser(description="Caesar cipher encrypt/decrypt/crack tool.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    enc = subparsers.add_parser("encrypt", help="Encrypt text with a given shift")
    enc.add_argument("text")
    enc.add_argument("shift", type=int)

    dec = subparsers.add_parser("decrypt", help="Decrypt text with a given shift")
    dec.add_argument("text")
    dec.add_argument("shift", type=int)

    brute = subparsers.add_parser("brute", help="Try all 25 shifts on ciphertext")
    brute.add_argument("text")

    guess = subparsers.add_parser("guess", help="Guess the shift using frequency analysis")
    guess.add_argument("text")

    args = parser.parse_args()

    if args.mode == "encrypt":
        print(encrypt(args.text, args.shift))
    elif args.mode == "decrypt":
        print(decrypt(args.text, args.shift))
    elif args.mode == "brute":
        brute_force(args.text)
    elif args.mode == "guess":
        shift = guess_shift_by_frequency(args.text)
        print(f"Likely shift: {shift}")
        print(f"Decrypted guess: {decrypt(args.text, shift)}")


if __name__ == "__main__":
    main()
