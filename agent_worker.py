import os, requests, subprocess, time

time.sleep(60)
api_key = os.environ.get("GROQ_API_KEY")
issue_number = os.environ["ISSUE_NUMBER"]

# Context Pruning
issue_body = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body", "-q", ".body"], text=True)

try:
    supervisor_strategy = subprocess.check_output(
        ["gh", "issue", "view", issue_number, "--json", "comments", "-q", ".comments[-1].body"], text=True
    )
except:
    supervisor_strategy = "No strategy provided."

try:
    last_pr_comment = subprocess.check_output(
        ["gh", "pr", "view", f"proof/issue-{issue_number}", "--json", "comments", "-q", ".comments[-1].body"],
        stderr=subprocess.DEVNULL, text=True
    )
except subprocess.CalledProcessError:
    last_pr_comment = "No previous reviewer critique available (this is the first attempt)."

prompt = f"""You are the Worker, a brilliant mathematician for graph theory. 
Here is the original problem:
{issue_body}

Here is the latest directive from your Supervisor:
{supervisor_strategy}

Here is the latest critique from your previous attempt (if available):
{last_pr_comment}

Your task:
1. Try to find a counterexample to disprove the statement. If you find one, present it clearly as a disproof.
2. If you cannot find a counterexample, write a complete, rigorous mathematical proof for the statement.
If there is a critique from the Supervisor, address those exact points. 
Use LaTeX formatting for formulas (e.g., $V(G)$).
IMPORTANT: End your response with the exact word [WORK_COMPLETE].
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "max_tokens": 4000} # <-- ERHÖHT
)

# NEU: Fehlerprüfung
if "choices" not in response.json() or not response.json()["choices"]:
    print(f"❌ API Error: {response.text}")
    raise SystemExit(1)

proof_text = response.json()["choices"][0]["message"]["content"]

with open("beweis.md", "w") as f:
    f.write(f"# Solution for Issue #{issue_number}\n\n" + proof_text)

subprocess.run(["git", "config", "user.name", "Worker-Agent"], check=True)
subprocess.run(["git", "config", "user.email", "worker@agent.com"], check=True)
subprocess.run(["git", "checkout", "-B", f"proof/issue-{issue_number}"], check=True) 
subprocess.run(["git", "add", "beweis.md"], check=True)
subprocess.run(["git", "commit", "-m", "Worker solution generated"], check=True)
subprocess.run(["git", "push", "origin", f"proof/issue-{issue_number}", "--force"], check=True)

# Erstelle den PR nur, wenn es noch keinen gibt
try:
    subprocess.run(["gh", "pr", "create", "--title", f"Proof for #{issue_number}", "--body", f"Closes #{issue_number}.", "--base", "main", "--head", f"proof/issue-{issue_number}"], check=True)
except subprocess.CalledProcessError:
    print("PR already exists, force-pushed update.")

print("✅ Worker finished. Removing 'status-ready-for-work' label to reset the loop.")
subprocess.run(["gh", "issue", "edit", issue_number, "--remove-label", "status-ready-for-work"], check=True)

print("✅ Worker finished. Triggering Supervisor Review via API...")
# Finde die PR-Nummer heraus
pr_info = subprocess.check_output(
    ["gh", "pr", "list", "--head", f"proof/issue-{issue_number}", "--json", "number", "-q", ".[0].number"], 
    text=True
).strip()

if pr_info:
    # Starte den Supervisor-Workflow und übergib die PR-Nummer
    subprocess.run(
        ["gh", "workflow", "run", "2 - Supervisor Review", "-f", f"pr_number={pr_info}"], 
        check=True
    )
