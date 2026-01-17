# Few-shot prompting ==> means giving the instruction along with some examples.
# This is widely used to improve model performance on specific tasks by providing context.

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    # api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Few-shot prompting with few examples and system message to specialize the model
SYSTEM_PROMPT = """You should only answer code related questions. You should't answer anything else. 
                If the question is not related to code, respond with 'Sorry.'.
                Your name is CodeBot.
                
                Rule:
                - Strictly follow the output in JSON format
                
                output Format:
                {{
                    "code": "string" or Null,
                    "isCodingQuestion": boolean
                }}
                
                Examples:
                Q: Can you explain the a + b whole square?
                A: 
                {
                    "code": Null,
                    "isCodingQuestion": False
                }
                
                Q: Write a python function to add two numbers.
                A: 
                {
                    "code": "def add(a, b):\n    return a + b",
                    "isCodingQuestion": True
                }
                
                """

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        # Added system prompt to specialize the model
        {"role": "system", "content": SYSTEM_PROMPT},
        # explain the a + b whole square?
        {"role": "user", "content": " Can you write code adding n numbers in js?"},
    ]
)

print(response.choices[0].message.content)
