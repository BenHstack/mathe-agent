import os, requests, subprocess, time

# 90 Sekunden Pause, um Rate-Limits zu vermeiden
time.sleep(90)

api_key = os.environ.get("GROQ_API_KEY")
issue_number = os.environ["ISSUE_NUMBER"]

# Notfallschalter prüfen
labels = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "labels", "-q", ".labels[].name"], text=True)
if "emergency-stop" in labels:
    print("🚨 NOTFALLSCHALTER AKTIVIERT. Agent wird gestoppt.")
    raise SystemExit(0)
    
issue_body = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body", "-q", ".body"], text=True)

prompt = f"""You are the lead mathematician for graph theory.
Here is the new task:
{issue_body}

Your task:
1. Analyze the conjecture. Define the central terms precisely.
2. Which known theorems could be relevant?
3. Develop a research strategy: Should the team look for counterexamples first, or attempt a direct proof?
4. Formulate a brief to-do list for the falsifier.

Keep your analysis concise and to the point.
IMPORTANT: End your response with the exact word [STRATEGY_COMPLETE].
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000}
)

if "choices" not in response.json() or not response.json()["choices"]:
    print("❌ API Error:", response.text)
    raise SystemExit(1)

answer = response.json()["choices"][0]["message"]["content"]
subprocess.run(["gh", "issue", "comment", issue_number, "--body", f"### 🧠 Manager (Strategy)\n{answer}"], check=True)
subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status-ready-for-falsification"], check=True)
