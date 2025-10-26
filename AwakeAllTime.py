from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello!</h1>"

def keep_alive():
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
