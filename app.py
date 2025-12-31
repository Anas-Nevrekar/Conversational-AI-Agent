from flask import Flask, request, jsonify
from intent_parser import extract_intent

app = Flask(__name__)

@app.route("/command", methods=["POST"])
def handle_command():
    data = request.get_json()

    if not data or "command" not in data:
        return jsonify({"error": "Command missing"}), 400

    user_command = data["command"]

    intent = extract_intent(user_command)

    return jsonify({
        "user_command": user_command,
        "intent_extracted": intent
    })

if __name__ == "__main__":
    app.run(debug=True)
