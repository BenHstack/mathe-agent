import os, requests, subprocess

api_key = os.environ.get("GROQ_API_KEY")
issue_number = os.environ["ISSUE_NUMBER"]

# 1. Lese den bisherigen Verlauf aus dem Issue
issue_context = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body,comments"]).decode("utf-8")

# 2. Versuche, den letzten PR und dessen Kommentare (Reviewer-Kritik) zu finden
try:
    # Wir holen uns die Kommentare aus dem PR (falls es schon einen gibt)
    pr_comments = subprocess.check_output(
        ["gh", "pr", "view", f"proof/issue-{issue_number}", "--json", "comments", "-q", ".comments[].body"],
        stderr=subprocess.DEVNULL # Unterdrückt Fehler, falls der PR noch nicht existiert
    ).decode("utf-8")
except subprocess.CalledProcessError:
    pr_comments = "Noch kein vorheriger PR oder Review vorhanden."

# 3. Der Prompt (jetzt mit der Review-Kritik)
prompt = f"""Du bist ein brillanter Mathematiker für Graphentheorie.
Hier ist der bisherige Verlauf aus dem Issue:
{issue_context}

Hier ist die Kritik des Reviewers vom letzten Versuch (falls vorhanden):
{pr_comments}

Deine Aufgabe: 
Wenn es Kritik gab, behebe die Fehler und schreibe den Beweis neu. 
Wenn es keine Kritik gab, schreibe einen vollständigen, mathematisch strengen Beweis für die Vermutung (oder formalisiere das gefundene Gegenbeispiel).
Konzentriere dich auf den Kern des Beweises. Du musst nicht die gesamte Theorie erklären. Fasse Beispiele für Graphklassen in ein oder zwei Sätzen zusammen.
Nutze LaTeX-Formatierung für Formeln (z.B. $V(G)$ für die Knotenmenge).
Schreibe deinen Beweis Schritt für Schritt und begründe jeden Übergang.
WICHTIG: Beende deine Antwort mit [BEWEIS_FERTIG].
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "model": "openai/gpt-oss-120b", 
        "messages": [{"role": "user", "content": prompt}], 
        "max_tokens": 3500 # Etwas mehr Platz für den zweiten Versuch
    }
)

if "choices" not in response.json() or not response.json()["choices"]:
    print("❌ API-Fehler:", response.text)
    raise SystemExit(1)

proof_text = response.json()["choices"][0]["message"]["content"]

# 4. Datei schreiben
with open("beweis.md", "w") as f:
    f.write(f"# Beweis für Issue #{issue_number} (Versuch 2)\n\n" + proof_text)

# 5. Git-Prozess (überschreibt den alten Branch)
subprocess.run(["git", "config", "user.name", "Prover-Agent"], check=True)
subprocess.run(["git", "config", "user.email", "prover@agent.com"], check=True)
subprocess.run(["git", "checkout", "-B", f"proof/issue-{issue_number}"], check=True) 
subprocess.run(["git", "add", "beweis.md"], check=True)
subprocess.run(["git", "commit", "-m", "Beweis generiert (Versuch 2)"], check=True)
subprocess.run(["git", "push", "origin", f"proof/issue-{issue_number}", "--force"], check=True) # Force push, um den alten PR zu aktualisieren

print("✅ Beweis aktualisiert.")
