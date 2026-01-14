from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="AIzaSyC1ckkACSkXCDF78B8qWPRz6BI8h2X0Bzk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {"role": "user", "content": "Hey, I am Ginwan nice to meet you!"},
    ]
)

print(response.choices[0].message.content)
