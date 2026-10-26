import os, requests, subprocess

issue_number = os.environ["ISSUE_NUMBER"]
issue_context = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body,comments"]).decode("utf-8")

prompt = f"""Du bist ein brillanter, kreativer Mathematiker für Graphentheorie.
Hier ist der bisherige Verlauf (Aufgabe + Strategie des Managers):
{issue_context}

Deine Aufgabe: Versuche, die Vermutung zu widerlegen (ein Gegenbeispiel zu finden).
Du hast völlige Freiheit in deiner Herangehensweise. 
Überlege dir zum Beispiel: 
- Gibt es spezielle Graphklassen (z.B. Bäume, reguläre Graphen, Graphen mit bestimmten Symmetrien), bei denen das Löschen von Knoten zu Verwechslungen führen könnte?
- Kannst du zwei nicht-isomorphe Graphen konstruieren, die dieselben unlabelled Subgraphen (das gleiche Deck) haben?
Wenn du ein Gegenbeispiel findest, beschreibe die beiden Graphen exakt (z.B. als Adjazenzliste) und beweise, dass ihre Decks identisch, die Graphen aber nicht isomorph sind.
Wenn du keins findest, beschreibe, warum die Struktur der Decks so mächtig ist, dass sie den Graphen eindeutig rekonstruierbar macht.

Schreibe deine Gedanken frei und ausführlich.
WICHTIG: Beende deine Antwort mit dem Wort [WEITER_ZUM_BEWEIS].
"""

response = requests.post(
    "https://text.pollinations.ai/openai",
    headers={"Content-Type": "application/json"},
    json={"model": "openai", "messages": [{"role": "user", "content": prompt}]}
)
answer = response.json()["choices"][0]["message"]["content"]

subprocess.run(["gh", "issue", "comment", issue_number, "--body", f"### 🕵️ Falsifizierer\n{answer}"])
subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status: ready-for-proof"])
