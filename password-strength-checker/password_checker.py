#!/usr/bin/env python3
"""
Password Strength Checker
--------------------------
Evaluates password strength based on length, character variety,
common patterns, and presence in a small list of known weak passwords.
"""

import re
import argparse
import getpass

COMMON_WEAK_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345",
    "qwerty", "abc123", "password1", "111111", "iloveyou",
    "admin", "welcome", "monkey", "letmein", "dragon",
}


def check_length(password: str) -> tuple[int, str]:
    length = len(password)
    if length < 8:
        return 0, "Too short (minimum 8 characters recommended)"
    elif length < 12:
        return 1, "Acceptable length"
    else:
        return 2, "Strong length"


def check_variety(password: str) -> tuple[int, list[str]]:
    score = 0
    missing = []

    if re.search(r"[a-z]", password):
        score += 1
    else:
        missing.append("lowercase letter")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        missing.append("uppercase letter")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        missing.append("number")

    if re.search(r"[^a-zA-Z0-9]", password):
        score += 1
    else:
        missing.append("special character")

    return score, missing


def check_common_patterns(password: str) -> list[str]:
    issues = []
    lowered = password.lower()

    if lowered in COMMON_WEAK_PASSWORDS:
        issues.append("This is a widely known weak/breached password")

    if re.search(r"(.)\1{2,}", password):
        issues.append("Contains repeated characters (e.g. 'aaa')")

    if re.search(r"(0123|1234|2345|3456|4567|5678|6789|abcd|bcde|cdef)", lowered):
        issues.append("Contains a sequential pattern")

    return issues


def rate_password(password: str) -> dict:
    length_score, length_msg = check_length(password)
    variety_score, missing = check_variety(password)
    pattern_issues = check_common_patterns(password)

    total_score = length_score + variety_score
    penalty = len(pattern_issues)
    final_score = max(0, total_score - penalty)

    if final_score <= 2:
        rating = "Weak"
    elif final_score <= 4:
        rating = "Moderate"
    elif final_score <= 5:
        rating = "Strong"
    else:
        rating = "Very Strong"

    return {
        "rating": rating,
        "score": final_score,
        "max_score": 6,
        "length_feedback": length_msg,
        "missing_character_types": missing,
        "pattern_issues": pattern_issues,
    }


def print_report(password: str):
    result = rate_password(password)

    print("\n--- Password Strength Report ---")
    print(f"Rating: {result['rating']} ({result['score']}/{result['max_score']})")
    print(f"Length: {result['length_feedback']}")

    if result["missing_character_types"]:
        print("Missing character types:", ", ".join(result["missing_character_types"]))
    else:
        print("Character variety: good (has upper, lower, number, and symbol)")

    if result["pattern_issues"]:
        print("Issues found:")
        for issue in result["pattern_issues"]:
            print(f"  - {issue}")
    else:
        print("No common weak patterns detected")

    print()


def main():
    parser = argparse.ArgumentParser(description="Check password strength.")
    parser.add_argument("-p", "--password", help="Password to check (omit to be prompted securely)")
    args = parser.parse_args()

    password = args.password or getpass.getpass("Enter password to check: ")
    print_report(password)


if __name__ == "__main__":
    main()
