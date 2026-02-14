from flask import Flask, render_template, jsonify, request
import threading

app = Flask(__name__)

MAX_PER_ROOM = 8
ADMIN_PASSWORD = "supersecret123"

rooms = {
    "Room 1": {"count": 0, "link": "https://vdo.ninja/?room=room1"},
    "Room 2": {"count": 0, "link": "https://vdo.ninja/?room=room2"},
    "Room 3": {"count": 0, "link": "https://vdo.ninja/?room=room3"},
    "Room 4": {"count": 0, "link": "https://vdo.ninja/?room=room4"},
    "Room 5": {"count": 0, "link": "https://vdo.ninja/?room=room5"},
    "Room 6": {"count": 0, "link": "https://vdo.ninja/?room=room6"},
    "Room 7": {"count": 0, "link": "https://vdo.ninja/?room=room7"},
    "Room 8": {"count": 0, "link": "https://vdo.ninja/?room=room8"},
    "Room 9": {"count": 0, "link": "https://vdo.ninja/?room=room9"},
    "Room 10": {"count": 0, "link": "https://vdo.ninja/?room=room10"},
    "Room 11": {"count": 0, "link": "https://vdo.ninja/?room=room11"},
    "Room 12": {"count": 0, "link": "https://vdo.ninja/?room=room12"},
    "Room 13": {"count": 0, "link": "https://vdo.ninja/?room=room13"},
    "Room 14": {"count": 0, "link": "https://vdo.ninja/?room=room14"},
    "Room 15": {"count": 0, "link": "https://vdo.ninja/?room=room15"},
}

lock = threading.Lock()
assigned_users = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/assign", methods=["POST"])
def assign_room():
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID required"}), 400

    with lock:
        # If already assigned, return same room
        if user_id in assigned_users:
            return jsonify(assigned_users[user_id])

        # Assign new room
        for room_name, room in rooms.items():
            if room["count"] < MAX_PER_ROOM:
                room["count"] += 1
                assigned_users[user_id] = {
                    "room_name": room_name,
                    "link": room["link"]
                }
                return jsonify(assigned_users[user_id])

    return jsonify({"error": "All rooms are full"}), 400

@app.route("/admin")
def admin_page():
    return render_template("admin.html")

@app.route("/admin/data", methods=["POST"])
def admin_data():
    password = request.json.get("password")

    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify({
        "rooms": rooms,
        "total_users": len(assigned_users)
    })


@app.route("/admin/reset", methods=["POST"])
def admin_reset():
    password = request.json.get("password")

    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Unauthorized"}), 403

    with lock:
        for room in rooms:
            rooms[room]["count"] = 0
        assigned_users.clear()

    return jsonify({"message": "System reset successful"})


if __name__ == "__main__":
    app.run(debug=True)
