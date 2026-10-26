import os, requests, subprocess

api_key = os.environ.get("GROQ_API_KEY")
pr_number = os.environ["PR_NUMBER"]
proof_content = subprocess.check_output(["gh", "pr", "diff", pr_number]).decode("utf-8")

prompt = f"""Du bist ein extrem strenger, pedantischer Mathematik-Professor für Graphentheorie.
Hier ist der eingereichte Beweis:
{proof_content}

Prüfe jeden Schritt. Suche nach Lücken, Zirkelschlüssen, falsch angewendeten Theoremen (z.B. Kellys Lemma) oder ungenauen Definitionen von "unlabelled" oder "isomorph".
Schreibe dein Review frei und ausführlich. Wenn du Fehler findest, erkläre genau, was falsch ist.
Am Ende deiner Antwort musst du dich entscheiden:
Wenn der Beweis wasserdicht ist, schreibe exakt: [ENTSCHEIDUNG: APPROVED]
Wenn der Beweis fehlerhaft ist, schreibe exakt: [ENTSCHEIDUNG: REJECTED]
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
)
review_text = response.json()["choices"][0]["message"]["content"]

subprocess.run(["gh", "pr", "comment", pr_number, "--body", f"### 🕵️ Reviewer\n{review_text}"])

if "[ENTSCHEIDUNG: APPROVED]" in review_text:
    subprocess.run(["gh", "pr", "review", pr_number, "--approve", "--body", "Wasserdicht. Freigegeben."])
    subprocess.run(["gh", "pr", "merge", pr_number, "--merge", "--delete-branch"])
else:
    subprocess.run(["gh", "pr", "review", pr_number, "--request-changes", "--body", "Bitte überarbeiten. Siehe Review-Kommentar."])
