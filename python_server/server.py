from flask import Flask
app = Flask("notify")

@app.route("/notify")
def notify():
    return "hello"

