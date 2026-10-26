import os, requests, subprocess

api_key = os.environ.get("GROQ_API_KEY") # Sicher aus der Umgebung geladen
issue_number = os.environ["ISSUE_NUMBER"]
issue_body = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body", "-q", ".body"]).decode("utf-8")

prompt = f"""Du bist der leitende Mathematiker für Graphentheorie.
Hier ist die neue Aufgabe:
{issue_body}

Deine Aufgabe:
1. Analysiere die Vermutung. Definiere die zentralen Begriffe (Deck, unlabelled, isomorph) präzise.
2. Welche bekannten Sätze (z.B. Kellys Lemma) könnten hier relevant sein?
3. Entwickle eine Forschungsstrategie: Sollte das Team zuerst versuchen, die Vermutung für spezielle Graphklassen (z.B. Bäume, reguläre Graphen) zu beweisen? Oder gibt es einen Grund, warum ein Gegenbeispiel existieren könnte?
4. Formuliere eine klare, aber offene "To-Do-Liste" für den Falsifizierer.

Du hast völlige mathematische Freiheit. Schreibe deine Gedanken ausführlich.
WICHTIG: Beende deine Antwort mit dem Wort [STRATEGIE_FERTIG].
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
)
answer = response.json()["choices"][0]["message"]["content"]

subprocess.run(["gh", "issue", "comment", issue_number, "--body", f"### 🧠 Manager (Strategie)\n{answer}"])
subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status: ready-for-falsification"])
