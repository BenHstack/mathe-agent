import os, requests, subprocess

api_key = os.environ.get("GROQ_API_KEY")
issue_number = os.environ["ISSUE_NUMBER"]
issue_context = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body,comments"]).decode("utf-8")

prompt = f"""Du bist ein brillanter, kreativer Mathematiker für Graphentheorie.
Hier ist der bisherige Verlauf:
{issue_context}

Deine Aufgabe: Versuche, die Vermutung zu widerlegen (ein Gegenbeispiel zu finden).
Überlege dir spezielle Graphklassen, bei denen das Löschen von Knoten zu Verwechslungen führen könnte.
Wenn du ein Gegenbeispiel findest, beschreibe die Graphen exakt und beweise, dass ihre Decks identisch sind.
Wenn du keins findest, beschreibe kurz und präzise, warum die Struktur der Decks so mächtig ist.

Fasse dich kurz und konzentriere dich auf die mathematische Essenz.
WICHTIG: Beende deine Antwort mit dem Wort [WEITER_ZUM_BEWEIS].
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
subprocess.run(["gh", "issue", "comment", issue_number, "--body", f"### 🕵️ Falsifizierer\n{answer}"])
subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status-ready-for-proof"])
