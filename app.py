from flask import Flask, request, jsonify, render_template
from detection import analyze_log
from storage import save_incident, load_incidents

app = Flask(__name__)

@app.route("/")
def dashboard():
    incidents = load_incidents()
    return render_template("dashboard.html", incidents=incidents)

@app.route("/api/log", methods=["POST"])
def ingest_log():
    data = request.json

    user_prompt = data.get("user_prompt", "")
    system_context = data.get("system_context", "")
    model_output = data.get("model_output", "")

    result = analyze_log(user_prompt, system_context, model_output)
    save_incident(result)

    return jsonify({
        "status": "logged",
        "threat_score": result["threat_score"],
        "severity": result["severity"]
    })

if __name__ == "__main__":
    app.run(debug=True)

