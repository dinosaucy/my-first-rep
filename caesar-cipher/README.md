# Caesar Cipher Tool

A command-line implementation of the classic Caesar cipher, with encrypt, decrypt, brute-force, and basic frequency-analysis modes.

## What it does

- **Encrypt**: shifts each letter forward by N positions
- **Decrypt**: shifts each letter back by N positions
- **Brute force**: tries all 25 possible shifts and prints the results, so you can spot the readable one by eye
- **Guess**: attempts to automatically determine the shift using basic frequency analysis (assumes the most frequent letter in the ciphertext maps to 'e', the most common letter in English)

## Why I built it

The Caesar cipher is the simplest possible introduction to cryptography and cryptanalysis. Building the brute-force and frequency-analysis modes helped me understand *why* single-substitution ciphers are trivially breakable — there just aren't enough possible keys (only 25), and letter frequency in English is predictable enough to exploit.

## Usage

```bash
# Encrypt
python3 caesar_cipher.py encrypt "Attack at dawn" 3
# Output: Dwwdfn dw gdzq

# Decrypt (when you know the shift)
python3 caesar_cipher.py decrypt "Dwwdfn dw gdzq" 3
# Output: Attack at dawn

# Brute force (when you don't know the shift)
python3 caesar_cipher.py brute "Dwwdfn dw gdzq"
# Prints all 25 shifts - shift 3 will read "Attack at dawn"

# Guess the shift automatically
python3 caesar_cipher.py guess "Dwwdfn dw gdzq"
```

## Tech used

- Python 3
- `argparse` with subcommands for a clean CLI

## Limitations (and why that's worth knowing)

The frequency-analysis "guess" mode is naive and works best on longer text — on short phrases it often guesses wrong, because a handful of words isn't enough data for English letter-frequency averages to hold. This is actually a useful lesson: real cryptanalysis needs enough ciphertext to work with, which is one reason short messages are relatively safer even with weak encryption.

## Possible improvements

- Support the Vigenère cipher (multi-shift, harder to crack)
- Improve frequency analysis using chi-squared scoring across all 26 shifts instead of single-letter matching
- Add file input/output for larger texts
