import os, requests, subprocess, time

# 90 Sekunden Pause
time.sleep(90)

api_key = os.environ.get("GROQ_API_KEY")
issue_number = os.environ["ISSUE_NUMBER"]

# Notfallschalter prüfen
labels = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "labels", "-q", ".labels[].name"], text=True)
if "emergency-stop" in labels:
    print("🚨 NOTFALLSCHALTER AKTIVIERT. Agent wird gestoppt.")
    raise SystemExit(0)

issue_context = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body,comments"], text=True)

prompt = f"""You are a brilliant, creative mathematician specializing in graph theory.
Here is the context so far:
{issue_context}

Your task: Try to refute the conjecture by finding a counterexample.
Consider special graph classes where deleting vertices might lead to confusion.
If you find a counterexample, describe the graphs exactly and prove that their decks are identical.
If you don't find one, briefly and precisely explain why the structure of the decks is so powerful.

Be concise and focus on the mathematical essence.
IMPORTANT: End your response with the exact word [PROCEED_TO_PROOF].
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
subprocess.run(["gh", "issue", "comment", issue_number, "--body", f"### 🕵️ Falsifier\n{answer}"], check=True)
subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status-ready-for-proof"], check=True)
