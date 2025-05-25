@app.route("/message", methods=["GET", "POST"])
def message():
    success = False
    if request.method == "POST":
        content = request.form.get("message")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("messages.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n{content}\n\n")
        success = True
    return render_template("message.html", success=success)