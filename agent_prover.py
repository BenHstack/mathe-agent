import os, requests, subprocess

api_key = os.environ.get("GROQ_API_KEY")
issue_number = os.environ["ISSUE_NUMBER"]
issue_context = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body,comments"]).decode("utf-8")

prompt = f"""Du bist ein brillanter Mathematiker für Graphentheorie.
Hier ist der bisherige Verlauf (Aufgabe + Manager + Falsifizierer):
{issue_context}

Deine Aufgabe: Schreibe einen vollständigen, mathematisch strengen Beweis für die Vermutung (oder formalisiere das gefundene Gegenbeispiel).
Nutze die Ideen des Managers und des Falsifizierers als Inspiration, aber du darfst auch einen völlig eigenen, besseren Weg einschlagen.
Nutze LaTeX-Formatierung für Formeln (z.B. $V(G)$ für die Knotenmenge).
Schreibe deinen Beweis Schritt für Schritt und begründe jeden Übergang.
WICHTIG: Beende deine Antwort mit [BEWEIS_FERTIG].
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
)
proof_text = response.json()["choices"][0]["message"]["content"]

with open("beweis.md", "w") as f:
    f.write(f"# Beweis für Issue #{issue_number}\n\n" + proof_text)

subprocess.run(["git", "config", "user.name", "Prover-Agent"])
subprocess.run(["git", "config", "user.email", "prover@agent.com"])
subprocess.run(["git", "checkout", "-b", f"proof/issue-{issue_number}"])
subprocess.run(["git", "add", "beweis.md"])
subprocess.run(["git", "commit", "-m", "Beweis generiert"])
subprocess.run(["git", "push", "origin", f"proof/issue-{issue_number}"])
subprocess.run(["gh", "pr", "create", "--title", f"Beweis für #{issue_number}", "--body", f"Dieser PR schließt Issue #{issue_number}.", "--base", "main", "--head", f"proof/issue-{issue_number}"])
