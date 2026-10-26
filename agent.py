import os
import requests

token = os.environ["GITHUB_TOKEN"]

prompt = """Write a complete Julia program that finds all perfect numbers less than 10^6.
A natural number is perfect if it is equal to the sum of its divisors,
including 1 and excluding itself.
The program should print each perfect number it finds.
Output ONLY the raw Julia code, without any Markdown formatting or explanations."""

response = requests.post(
    "https://models.github.ai/inference/chat/completions",
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    },
    json={
        "model": "deepseek/DeepSeek-R1",
        "messages": [{"role": "user", "content": prompt}]
    }
)

data = response.json()
code = data["choices"][0]["message"]["content"]

# Falls das Modell doch Markdown-Backticks verwendet, entfernen wir sie
if code.startswith("```"):
    code = "\n".join(code.split("\n")[1:])
if code.endswith("```"):
    code = "\n".join(code.split("\n")[:-1])

with open("perfect_numbers.jl", "w") as f:
    f.write(code)

print("Julia-Code wurde in perfect_numbers.jl geschrieben.")
