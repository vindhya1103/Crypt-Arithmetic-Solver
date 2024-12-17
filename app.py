from flask import Flask, request, render_template
from itertools import permutations

app = Flask(__name__)


def solve_cryptarithmetic(puzzle):
    # Extract unique letters and words
    words = puzzle.replace("==", "=").split("=")
    letters = sorted(set(filter(str.isalpha, "".join(words))))

    # Validate input to prevent large inputs
    if len(letters) > 10:
        return {"error": "Too many unique letters. Maximum is 10."}

    first_letters = {word.strip()[0] for word in words if word.strip()}

    # Generate valid permutations
    for perm in permutations(range(10), len(letters)):
        mapping = dict(zip(letters, perm))

        # Skip invalid mappings with leading zeros
        if any(mapping[letter] == 0 for letter in first_letters):
            continue

        # Replace letters with digits
        translated = "".join(str(mapping.get(char, char)) for char in puzzle)
        try:
            # Evaluate the equation
            if eval(translated):
                return mapping
        except (ZeroDivisionError, SyntaxError):
            continue

    return {"error": "No solution found."}


@app.route("/", methods=["GET", "POST"])
def index():
    solution = None
    if request.method == "POST":
        puzzle = request.form["puzzle"]
        solution = solve_cryptarithmetic(puzzle)
    return render_template("index.html", solution=solution)


if __name__ == "__main__":
    app.run(debug=True)
