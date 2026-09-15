"""
Password Generator Logic Module - OASIS INFOBYTE Task 3: Random Password Generator (Advanced)
Implements cryptographically secure password generation using Python's `secrets` module (CSPRNG).
DO NOT use the standard `random` module for security-sensitive operations.
"""

import secrets
import string
import math
from typing import Tuple, Dict, Any, List

# Character sets
CHAR_SETS = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "digits": string.digits,
    "symbols": "!@#$%^&*()-_=+[]{}|;:,.<>?"
}

# Ambiguous characters often misread or confused in different typefaces
AMBIGUOUS_CHARACTERS = set("0O1Il|`~;:.,'")


def generate_secure_password(
    length: int,
    use_upper: bool,
    use_lower: bool,
    use_digits: bool,
    use_symbols: bool,
    exclude_ambiguous: bool = False
) -> str:
    """
    Generate a cryptographically secure random password using secrets module (CSPRNG).

    Requirements:
        - Minimum length: 8 characters.
        - At least TWO character types must be selected.
        - Guaranteed character inclusion: Every selected character type is guaranteed
          to be represented by at least one character in the generated password.
        - Cryptographic shuffle using secrets.SystemRandom().shuffle() to prevent
          predictable character ordering.
        - Ambiguous characters excluded if requested.

    Returns:
        Generated password string.

    Raises:
        ValueError: If validation conditions are not met.
    """
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")
    if length > 128:
        raise ValueError("Password length cannot exceed 128 characters.")

    # Determine enabled character pools
    selected_pools: Dict[str, str] = {}
    if use_upper:
        selected_pools["uppercase"] = CHAR_SETS["uppercase"]
    if use_lower:
        selected_pools["lowercase"] = CHAR_SETS["lowercase"]
    if use_digits:
        selected_pools["digits"] = CHAR_SETS["digits"]
    if use_symbols:
        selected_pools["symbols"] = CHAR_SETS["symbols"]

    # Strict requirement: At least TWO character types must be selected
    if len(selected_pools) < 2:
        raise ValueError(
            "At least TWO character types must be selected (e.g., Uppercase + Numbers, or Lowercase + Symbols)."
        )

    # Filter out ambiguous characters if requested
    filtered_pools: Dict[str, str] = {}
    for pool_name, pool_chars in selected_pools.items():
        if exclude_ambiguous:
            cleaned = "".join(c for c in pool_chars if c not in AMBIGUOUS_CHARACTERS)
            if not cleaned:
                raise ValueError(f"Excluding ambiguous characters left the '{pool_name}' pool empty.")
            filtered_pools[pool_name] = cleaned
        else:
            filtered_pools[pool_name] = pool_chars

    # 1. Guaranteed Inclusion: Guarantee at least 1 character from each selected pool
    password_chars: List[str] = []
    for pool_chars in filtered_pools.values():
        password_chars.append(secrets.choice(pool_chars))

    # 2. Fill the remaining length from the combined pool of all selected types
    combined_pool = "".join(filtered_pools.values())
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(combined_pool))

    # 3. Cryptographically secure Fisher-Yates shuffle
    # Using secrets.SystemRandom() so character positions are unpredictable
    secure_rng = secrets.SystemRandom()
    secure_rng.shuffle(password_chars)

    return "".join(password_chars)


def calculate_entropy(password: str, pool_size: int) -> float:
    """
    Calculate Shannon information entropy (in bits) for the password:
        Entropy = Length * log2(Pool Size)
    """
    if pool_size <= 1 or not password:
        return 0.0
    return round(len(password) * math.log2(pool_size), 1)


def evaluate_password_strength(password: str, pool_size: int = 70) -> Tuple[str, int, str, str, float]:
    """
    Evaluate password strength based on length, entropy, and character diversity.

    Returns:
        (strength_level, score_percentage, hex_color, feedback_message, entropy_bits)
    """
    if not password:
        return ("Empty", 0, "#94a3b8", "No password generated yet.", 0.0)

    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in CHAR_SETS["symbols"] for c in password)

    types_count = sum([has_upper, has_lower, has_digit, has_symbol])
    entropy = calculate_entropy(password, pool_size)

    # Scoring metric (0 - 100)
    score = 0

    # Length factor (up to 55 points)
    if length < 8:
        score += 5
    elif 8 <= length <= 9:
        score += 15
    elif 10 <= length <= 12:
        score += 25
    elif 13 <= length <= 15:
        score += 40
    elif 16 <= length <= 20:
        score += 50
    else:
        score += 55

    # Diversity factor (up to 40 points: 10 per type)
    score += (types_count * 10)

    # High security bonus (+5 for length >= 16 and all 4 types)
    if types_count >= 4 and length >= 16:
        score += 5

    score = min(score, 100)

    # Classify strength
    if score < 40:
        return (
            "Weak",
            score,
            "#ef4444",  # Red
            "Weak: Vulnerable to brute-force attacks. Recommend 16+ characters with mixed types.",
            entropy
        )
    elif 40 <= score < 70:
        return (
            "Medium",
            score,
            "#f59e0b",  # Amber
            "Medium: Acceptable for standard accounts. Recommend adding symbols or more length.",
            entropy
        )
    elif 70 <= score < 88:
        return (
            "Strong",
            score,
            "#0284c7",  # Blue
            "Strong: High resistance to dictionary and automated cracking attacks.",
            entropy
        )
    else:
        return (
            "Very Strong",
            score,
            "#16a34a",  # Green
            "Very Strong: Outstanding cryptographic entropy! Excellent for high-security accounts.",
            entropy
        )
