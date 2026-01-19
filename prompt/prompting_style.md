# Prompting Style

# 1- Alpaca Style Prompting
# This prompt style is inspired by the Alpaca model, used by metaLama.

### Instructions:<SYSTEM PROMPT>\n
### Input:<USER QUERY>\n
### Response:\n

# 2- ChatML Style Prompting
# The same style as used in OpenAI's ChatGPT and GPT-4 models.
# This style uses roles like system, user, and assistant to structure the conversation.
### {"role": "user" | "system" | "assistant", "content": "string"} 

# 3- INST Style Prompting (Instruction Style Prompting)
# used LLaMA 2 models.
### [INST] What is the time Now? [/INST] # This is a user query.

