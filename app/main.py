from flask import Flask, request, redirect, render_template_string
import sqlite3
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Customer Portal</h1>
    <a href="/login?username=admin&password=admin">Login</a><br>
    <a href="/redirect?url=https://example.com">Redirect</a><br>
    <a href="/search?q=customer">Search</a><br>
    <a href="/network?host=127.0.0.1">Network Check</a>
    """

@app.route("/login")
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'admin')")

    query = "SELECT * FROM users WHERE username='%s' AND password='%s'" % (username, password)
    cursor.execute(query)

    return "Login processed"

@app.route("/search")
def search():
    q = request.args.get("q", "")
    return render_template_string("<h2>Search result for: " + q + "</h2>")

@app.route("/redirect")
def open_redirect():
    url = request.args.get("url", "")
    return redirect(url)

@app.route("/network")
def network():
    host = request.args.get("host", "127.0.0.1")
    result = subprocess.check_output("ping -c 1 " + host, shell=True)
    return result

@app.route("/debug")
def debug():
    return {
        "debug": True,
        "environment": "customer-validation",
        "security_headers": "not-configured"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
