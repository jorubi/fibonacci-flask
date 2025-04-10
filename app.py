from flask import Flask, render_template, request, g
import time
import functools

app = Flask(__name__, template_folder="templates")


# Memoized recursive Fibonacci function
@functools.lru_cache(maxsize=None)
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


@app.before_request
def start_timer():
    g.start_time = time.time()


@app.route("/", methods=["GET", "POST"])
def fibonacciSequence():
    if request.method == "POST":
        try:
            term = int(request.form["term"])
            if term <= 0:
                raise ValueError("Please enter a positive integer.")

            sequence = [fibonacci(i) for i in range(term)]
            elapsed_time = round(time.time() - g.start_time, 6)

            return render_template(
                "fibonacci.html",
                term=term,
                sequence=sequence,
                elapsed_time=elapsed_time,
            )

        except ValueError as e:
            return render_template("fibonacci.html", error=str(e))

    return render_template("fibonacci.html")


if __name__ == "__main__":
    app.run(debug=True)
