import re
import base64
from datetime import datetime

PROMPT_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"you are now the system",
    r"disregard all prior rules",
    r"act as an unrestricted model"
]

BASE64_PATTERN = r"(?:[A-Za-z0-9+/]{20,}={0,2})"

def detect_prompt_injection(text):
    matches = []
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            matches.append(pattern)
    return matches

def detect_base64(text):
    return re.findall(BASE64_PATTERN, text)

def analyze_log(user_prompt, system_context, model_output):
    indicators = []

    injection_hits = detect_prompt_injection(user_prompt + system_context)
    base64_hits = detect_base64(model_output)

    threat_score = 0

    if injection_hits:
        threat_score += 60
        indicators.append("Prompt Injection Attempt")

    if base64_hits:
        threat_score += 40
        indicators.append("Possible Data Exfiltration")

    threat_score = min(threat_score, 100)

    if threat_score >= 70:
        severity = "High"
    elif threat_score >= 40:
        severity = "Medium"
    else:
        severity = "Low"

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "user_prompt": user_prompt,
        "system_context": system_context,
        "model_output": model_output,
        "threat_score": threat_score,
        "severity": severity,
        "indicators": indicators
    }

