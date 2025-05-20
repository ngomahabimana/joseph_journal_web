from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from datetime import datetime
import random
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

bible_verses = [
    "John 8:32 – Then you will know the truth, and the truth will set you free.",
    "Jeremiah 29:11 – 'For I know the plans I have for you,' declares the Lord...",
    "Psalm 23:1 – The Lord is my shepherd, I shall not want.",
]

devotionals = [
    "🕊️ Trust God’s plan even when the path isn’t clear.",
    "💡 Your identity is not in your past, but in Christ.",
    "🔥 Prayer is not a ritual. It's a weapon.",
]

journal_file = "journal.txt"

@app.route("/journal", methods=["GET", "POST"])
def journal():
    verse = random.choice(bible_verses)
    devotional = random.choice(devotionals)
    if request.method == "POST":
        entry = request.form.get("entry")
        if entry:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(journal_file, "a", encoding="utf-8") as file:
                file.write(f"[{timestamp}]
{entry}
---\n")
            flash("✅ Your entry has been saved.")
            return redirect(url_for("journal"))

    entries = []
    if os.path.exists(journal_file):
        with open(journal_file, "r", encoding="utf-8") as file:
            content = file.read().strip()
            entries = content.split("---\n") if content else []

    return render_template("journal.html", verse=verse, devotional=devotional, entries=entries)

@app.route("/")
def home():
    return redirect(url_for("journal"))

if __name__ == "__main__":
    from os import environ
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
