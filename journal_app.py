from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
import os
from devotions import DEVOTIONS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "your_secret_key"

# ✅ Only declare once — here
stored_username = "admin"
stored_password_hash = "$2b$12$T9LABCAafaSc6FZMwmozLOpilTySRDjIefmgnBFQTcX7IsoPHZGaa" # hashed "1234"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == stored_username and bcrypt.check_password_hash(stored_password_hash, password):
            session["user"] = username
            return redirect(url_for("journal"))
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/journal", methods=["GET"])
def journal():
    if "user" not in session:
        return redirect(url_for("login"))
    lang = request.args.get("lang", "en")
    return render_template("journal.html", lang=lang)

@app.route("/submit", methods=["POST"])
def submit():
    if "user" not in session:
        return redirect(url_for("login"))
    entry = request.form.get("entry")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"journal_{date_str}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(entry + "\n\n")
    return "Your entry has been saved! <a href='/journal'>Back to journal</a>"

# ✅ Place this directly below the submit route
@app.route("/clear", methods=["POST"])
def clear():
    if "user" not in session:
        return redirect(url_for("login"))

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"journal_{date_str}.txt"

    if os.path.exists(filename):
        os.remove(filename)
        message = "Today's journal entry has been cleared."
    else:
        message = "No entry found for today."

    return f"<h3>{message}</h3><p><a href='/journal'>Back to Journal</a></p>"
@app.route("/entries")
def entries():
    if "user" not in session:
        return redirect(url_for("login"))
    files = [f for f in os.listdir() if f.startswith("journal_") and f.endswith(".txt")]
    files.sort(reverse=True)
    all_entries = {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            all_entries[file.replace("journal_", "").replace(".txt", "")] = f.read()
    return render_template("entries.html", entries=all_entries)

@app.route("/export")
def export():
    if "user" not in session:
        return redirect(url_for("login"))
    files = [f for f in os.listdir() if f.startswith("journal_") and f.endswith(".txt")]
    files.sort()
    content = ""
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            content += f"--- {file} ---\n"
            content += f.read() + "\n\n"
    response = app.response_class(response=content, status=200, mimetype='text/plain')
    response.headers["Content-Disposition"] = "attachment; filename=journal_export.txt"
    return response

@app.route("/view_by_date")
def view_by_date():
    if "user" not in session:
        return redirect(url_for("login"))
    date = request.args.get("date")
    filename = f"journal_{date}.txt"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = "No entry found for this date."
    return f"<h2>Journal Entry for {date}</h2><pre>{content}</pre><p><a href='/journal'>Back</a></p>"

@app.route("/devotional")
def devotional():
    lang = request.args.get("lang", "en")
    today = datetime.now().strftime("%Y-%m-%d")
    devo = DEVOTIONS.get(today, {}).get(lang)

    if not devo:
        return f"<h2>No devotional found for today in {lang.upper()}</h2>"

    return render_template("devotional.html", devo=devo, lang=lang)

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
@app.route("/devotional")
def devotional():
    lang = request.args.get("lang", "en")
    today = datetime.now().strftime("%Y-%m-%d")
    devo = DEVOTIONS.get(today, {}).get(lang)

    if not devo:
        return f"<h2>No devotional found for today in {lang.upper()}</h2>"

    return render_template("devotional.html", devo=devo, lang=lang)
if __name__ == "__main__":
    from os import environ
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)), debug=True)
