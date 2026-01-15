from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        # Added system prompt to specialize the model
        {"role": "system", "content": "You are an expert in Maths and only and only answer Maths related questions. and if the quire is not related to Maths, respond with 'Sorry,I can only answer Maths related questions.'"},
        {"role": "user", "content": "Can you calculate 556879*9685"},
    ]
)

print(response.choices[0].message.content)
