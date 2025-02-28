import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# LanguageTool API endpoint
LANGUAGETOOL_URL = "https://api.languagetool.org/v2/check"

@app.route("/check_grammar", methods=["POST"])
def check_grammar():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    params = {
        "text": text,
        "language": "en-US"
    }

    response = requests.post(LANGUAGETOOL_URL, data=params)
    return response.json()

if __name__ == "__main__":
    app.run(debug=True)
