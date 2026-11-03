import os, requests, subprocess, time

time.sleep(90)
api_key = os.environ.get("GROQ_API_KEY")
pr_number = os.environ["PR_NUMBER"]

branch_name = subprocess.check_output(["gh", "pr", "view", pr_number, "--json", "headRefName", "-q", ".headRefName"], text=True).strip()
issue_number = branch_name.split("-")[-1]

# Notfallschalter
labels = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "labels", "-q", ".labels[].name"], text=True)
if "emergency-stop" in labels:
    raise SystemExit(0)

# Iterations-Zähler
commit_count = int(subprocess.check_output(["gh", "pr", "view", pr_number, "--json", "commits", "-q", ".commits | length"], text=True).strip())
if commit_count >= 5:
    subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status-needs-human"], check=True)
    subprocess.run(["gh", "pr", "comment", pr_number, "--body", "Max iterations reached. Human needed."], check=True)
    raise SystemExit(0)

proof_content = subprocess.check_output(["gh", "pr", "diff", pr_number], text=True)

prompt = f"""You are the Supervisor. Your Worker has submitted the following solution:
{proof_content}

Your task:
1. Check for logical gaps, circular reasoning, or missing counterexamples.
2. Start your response with [DECISION: APPROVED] (if flawless) or [DECISION: REJECTED] (if errors exist).
3. If rejected, do not just point out the error. Update your strategy and give the Worker a clear, new directive to fix it.
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000}
)

review_text = response.json()["choices"][0]["message"]["content"]

subprocess.run(["gh", "pr", "comment", pr_number, "--body", f"### 🎩 Supervisor (Review)\n{review_text}"], check=True)

if "[DECISION: APPROVED]" in review_text:
    subprocess.run(["gh", "pr", "review", pr_number, "--approve", "--body", "Approved by Supervisor."], check=True)
    subprocess.run(["gh", "pr", "merge", pr_number, "--merge", "--delete-branch"], check=True)
else:
    subprocess.run(["gh", "pr", "review", pr_number, "--request-changes", "--body", "Revise according to Supervisor feedback."], check=True)
    
    # NEU: Kritik als neue Strategie ins Issue schreiben und Loop starten
    subprocess.run(["gh", "issue", "comment", issue_number, "--body", f"### 🎩 Supervisor (Updated Strategy)\n{review_text}"], check=True)
    subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status-ready-for-work"], check=True)
