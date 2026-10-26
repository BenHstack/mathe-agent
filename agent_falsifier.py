import os, requests, subprocess

api_key = os.environ.get("GROQ_API_KEY")
issue_number = os.environ["ISSUE_NUMBER"]
issue_context = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body,comments"]).decode("utf-8")

prompt = f"""Du bist ein brillanter Mathematiker für Graphentheorie.
Hier ist der bisherige Verlauf:
{issue_context}

Deine Aufgabe: Schreibe einen vollständigen, mathematisch strengen Beweis für die Vermutung (oder formalisiere das gefundene Gegenbeispiel).
Konzentriere dich auf den Kern des Beweises. Du musst nicht die gesamte Theorie erklären. Fasse Beispiele für Graphklassen in ein oder zwei Sätzen zusammen.
Nutze LaTeX-Formatierung für Formeln (z.B. $V(G)$ für die Knotenmenge).
Schreibe deinen Beweis Schritt für Schritt und begründe jeden Übergang.
WICHTIG: Beende deine Antwort mit [BEWEIS_FERTIG].
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "max_tokens": 3000}
)

if "choices" not in response.json() or not response.json()["choices"]:
    print("❌ API-Fehler:", response.text)
    raise SystemExit(1)

proof_text = response.json()["choices"][0]["message"]["content"]

with open("beweis.md", "w") as f:
    f.write(f"# Beweis für Issue #{issue_number}\n\n" + proof_text)

subprocess.run(["git", "config", "user.name", "Prover-Agent"], check=True)
subprocess.run(["git", "config", "user.email", "prover@agent.com"], check=True)
subprocess.run(["git", "checkout", "-B", f"proof/issue-{issue_number}"], check=True) 
subprocess.run(["git", "add", "beweis.md"], check=True)
subprocess.run(["git", "commit", "-m", "Beweis generiert"], check=True)
subprocess.run(["git", "push", "origin", f"proof/issue-{issue_number}"], check=True)
subprocess.run(["gh", "pr", "create", "--title", f"Beweis für #{issue_number}", "--body", f"Dieser PR schließt Issue #{issue_number}.", "--base", "main", "--head", f"proof/issue-{issue_number}"], check=True)
