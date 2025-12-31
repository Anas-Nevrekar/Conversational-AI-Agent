from flask import Flask, request, jsonify
from intent_parser import extract_intent
from device_controller import control_device

app = Flask(__name__)

@app.route("/")
def home():
    return "Conversational AI Agent is running"

@app.route("/command", methods=["POST"])
def handle_command():
    data = request.get_json()

    if not data or "command" not in data:
        return jsonify({"error": "Command missing"}), 400

    user_command = data["command"]

    intent = extract_intent(user_command)
    result = control_device(intent["device"], intent["action"])

    return jsonify({
        "command": user_command,
        "intent": intent,
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True)
