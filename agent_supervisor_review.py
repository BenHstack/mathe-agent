import os, requests, subprocess, time ,base64

# 60 Sekunden Pause, um das Groq-Rate-Limit sicher einzuhalten
time.sleep(60) 
api_key = os.environ.get("GROQ_API_KEY")
pr_number = os.environ["PR_NUMBER"]

# Issue-Nummer aus dem Branch-Namen extrahieren (z.B. proof/issue-15)
branch_name = subprocess.check_output(["gh", "pr", "view", pr_number, "--json", "headRefName", "-q", ".headRefName"], text=True).strip()
issue_number = branch_name.split("-")[-1]

# 1. Notfallschalter prüfen
labels = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "labels", "-q", ".labels[].name"], text=True)
if "emergency-stop" in labels:
    print("🚨 EMERGENCY STOP ACTIVATED.")
    raise SystemExit(0)

# 2. Iterations-Zähler prüfen (Maximal 5 Versuche)
commit_count = int(subprocess.check_output(["gh", "pr", "view", pr_number, "--json", "commits", "-q", ".commits | length"], text=True).strip())
if commit_count >= 5:
    print("🛑 Maximum iterations reached. Stopping!")
    subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status-needs-human"], check=True)
    subprocess.run(["gh", "pr", "comment", pr_number, "--body", "Max iterations reached. Human needed."], check=True)
    raise SystemExit(0)

# 3. Die originale Aufgabe aus dem Issue lesen (Verhindert Halluzinationen)
issue_body = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body", "-q", ".body"], text=True)

# Hole den Inhalt der Datei beweis.md direkt aus dem PR-Branch
repo_name = subprocess.check_output(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"], text=True).strip()
try:
    # Frage die GitHub API nach der Datei im Branch (z.B. proof/issue-15)
    file_response = subprocess.check_output(
        ["gh", "api", f"repos/{repo_name}/contents/beweis.md?ref={branch_name}", "-q", ".content"], 
        text=True
    ).strip()
    # GitHub schickt die Datei Base64-kodiert. Wir müssen sie dekodieren.
    proof_content = base64.b64decode(file_response).decode("utf-8")
except subprocess.CalledProcessError:
    proof_content = "No file found in the PR branch."

prompt = f"""You are the Supervisor, an extremely strict mathematics professor.
Here is the ORIGINAL problem that needs to be solved:
{issue_body}

Here is the Worker's submitted solution (diff):
{proof_content}

Your task:
1. Check the solution for logical gaps, circular reasoning, or missing proofs, SPECIFICALLY in the context of the original problem stated above.
2. Start your response with [DECISION: APPROVED] (if flawless) or [DECISION: REJECTED] (if errors exist).
3. If rejected, do not just point out the error. Update your strategy and give the Worker a clear, new directive to fix it.
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    # TOKEN-LIMIT auf 4000 erhöht
    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "max_tokens": 4000}
)

# API-Fehlerbehandlung
if "choices" not in response.json() or not response.json()["choices"]:
    print(f"❌ API Error: {response.text}")
    raise SystemExit(1)

review_text = response.json()["choices"][0]["message"]["content"]

# Review als Kommentar im PR posten
subprocess.run(["gh", "pr", "comment", pr_number, "--body", f"### 🎩 Supervisor (Review)\n{review_text}"], check=True)

if "[DECISION: APPROVED]" in review_text:
    print("✅ Proof approved. Merging...")
    subprocess.run(["gh", "pr", "review", pr_number, "--approve", "--body", "Approved by Supervisor."], check=True)
    subprocess.run(["gh", "pr", "merge", pr_number, "--admin", "--merge", "--delete-branch"], check=True)

    subprocess.run(["gh", "issue", "comment", issue_number, "--body", "Proof approved and merged. Closing issue."], check=True)
    subprocess.run(["gh", "issue", "close", issue_number], check=True)
    print("✅ Loop successfully finished.")
else:
    print("❌ Proof rejected. Requesting changes...")
    subprocess.run(["gh", "pr", "review", pr_number, "--request-changes", "--body", "Revise according to Supervisor feedback."], check=True)
    
    # Kritik als neue Strategie ins Issue schreiben
    subprocess.run(["gh", "issue", "comment", issue_number, "--body", f"### 🎩 Supervisor (Updated Strategy)\n{review_text}"], check=True)
    
    # NUR das Label hinzufügen (der Worker hat es beim Start entfernt!)
    subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status-ready-for-work"], check=True)
