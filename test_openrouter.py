import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

print("Key exists:", bool(os.getenv("OPENROUTER_API_KEY")))

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    messages=[
        {
            "role": "user",
            "content": "Hello! Please count from 1 to 5."
        }
    ],
    temperature=0.2
)

print("\nRESPONSE:")
print(response.choices[0].message.content)
