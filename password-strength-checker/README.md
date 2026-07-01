# Password Strength Checker

A command-line tool that evaluates password strength based on length, character variety, and known weak patterns.

## What it does

- Scores a password out of 6 based on length and character variety (lowercase, uppercase, numbers, symbols)
- Flags passwords found in a small list of commonly breached/weak passwords
- Detects repeated characters (`aaa`) and sequential patterns (`1234`, `abcd`)
- Prompts securely (input hidden) if no password is passed via CLI

## Why I built it

Weak passwords are still one of the top causes of account compromise. Building this helped me understand what actually makes a password crackable (predictability, low entropy, reused patterns) rather than just "add a special character."

## Usage

```bash
# Prompt securely (recommended - doesn't show password or store it in shell history)
python3 password_checker.py

# Or pass directly (not recommended for real passwords - visible in shell history)
python3 password_checker.py -p "MyTestPassword123!"
```

### Example output

```
--- Password Strength Report ---
Rating: Strong (5/6)
Length: Strong length
Character variety: good (has upper, lower, number, and symbol)
No common weak patterns detected
```

## Tech used

- Python 3
- `re` (regex pattern matching)
- `getpass` (secure, hidden password input)

## Possible improvements

- Check against a larger breached-password dataset (e.g. Have I Been Pwned API, using k-anonymity)
- Estimate crack time based on entropy
- Add a GUI or web front-end
