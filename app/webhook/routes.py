from flask import Blueprint, request, jsonify, render_template
from app.extensions import collection
from datetime import datetime
import pytz

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=['POST'])
def receiver():
    payload = request.get_json()
    event_type = request.headers.get("X-GitHub-Event")
    
    if not payload:
        return jsonify({"message": "No data"}), 400

    # Format requirements: Use UTC for time as per assessment
    utc = pytz.utc
    timestamp = datetime.now(utc).isoformat()
    
    event = {
        "request_id": "", # Will be filled below
        "author": "",
        "action": "",
        "from_branch": "",
        "to_branch": "",
        "timestamp": timestamp
    }

    if event_type == "push":
        event["action"] = "PUSH"
        event["request_id"] = payload.get("after") # Commit hash
        event["author"] = payload["pusher"]["name"]
        event["to_branch"] = payload.get("ref", "").split('/')[-1]
        
    elif event_type == "pull_request":
        event["request_id"] = str(payload["pull_request"]["id"])
        event["author"] = payload["pull_request"]["user"]["login"]
        event["from_branch"] = payload["pull_request"]["head"]["ref"]
        event["to_branch"] = payload["pull_request"]["base"]["ref"]
        
        if payload["action"] == "opened":
            event["action"] = "PULL_REQUEST"
        elif payload["action"] == "closed" and payload["pull_request"].get("merged"):
            event["action"] = "MERGE"
            event["author"] = payload["pull_request"]["merged_by"]["login"]
        else:
            return jsonify({"message": "Ignored"}), 200

    collection.insert_one(event)
    return jsonify({"message": "Success"}), 200

# UI Route (Added for local viewing)
@webhook.route('/ui')
def index():
    return render_template("index.html")

@webhook.route('/receiver_data')
def get_data():
    events = list(collection.find().sort("_id", -1))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events)