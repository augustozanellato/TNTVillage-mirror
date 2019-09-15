from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory
import search
app = Flask(__name__)

@app.route('/assets/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search")
def hello():
    query = request.args.get("query", default=None)
    if (query is not None):
        return render_template('search.html', results=search.search(query), searched=query)
    else:
        return "<h1>Bad Request</h1>", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081) 