from flask import Flask, render_template, request, jsonify
from chains.humanizer_chain import run_humanizer_pipeline

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/humanize", methods=["POST"])
def humanize():
    data = request.json
    return jsonify(run_humanizer_pipeline(
        data["text"], data["persona"]
    ))

app.run(debug=True)

