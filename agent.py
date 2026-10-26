import os
import requests

token = os.environ["GITHUB_TOKEN"]

prompt = """Write a complete Julia program that finds all perfect numbers less than 10^6.
A natural number is perfect if it is equal to the sum of its divisors,
including 1 and excluding itself.
The program should print each perfect number it finds.
Output ONLY the raw Julia code, without any Markdown formatting or explanations."""

response = requests.post(
    "https://text.pollinations.ai/openai", # Pollinations Endpunkt
    headers={"Content-Type": "application/json"}, # Kein Auth-Header nötig!
    json={
        "model": "openai", # oder "mistral"
        "messages": [{"role": "user", "content": prompt}]
    }
)

# Statuscode prüfen (zur Sicherheit)
print(f"HTTP-Statuscode: {response.status_code}")

data = response.json()
code = data["choices"][0]["message"]["content"]

# Markdown-Backticks entfernen, falls vorhanden
if code.startswith("```"):
    code = "\n".join(code.split("\n")[1:])
if code.endswith("```"):
    code = "\n".join(code.split("\n")[:-1])

with open("perfect_numbers.jl", "w") as f:
    f.write(code)

print("✅ Julia-Code wurde in perfect_numbers.jl geschrieben.")
