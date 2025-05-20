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
    "Romans 8:28 – All things work together for good for those who love God.",
    "Proverbs 3:5 – Trust in the Lord with all your heart and lean not on your own understanding.",
    "Matthew 11:28 – Come to me, all who are weary and burdened, and I will give you rest.",
    "Isaiah 41:10 – Do not fear, for I am with you; do not be dismayed, for I am your God."
]

devotionals = [
    "🕊️ Trust God’s plan even when the path isn’t clear.",
    "💡 Your identity is not in your past, but in Christ.",
    "🔥 Prayer is not a ritual. It's a weapon.",
    "🌱 Growth requires pruning. Let God cut what hinders you.",
    "🙌 Gratitude changes your attitude and attracts blessings.",
    "🛡️ You are not alone in battle. God is your defender.",
    "👑 Remember: You are chosen, not forsaken."
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
                file.write(f"[{timestamp}]\n{entry}\n---\n")
            flash("✅ Your entry has been saved.")
            return redirect(url_for("journal"))

    entries = []
    if os.path.exists(journal_file):
        with open(journal_file, "r", encoding="utf-8") as file:
            content = file.read().strip()
            entries = content.split("---\n") if content else []

    return render_template("journal.html", verse=verse, devotional=devotional, entries=entries)

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    results = []
    if os.path.exists(journal_file):
        with open(journal_file, "r", encoding="utf-8") as file:
            entries = file.read().split("---\n")
            results = [e for e in entries if query in e.lower()]

    return render_template("search.html", query=query, results=results)

@app.route("/clear", methods=["POST"])
def clear():
    if os.path.exists(journal_file):
        os.remove(journal_file)
        flash("🧹 Journal has been cleared.")
    return redirect(url_for("journal"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/devotional")
def devotional_page():
    verse = random.choice(bible_verses)
    devotional = random.choice(devotionals)
    return render_template("devotional.html", verse=verse, devotional=devotional)

@app.route("/export")
def export():
    pdf_path = "journal_export.pdf"
    try:
        from reportlab.pdfgen import canvas
        if os.path.exists(journal_file):
            with open(journal_file, "r", encoding="utf-8") as file:
                content = file.read().splitlines()
            c = canvas.Canvas(pdf_path)
            c.setFont("Helvetica", 12)
            y = 800
            for line in content:
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 800
                c.drawString(50, y, line)
                y -= 18
            c.save()
            return send_file(pdf_path, as_attachment=True)
        else:
            flash("⚠️ No journal entries found to export.")
            return redirect(url_for("journal"))
    except Exception:
        flash("❌ Failed to export journal. Please try again later.")
        return redirect(url_for("journal"))

@app.route("/")
def home():
    return redirect(url_for("journal"))

if __name__ == "__main__":
    from os import environ
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
