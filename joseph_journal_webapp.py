import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

bible_verses = [
    "John 8:32 – Then you will know the truth, and the truth will set you free.",
    "Psalm 23:1 – The Lord is my shepherd, I shall not want.",
    "Romans 8:28 – All things work together for good for those who love God.",
    "Matthew 11:28 – Come to me, all who are weary and burdened, and I will give you rest."
]

devotionals = [
    "🕊️ Trust God’s plan even when the path isn’t clear.",
    "💡 Your identity is not in your past, but in Christ.",
    "🔥 Prayer is not a ritual. It's a weapon.",
    "🌱 Growth requires pruning. Let God cut what hinders you."
]

ENTRY_FILE = "journal_entries.txt"

@app.route("/")
def index():
    verse = random.choice(bible_verses)
    devotional = random.choice(devotionals)
    return render_template("index.html", verse=verse, devotional=devotional)

@app.route("/submit", methods=["POST"])
def submit():
    entry = request.form.get("entry")
    if entry:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ENTRY_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n{entry}\n---\n")
    return redirect(url_for("index"))

@app.route("/entries")
def entries():
    if os.path.exists(ENTRY_FILE):
        with open(ENTRY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip().split("---\n")
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
                entries = f.read().strip().split("---\n")
                results = [entry for entry in entries if query in entry.lower()]
    return render_template("search.html", results=results, query=query)

@app.route("/clear", methods=["POST"])
def clear_entries():
    if os.path.exists(ENTRY_FILE):
        os.remove(ENTRY_FILE)
    return redirect(url_for("entries"))

if __name__ == "__main__":
    app.run(debug=True)