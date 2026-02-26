from flask import Flask, request, jsonify
from intent_parser import extract_intent

app=Flask(__name__)

@app.route("/command", methods=["POST"])
def handle_command():
    data = request.get_json()

    # Check command
    if not data or "command" not in data:
        return jsonify({"error": "Command missing"}), 400

    # Check agent
    if "agent" not in data:
        return jsonify({"error": "Agent must be specified"}), 400

    user_command = data["command"]
    agent = data["agent"]

    try:
        intent = extract_intent(user_command, agent)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "user_command": user_command,
        "agent_used": agent,
        "intent_extracted": intent
    })

print("Server is running...")
if __name__ == "__main__":
    app.run(debug=True)