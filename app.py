from flask import Flask, render_template, request
from password_checker import evaluate_password, load_leaked_passwords, hash_password, \
    check_length, check_uppercase, check_lowercase, check_digits, check_special, calculate_entropy

app = Flask(__name__)
leaked_hashes = load_leaked_passwords("leaked_passwords.txt")


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        password = request.form.get("password", "")
        result = build_result(password)
    return render_template("index.html", result=result)


def build_result(password: str) -> dict:
    if hash_password(password) in leaked_hashes:
        return {
            "strength": "COMPROMISED",
            "score": 0,
            "entropy": 0,
            "feedback": ["This password has appeared in a leaked dataset. Do not use it."],
            "compromised": True,
        }

    score = 0
    feedback = []

    if check_length(password):
        score += 1
    else:
        feedback.append("Use at least 12 characters.")

    if check_uppercase(password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if check_lowercase(password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if check_digits(password):
        score += 1
    else:
        feedback.append("Include numbers.")

    if check_special(password):
        score += 1
    else:
        feedback.append("Include special characters.")

    strength_map = {0: "Weak", 1: "Weak", 2: "Weak", 3: "Moderate", 4: "Strong", 5: "Very Strong"}

    return {
        "strength": strength_map[score],
        "score": score,
        "entropy": round(calculate_entropy(password), 2),
        "feedback": feedback,
        "compromised": False,
    }


if __name__ == "__main__":
    app.run(debug=True)
