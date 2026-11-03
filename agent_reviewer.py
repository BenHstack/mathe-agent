import os, requests, subprocess

api_key = os.environ.get("GROQ_API_KEY")
pr_number = os.environ["PR_NUMBER"]

# text=True macht die Ausgabe direkt zu einem String
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

# Kommentar schreiben (check=True wirft Fehler, falls Rechte fehlen)
subprocess.run(["gh", "pr", "comment", pr_number, "--body", f"### 🕵️ Reviewer\n{review_text}"], check=True)

if "[ENTSCHEIDUNG: APPROVED]" in review_text:
    subprocess.run(["gh", "pr", "review", pr_number, "--approve", "--body", "Wasserdicht. Freigegeben."], check=True)
    subprocess.run(["gh", "pr", "merge", pr_number, "--merge", "--delete-branch"], check=True)
else:
    subprocess.run(["gh", "pr", "review", pr_number, "--request-changes", "--body", "Bitte überarbeiten. Siehe Review-Kommentar."], check=True)
