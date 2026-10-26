import os
import requests

token = os.environ["GITHUB_TOKEN"]

prompt = """Write a complete Julia program that finds all perfect numbers less than 10^6.
A natural number is perfect if it is equal to the sum of its divisors,
including 1 and excluding itself.
The program should print each perfect number it finds.
Output ONLY the raw Julia code, without any Markdown formatting or explanations."""

try:
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

    # WICHTIG: Zuerst den HTTP-Statuscode prüfen
    print(f"HTTP-Statuscode: {response.status_code}")
    
    # Den Rohtext ausgeben, um zu sehen, was die API wirklich zurückschickt
    print("Rohtext der Antwort:")
    print(response.text[:1000])  # Nur die ersten 1000 Zeichen anzeigen

    # Erst parsen, wenn die Antwort erfolgreich war
    response.raise_for_status()
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

except requests.exceptions.RequestException as e:
    print(f"❌ Ein Netzwerk- oder API-Fehler ist aufgetreten: {e}")
    # Hier wird der Fehler nicht verschluckt, sondern der Workflow schlägt fehl.
    raise
