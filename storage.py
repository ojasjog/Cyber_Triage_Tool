import json
import os

LOG_FILE = "logs/incidents.json"

def load_incidents():
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as f:
        return json.load(f)

def save_incident(incident):
    incidents = load_incidents()
    incidents.insert(0, incident)

    with open(LOG_FILE, "w") as f:
        json.dump(incidents, f, indent=2)

