# Chain of Thought Prompting
# This prompt encourages the model to reason through problems step-by-step.
# Make your model act more human-like by having it explain its reasoning.

from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
    You are an expert AI assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what need to be done. The PLAN can be multiple steps.
    Once you think enough, you will OUTPUT the final answer.
    
    Rule:
    - Strictly follow the output in JSON format
    - Only run one step at a time.
    - The sequence of steps is START (Where user give an input), PLAN (That can be multiple time),
        and finally OUTPUT (Which is going to display to the user)
        
    output Format:
    {
        "step": "START" or "PLAN" or "OUTPUT",
        "content": "string",
    }
    
    Examples:
    START: {"step": "START", "content": "What is the result of 2 + 3 * 5 / 10?"}
    PLAN: {"step": "PLAN","content": "Seems like user interested in mathematical problems"}
    PLAN: {"step": "PLAN", "content": "Looking at the problem, we should solve it following the BODMAS rule"}
    PLAN: {"step": "PLAN", "content": "First we should multiply 3 * 5 which is 15"}
    PLAN: {"step": "PLAN", "content": "Now The new equation is 2 + 15 / 10"}
    PLAN: {"step": "PLAN", "content": "We should now divide 15 / 10 which is 1.5"}
    PLAN: {"step": "PLAN", "content": "Now The new equation is 2 + 1.5"}
    PLAN: {"step": "PLAN", "content": "Now finally we should add 2 + 1.5 which is 3.5"}
    PLAN: {"step": "PLAN", "content": "Great we have the final answer now which is 3.5"}
    OUTPUT: {"step": "OUTPUT","content": "3.5"}  
"""

print("\n\n")

# Automate message history for chain of thought prompting
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]
user_query = input("✍️ Enter your question: ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=message_history
    )

    row_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": row_result})

    parsed_result = json.loads(row_result)

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("✅", parsed_result.get("content"))
        break


print("\n")


# response = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     response_format={"type": "json_object"},
#     messages=[
#         # Added system prompt to specialize the model
#         {"role": "system", "content": SYSTEM_PROMPT},
#         # explain the a + b whole square?
#         # This the manual way of doing history to guide the model step by step
#         {"role": "user", "content": " Can you write code adding n numbers in js?"},
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "step": "START",
#                     "content": "Can you write code adding n numbers in js?"
#                 }
#             )
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "step": "PLAN",
#                     "content": "The user wants JavaScript code to add 'n' numbers. I need to provide a function that takes an array of numbers as input and returns their sum."
#                 }
#             )
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "step": "PLAN",
#                     "content": "I will define a JavaScript function called `sumNumbers` that takes an array of numbers as an argument. Inside the function, I will use the `reduce` method to iterate over the array and calculate the sum of all its elements. Finally, I will provide the complete JavaScript code including an example of how to use the function."
#                 }
#             )
#         },
#     ]
# )

# print(response.choices[0].message.content)
