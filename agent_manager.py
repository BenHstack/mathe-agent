import os, requests, subprocess

api_key = os.environ.get("GROQ_API_KEY")
issue_number = os.environ["ISSUE_NUMBER"]
issue_body = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body", "-q", ".body"]).decode("utf-8")

prompt = f"""Du bist der leitende Mathematiker für Graphentheorie.
Hier ist die neue Aufgabe:
{issue_body}

Deine Aufgabe:
1. Analysiere die Vermutung. Definiere die zentralen Begriffe präzise.
2. Welche bekannten Sätze könnten relevant sein?
3. Entwickle eine Forschungsstrategie: Sollte das Team zuerst nach Gegenbeispielen suchen oder einen direkten Beweis versuchen?
4. Formuliere eine kurze To-Do-Liste für den Falsifizierer.

Halte deine Analyse prägnant und auf den Punkt gebracht.
WICHTIG: Beende deine Antwort mit dem Wort [STRATEGIE_FERTIG].
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "max_tokens": 3000}
)

if "choices" not in response.json() or not response.json()["choices"]:
    print("❌ API-Fehler:", response.text)
    raise SystemExit(1)

answer = response.json()["choices"][0]["message"]["content"]
subprocess.run(["gh", "issue", "comment", issue_number, "--body", f"### 🧠 Manager (Strategie)\n{answer}"])
subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status-ready-for-falsification"])
