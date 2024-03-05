# app.py
from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index_multiple.html")
@app.route("/results", methods=["POST"])
def results():
    test_strings = request.form.get("test_strings")
    regex_pattern = request.form.get("regex_pattern")

    # Split test strings by newline characters
    test_strings_list = [line.strip() for line in test_strings.split('\n') if line.strip()]

    matches_per_string = []

    for test_string in test_strings_list:
        matches = re.findall(regex_pattern, test_string)
        matches_per_string.append((test_string, matches))

    return render_template("results_multiple.html", test_strings_list=test_strings_list,
                            regex_pattern=regex_pattern, matches_per_string=matches_per_string)
@app.route("/validate_email", methods=["GET", "POST"])
def validate_email():
    if request.method == "POST":
        email = request.form.get("email")

        # Use a more comprehensive regex pattern for email validation
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(email_pattern, email)

        if match:
            username, domain = email.split('@')
            password_strength = check_password_strength(request.form.get("password"))
            return render_template("email_validation_complex.html", email=email, is_valid=True,
                                   username=username, domain=domain, password_strength=password_strength)

        return render_template("email_validation_complex.html", email=email, is_valid=False)

    return render_template("email_validation_complex.html", email="", is_valid=None)

def check_password_strength(password):
    # Check password strength (simple example)
    if len(password) >= 8:
        return "Strong"
    elif len(password) >= 6:
        return "Medium"
    else:
        return "Weak"

if __name__ == "__main__":
    app.run(debug=True)
