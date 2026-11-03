import os, requests, subprocess, time

# 90 Sekunden Pause
time.sleep(90)

api_key = os.environ.get("GROQ_API_KEY")
pr_number = os.environ["PR_NUMBER"]

# Issue-Nummer aus dem Branch-Namen extrahieren (z.B. proof/issue-5)
branch_name = subprocess.check_output(["gh", "pr", "view", pr_number, "--json", "headRefName", "-q", ".headRefName"], text=True).strip()
issue_number = branch_name.split("-")[-1]

# NOTFALLSCHALTER
labels = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "labels", "-q", ".labels[].name"], text=True)
if "emergency-stop" in labels:
    print("🚨 EMERGENCY STOP ACTIVATED. Reviewer is stopping.")
    raise SystemExit(0)

# ITERATIONS-ZÄHLER
commit_count_str = subprocess.check_output(["gh", "pr", "view", pr_number, "--json", "commits", "-q", ".commits | length"], text=True).strip()
commit_count = int(commit_count_str)
MAX_ITERATIONS = 5

if commit_count >= MAX_ITERATIONS:
    print(f"🛑 Maximum iterations ({MAX_ITERATIONS}) reached. Stopping!")
    subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status-needs-human"], check=True)
    subprocess.run(["gh", "pr", "comment", pr_number, "--body", "I have made 5 attempts and cannot proceed. A human must take over."], check=True)
    raise SystemExit(0)

proof_content = subprocess.check_output(["gh", "pr", "diff", pr_number], text=True)

prompt = f"""You are an extremely strict, pedantic mathematics professor for graph theory.
Here is the submitted proof:
{proof_content}

Check every step for gaps and errors.
IMPORTANT: You MUST start your response with the verdict!
Write as the very first thing either [DECISION: APPROVED] (if flawless) or [DECISION: REJECTED] (if errors exist).
Write your detailed justification AFTER that.
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000}
)

if "choices" not in response.json() or not response.json()["choices"]:
    print("❌ API Error:", response.text)
    raise SystemExit(1)

review_text = response.json()["choices"][0]["message"]["content"]

subprocess.run(["gh", "pr", "comment", pr_number, "--body", f"### 🕵️ Reviewer\n{review_text}"], check=True)

# HIER WURDE DER TAG AUF [DECISION: APPROVED] GEÄNDERT!
if "[DECISION: APPROVED]" in review_text:
    subprocess.run(["gh", "pr", "review", pr_number, "--approve", "--body", "Watertight. Approved."], check=True)
    subprocess.run(["gh", "pr", "merge", pr_number, "--merge", "--delete-branch"], check=True)
else:
    subprocess.run(["gh", "pr", "review", pr_number, "--request-changes", "--body", "Please revise. See review comments."], check=True)
