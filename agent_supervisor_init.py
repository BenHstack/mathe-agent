import os, requests, subprocess, time


api_key = os.environ.get("GROQ_API_KEY")
issue_number = os.environ["ISSUE_NUMBER"]
issue_body = subprocess.check_output(["gh", "issue", "view", issue_number, "--json", "body", "-q", ".body"], text=True)

prompt = f"""You are the Supervisor and lead mathematician for a proof farm.
Here is the new task:
{issue_body}

Your task:
1. Analyze the statement. Define the central terms.
2. Develop a research strategy. Should the worker focus on finding a counterexample first? Which proof technique (induction, contradiction, etc.) seems most promising?
3. Write a clear, directive message for your Worker (the agent who will try to falsify and prove the statement).

Keep your analysis concise.
IMPORTANT: End your response with the exact word [STRATEGY_COMPLETE].
"""

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000}
)

answer = response.json()["choices"][0]["message"]["content"]
subprocess.run(["gh", "issue", "comment", issue_number, "--body", f"### 🎩 Supervisor (Initial Strategy)\n{answer}"], check=True)
subprocess.run(["gh", "issue", "edit", issue_number, "--add-label", "status-ready-for-work"], check=True)
