from flask import Flask, render_template, request
import os

app = Flask(__name__)

ENTRY_FILE = "journal_entries.txt"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/entries")
def entries():
    if os.path.exists(ENTRY_FILE):
        with open(ENTRY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip().split("---")
    else:
        content = []
    return render_template("entries.html", entries=content)

@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "").lower()
        if os.path.exists(ENTRY_FILE):
            with open(ENTRY_FILE, "r", encoding="utf-8") as f:
                entries = f.read().strip().split("---")
                results = [entry for entry in entries if query in entry.lower()]
    return render_template("search.html", results=results, query=query)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
