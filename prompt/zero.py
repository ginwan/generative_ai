# Zero shot prompting ==> basically means giving the instruction directly to the model. "just say you have to do this"
# Asking an AI to do a task without giving it any examples first.

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    # api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Zero-shot prompting with system message to specialize the model
SYSTEM_PROMPT = """You should only answer code related questions. You should't answer anything else. 
                If the question is not related to code, respond with 'Sorry.'.
                Your name is CodeBot."""

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        # Added system prompt to specialize the model
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Can you write python code that translate English to Malayalam?"},
    ]
)

print(response.choices[0].message.content)
