# 🔐 Password Strength Checker (Python / Flask)

A web app that evaluates password strength in real time — checking entropy, composition rules, and a leaked password database.

## Features

- Scores passwords 1–5 based on length, uppercase, lowercase, digits, and special characters
- Calculates entropy in bits
- Checks against a local leaked password list (SHA-256 hashed)
- Dark glassmorphism UI with color-coded strength indicator and score bar
- Improvement suggestions for weak passwords

## Tech Stack

- **Python 3** — core logic
- **Flask** — web framework
- **Jinja2** — templating

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Project Structure

```
password-checker-app/
├── app.py                  # Flask routes
├── password_checker.py     # Strength evaluation logic
├── leaked_passwords.txt    # Leaked password list
├── requirements.txt
└── templates/
    └── index.html          # UI template
```

## Strength Ratings

| Score | Rating |
|-------|--------|
| 0–2 | Weak |
| 3 | Moderate |
| 4 | Strong |
| 5 | Very Strong |
| — | Compromised (found in leaked list) |

## Related

- [Java/Spring Boot version](https://github.com/jmlucasusc4/password_checker.java)
- [Swift/SwiftUI version](https://github.com/jmlucasusc4/password_checker.swift)
