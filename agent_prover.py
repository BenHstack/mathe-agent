import os, requests, subprocess, time

# 90 Sekunden Pause
time.sleep(90)

api_key = os.environ.get("GROQ_API_KEY")
issue_number = os.environ["ISSUE_NUMBER"]

# Notfallschalter prüfen
labels = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "labels", "-q", ".labels[].name"], text=True)
if "emergency-stop" in labels:
    print("🚨 NOTFALLSCHALTER AKTIVIERT. Agent wird gestoppt.")
    raise SystemExit(0)

# CONTEXT PRUNING: Lese nur die originale Aufgabe (ohne Kommentare)
issue_body = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body", "-q", ".body"], text=True)

# CONTEXT PRUNING: Lese nur den ALLERLETZTEN Kommentar aus dem PR
try:
    last_pr_comment = subprocess.check_output(
        ["gh", "pr", "view", f"proof/issue-{issue_number}", "--json", "comments", "-q", ".comments[-1].body"],
        stderr=subprocess.DEVNULL, text=True
    )
except subprocess.CalledProcessError:
    last_pr_comment = "No previous reviewer critique available."

prompt = f"""You are a brilliant mathematician for graph theory.
Here is the original problem:
{issue_body}

Here is the latest critique from the reviewer (if available):
{last_pr_comment}

Your task: 
If there is critique, fix the errors and rewrite the proof. 
If there is no critique, write a complete, mathematically rigorous proof for the conjecture (or formalize the counterexample).
Focus on the core of the proof. Summarize examples for graph classes in one or two sentences.
Use LaTeX formatting for formulas (e.g., $V(G)$ for the vertex set).
Write your proof step by step and justify every transition.
IMPORTANT: End your response with the exact word [PROOF_COMPLETE].
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000}
)

if "choices" not in response.json() or not response.json()["choices"]:
    print("❌ API Error:", response.text)
    raise SystemExit(1)

proof_text = response.json()["choices"][0]["message"]["content"]

with open("beweis.md", "w") as f:
    f.write(f"# Proof for Issue #{issue_number}\n\n" + proof_text)

subprocess.run(["git", "config", "user.name", "Prover-Agent"], check=True)
subprocess.run(["git", "config", "user.email", "prover@agent.com"], check=True)
subprocess.run(["git", "checkout", "-B", f"proof/issue-{issue_number}"], check=True) 
subprocess.run(["git", "add", "beweis.md"], check=True)
subprocess.run(["git", "commit", "-m", "Proof generated"], check=True)
subprocess.run(["git", "push", "origin", f"proof/issue-{issue_number}", "--force"], check=True)
subprocess.run(["gh", "pr", "create", "--title", f"Proof for #{issue_number}", "--body", f"Closes #{issue_number}.", "--base", "main", "--head", f"proof/issue-{issue_number}"], check=True)
