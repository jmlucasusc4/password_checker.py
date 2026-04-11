import hashlib
import re
import math


# ===============================
# Utility Functions
# ===============================

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def load_leaked_passwords(file_path: str) -> set:
    """
    Load leaked passwords and return a set of hashed passwords.
    """
    leaked_hashes = set()

    try:
        with open(file_path, "r") as file:
            for line in file:
                pwd = line.strip()
                if pwd:
                    leaked_hashes.add(hash_password(pwd))
    except FileNotFoundError:
        print("⚠️ Leaked password file not found.")
    
    return leaked_hashes


# ===============================
# Strength Checks
# ===============================

def check_length(password: str) -> bool:
    return len(password) >= 12


def check_uppercase(password: str) -> bool:
    return any(char.isupper() for char in password)


def check_lowercase(password: str) -> bool:
    return any(char.islower() for char in password)


def check_digits(password: str) -> bool:
    return any(char.isdigit() for char in password)


def check_special(password: str) -> bool:
    return bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))


def calculate_entropy(password: str) -> float:
    """
    Estimate password entropy.
    """
    pool = 0

    if check_lowercase(password):
        pool += 26
    if check_uppercase(password):
        pool += 26
    if check_digits(password):
        pool += 10
    if check_special(password):
        pool += 32  # approximate symbol set size

    if pool == 0:
        return 0

    return len(password) * math.log2(pool)


# ===============================
# Main Strength Evaluation
# ===============================

def evaluate_password(password: str, leaked_hashes: set) -> None:
    score = 0
    feedback = []

    if check_length(password):
        score += 1
    else:
        feedback.append("❌ Use at least 12 characters.")

    if check_uppercase(password):
        score += 1
    else:
        feedback.append("❌ Add uppercase letters.")

    if check_lowercase(password):
        score += 1
    else:
        feedback.append("❌ Add lowercase letters.")

    if check_digits(password):
        score += 1
    else:
        feedback.append("❌ Include numbers.")

    if check_special(password):
        score += 1
    else:
        feedback.append("❌ Include special characters.")

    entropy = calculate_entropy(password)

    if hash_password(password) in leaked_hashes:
        print("\n🚨 WARNING: This password has appeared in a leaked dataset!")
        print("🔴 Strength: COMPROMISED")
        return

    # Strength rating
    if score <= 2:
        strength = "Weak"
    elif score == 3:
        strength = "Moderate"
    elif score == 4:
        strength = "Strong"
    else:
        strength = "Very Strong"

    print("\n========== PASSWORD REPORT ==========")
    print(f"Score: {score}/5")
    print(f"Entropy Estimate: {entropy:.2f} bits")
    print(f"Strength Rating: {strength}")

    if feedback:
        print("\nImprovement Suggestions:")
        for item in feedback:
            print(item)
    else:
        print("\n✅ Excellent password composition!")


# ===============================
# CLI Entry
# ===============================

def main():
    leaked_hashes = load_leaked_passwords("leaked_passwords.txt")
    
    password = input("Enter password to evaluate: ")
    evaluate_password(password, leaked_hashes)


if __name__ == "__main__":
    main()
