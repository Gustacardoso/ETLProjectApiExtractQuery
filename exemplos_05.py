import requests
import os
import json

from dotenv import load_dotenv

load_dotenv()

url = "https://api.openai.com/v1/chat/completions"

openai_api_key = os.getenv("OPENAI_API_KEY")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}



data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Olá, como você está?"}
    ]
}

response = requests.post(url, headers=headers, json=data)

print(response.json()["choices"][0]["message"]["content"])
