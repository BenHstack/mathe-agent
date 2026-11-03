import os, requests, subprocess

api_key = os.environ.get("GROQ_API_KEY")
pr_number = os.environ["PR_NUMBER"]

# --- NEU: Issue-Nummer aus dem Branch-Namen extrahieren (z.B. proof/issue-5) ---
branch_name = subprocess.check_output(["gh", "pr", "view", pr_number, "--json", "headRefName", "-q", ".headRefName"], text=True).strip()
issue_number = branch_name.split("-")[-1]

# --- NEU: NOTFALLSCHALTER (Ebene 2) ---
labels = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "labels", "-q", ".labels[].name"], text=True)
if "emergency-stop" in labels:
    print("🚨 NOTFALLSCHALTER AKTIVIERT. Reviewer wird gestoppt.")
    raise SystemExit(0)

# --- NEU: ITERATIONS-ZÄHLER (Ebene 3 - optional, aber empfohlen) ---
# Prüft, wie viele Commits der Beweiser schon gemacht hat (1 Commit = 1 Versuch)
commit_count_str = subprocess.check_output(["gh", "pr", "view", pr_number, "--json", "commits", "-q", ".commits | length"], text=True).strip()
commit_count = int(commit_count_str)
MAX_ITERATIONS = 5

if commit_count >= MAX_ITERATIONS:
    print(f"🛑 Maximale Anzahl an Iterationen ({MAX_ITERATIONS}) erreicht. Abbruch!")
    subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status-needs-human"], check=True)
    subprocess.run(["gh", "pr", "comment", pr_number, "--body", "Ich habe 5 Versuche gemacht und komme nicht weiter. Ein Mensch muss übernehmen."], check=True)
    raise SystemExit(0)

# --- AB HIER BEGINNT DER NORMALE PROZESS ---
proof_content = subprocess.check_output(["gh", "pr", "diff", pr_number], text=True)

prompt = f"""Du bist ein extrem strenger, pedantischer Mathematik-Professor für Graphentheorie.
Hier ist der eingereichte Beweis:
{proof_content}

Prüfe jeden Schritt auf Lücken und Fehler.
WICHTIG: Du MUSST deine Antwort mit dem Urteil beginnen!
Schreibe als allererstes entweder [ENTSCHEIDUNG: APPROVED] (wenn fehlerfrei) oder [ENTSCHEIDUNG: REJECTED] (wenn Fehler vorhanden sind).
Schreibe DANACH deine ausführliche Begründung.
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "max_tokens": 3000}
)

if "choices" not in response.json() or not response.json()["choices"]:
    print("❌ API-Fehler:", response.text)
    raise SystemExit(1)

review_text = response.json()["choices"][0]["message"]["content"]

subprocess.run(["gh", "pr", "comment", pr_number, "--body", f"### 🕵️ Reviewer\n{review_text}"], check=True)

if "[ENTSCHEIDUNG: APPROVED]" in review_text:
    subprocess.run(["gh", "pr", "review", pr_number, "--approve", "--body", "Wasserdicht. Freigegeben."], check=True)
    subprocess.run(["gh", "pr", "merge", pr_number, "--merge", "--delete-branch"], check=True)
else:
    subprocess.run(["gh", "pr", "review", pr_number, "--request-changes", "--body", "Bitte überarbeiten. Siehe Review-Kommentar."], check=True)
