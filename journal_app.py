from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from flask import Flask, render_template, request, redirect, session, url_for, flash, send_file
from datetime import datetime
import os
import json
from devotions import DEVOTIONS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "your_secret_key"

stored_username = "admin"
stored_password_hash = "$2b$12$T9LABCAafaSc6FZMwmozLOpilTySRDjIefmgnBFQTcX7IsoPHZGaa"  # hashed "1234"

@app.route("/", methods=["GET"])
def home():
    lang = request.args.get("lang", "en")
    today = datetime.now().strftime("%Y-%m-%d")
    filename = "dynamic_devotions.json"
    devo = None
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        devo = data.get(today, {}).get(lang)
    return render_template("index.html", devo=devo, lang=lang)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        else:
            users = {}

        stored_hash = users.get(username)
        if stored_hash and bcrypt.check_password_hash(stored_hash, password):
            session["user"] = username
            return redirect(url_for("journal"))
        else:
            flash("❌ Invalid username or password.")
            return redirect(url_for("login"))

    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("❗ Username and password are required.")
            return redirect(url_for("register"))

        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        else:
            users = {}

        if username in users:
            flash("⚠️ Username already exists. Choose another.")
            return redirect(url_for("register"))

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        users[username] = password_hash

        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)

        flash("✅ Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/journal", methods=["GET"], endpoint="journal")
def journal():
    if "user" not in session:
        return redirect(url_for("login"))
    lang = request.args.get("lang", "en")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"journal_{date_str}_{lang}.txt"
    content = ""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    return render_template("journal.html", lang=lang, entry=content)

@app.route("/journal", methods=["POST"], endpoint="save_journal")
def save_journal():
    if "user" not in session:
        return redirect(url_for("login"))
    lang = request.form.get("lang", "en")
    entry = request.form.get("entry", "")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"journal_{date_str}_{lang}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(entry)
    flash("✅ Entry saved successfully.")
    return redirect(url_for("journal") + f"?lang={lang}")

@app.route("/entries")
def entries():
    if "user" not in session:
        return redirect(url_for("login"))

    lang = request.args.get("lang", "en")
    files = [f for f in os.listdir() if f.startswith("journal_") and f.endswith(f"_{lang}.txt")]
    files.sort(reverse=True)

    all_entries = {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            date = file.replace("journal_", "").replace(f"_{lang}.txt", "")
            content = f.read()
            all_entries[date] = content

    return render_template("entries.html", entries=all_entries, lang=lang)

@app.route("/clear", methods=["POST"])
def clear():
    if "user" not in session:
        return redirect(url_for("login"))
    lang = request.form.get("lang", "en")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"journal_{date_str}_{lang}.txt"
    if os.path.exists(filename):
        os.remove(filename)
        flash("🗑️ Today's journal entry has been cleared.")
    else:
        flash("⚠️ No entry found for today.")
    return redirect(url_for("journal") + f"?lang={lang}")

@app.route("/export_pdf")
def export_pdf():
    if "user" not in session:
        return redirect(url_for("login"))

    lang = request.args.get("lang", "en")
    files = [f for f in os.listdir() if f.startswith("journal_") and f.endswith(f"_{lang}.txt")]
    files.sort()

    pdf_path = "journal_export.pdf"
    c = canvas.Canvas(pdf_path, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            date = file.replace("journal_", "").replace(f"_{lang}.txt", "")
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, f"📅 {date}")
            y -= 20

            c.setFont("Helvetica", 12)
            for line in f.readlines():
                for segment in line.strip().split("\n"):
                    if y < 50:
                        c.showPage()
                        y = height - 50
                    c.drawString(50, y, segment)
                    y -= 15

            y -= 30  # Space between entries

    c.save()

    return send_file(pdf_path, as_attachment=True)

@app.route("/view_by_date")
def view_by_date():
    if "user" not in session:
        return redirect(url_for("login"))
    lang = request.args.get("lang", "en")
    date = request.args.get("date")
    filename = f"journal_{date}_{lang}.txt"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = "No entry found for this date."
    return f"<h2>Journal Entry for {date}</h2><pre>{content}</pre><p><a href='/journal?lang={lang}'>Back</a></p>"
@app.route("/devotional", methods=["GET", "POST"])
def devotional():
    if "user" not in session:
        return redirect(url_for("login"))

    lang = request.args.get("lang", "en")
    today = datetime.now().strftime("%Y-%m-%d")
    filename = "dynamic_devotions.json"
    messages_filename = f"devotional_messages_{today}.json"

    devo = None
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        devo = data.get(today, {}).get(lang)

    messages = []
    if os.path.exists(messages_filename):
        with open(messages_filename, "r", encoding="utf-8") as f:
            messages = json.load(f)

    if request.method == "POST":
        if "message" in request.form:
            name = request.form.get("name")
            message = request.form.get("message")
            entry = {
                "name": name,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            messages.append(entry)
            with open(messages_filename, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)

    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    return render_template("devotional.html", devo=devo, messages=messages, lang=lang, current_date=current_date)
    
@app.route("/edit_devotional", methods=["GET", "POST"])
def edit_devotional():
    if "user" not in session:
        return redirect(url_for("login"))

    lang = request.args.get("lang", "en")
    date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    filename = "dynamic_devotions.json"

    # Load existing devotional data
    devotional_data = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            devotional_data = json.load(f)

    current_devotional = devotional_data.get(date, {}).get(lang, {
        "verse": "",
        "text": "",
        "reflection": "",
        "prayer": ""
    })

    if request.method == "POST":
        verse = request.form.get("verse", "")
        text = request.form.get("text", "")
        reflection = request.form.get("reflection", "")
        prayer = request.form.get("prayer", "")

        if date not in devotional_data:
            devotional_data[date] = {}

        devotional_data[date][lang] = {
            "verse": verse,
            "text": text,
            "reflection": reflection,
            "prayer": prayer
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(devotional_data, f, ensure_ascii=False, indent=2)

        flash("✅ Devotional updated successfully!")
        return redirect(url_for("devotional", lang=lang))

    return render_template("edit_devotional.html", date=date, lang=lang, devo=current_devotional)

@app.route("/submit_devotional", methods=["POST"])
def submit_devotional():
    if "user" not in session:
        return redirect(url_for("login"))

    date = request.form["date"]
    lang = request.form["lang"]
    verse = request.form["verse"]
    text = request.form["text"]
    reflection = request.form["reflection"]
    prayer = request.form["prayer"]

    filename = "dynamic_devotions.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    data.setdefault(date, {})[lang] = {
        "verse": verse,
        "text": text,
        "reflection": reflection,
        "prayer": prayer
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return redirect(url_for("devotional", lang=lang))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session:
        return redirect(url_for("login"))
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "").lower()
        files = [f for f in os.listdir() if f.startswith("journal_") and f.endswith(".txt")]
        files.sort(reverse=True)
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                if query in content.lower():
                    date = file.replace("journal_", "").replace(".txt", "")
                    results.append(f"📅 {date}:\n{content.strip()}")
    return render_template("search.html", results=results, query=query)

@app.route("/message", methods=["GET", "POST"])
def message():
    if "user" not in session:
        return redirect(url_for("login"))
    success = False
    if request.method == "POST":
        msg = request.form.get("message")
        name = request.form.get("name")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("messages.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {name}: {msg}\n")
        success = True
    return render_template("message.html", success=success)

@app.route("/message_success")
def message_success():
    return "<h3>Your message has been sent successfully.</h3><p><a href='/message'>Send another</a></p>"

if __name__ == "__main__":
    from os import environ
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)), debug=True)
