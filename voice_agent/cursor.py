# Chain of Thought Prompting
# This prompt encourages the model to reason through problems step-by-step.
# Make your model act more human-like by having it explain its reasoning.

from dotenv import load_dotenv
import speech_recognition as sr
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from pydantic import BaseModel, Field
from typing import Optional
import json
import requests
import os
import asyncio

load_dotenv()

client = OpenAI()
async_client = AsyncOpenAI()


async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        instructions="Always speak in a cheerful manner with full of delight and happiness.",
        input=speech,
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)


def run_command(cmd: str):
    result = os.system(cmd)
    return result


def get_weather(city: str):
    url = f"http://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The current weather in {city} is {response.text}"
    return "Sorry, I couldn't fetch the weather information right now. Please try again later."


available_tools = {
    "get_weather": get_weather,
    "run_command": run_command,
}

SYSTEM_PROMPT = """
    You are an expert AI assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what need to be done. The PLAN can be multiple steps.
    Once you think enough, you will OUTPUT the final answer.
    You can also use a tool if required from the list of available tools.
    For every tool call wait for the OBSERVED output which is the result of the tool call.
    
    Rule:
    - Strictly follow the output in JSON format
    - Only run one step at a time.
    - The sequence of steps is START (Where user give an input), PLAN (That can be multiple time),
        and finally OUTPUT (Which is going to display to the user)
        
    output Format:
    {
        "step": "START" or "PLAN" or "OUTPUT" or "TOOL" or "OBSERVED",
        "content": "string",
        "tool": "string",         
        "input": "string",        
    }
    
    Available Tools:
    - get_weather(city: str): Take city name as input string and return the current weather information about the city.
    - run_command(cmd: str): Take command as input string and execute it in the system shell, returning the result code.
    
    Example 1:
    START: What is the result of 2 + 3 * 5 / 10?
    PLAN: {"step": "PLAN","content": "Seems like user interested in mathematical problems"}
    PLAN: {"step": "PLAN", "content": "Looking at the problem, we should solve it following the BODMAS rule"}
    PLAN: {"step": "PLAN", "content": "First we should multiply 3 * 5 which is 15"}
    PLAN: {"step": "PLAN", "content": "Now The new equation is 2 + 15 / 10"}
    PLAN: {"step": "PLAN", "content": "We should now divide 15 / 10 which is 1.5"}
    PLAN: {"step": "PLAN", "content": "Now The new equation is 2 + 1.5"}
    PLAN: {"step": "PLAN", "content": "Now finally we should add 2 + 1.5 which is 3.5"}
    PLAN: {"step": "PLAN", "content": "Great we have the final answer now which is 3.5"}
    OUTPUT: {"step": "OUTPUT","content": "3.5"}  
    
    Example 1:
    START: What is the weather in khartoum?
    PLAN: {"step": "PLAN","content": "Seems like user interested in getting weather in khartoum Sudan"}
    PLAN: {"step": "PLAN", "content": "Let see if we have any tool to get weather information"}
    PLAN: {"step": "PLAN", "content": "Great we have a tool called get_weather available for this query"}
    PLAN: {"step": "PLAN", "content": "I need to call get_weather tool with khartoum as input"}
    TOOL: {"step": "TOOL", "tool": "get_weather", "input": "Khartoum"}
    TOOL: {"step": "OBSERVED", "tool": "get_weather", "output": "The temperature in khartoum is Sunny +23°C"}
    PLAN: {"step": "PLAN", "content": "Great I get the weather info about khartoum"}
    OUTPUT: {"step": "OUTPUT","content": "The current weather in khartoum is 23°C and Sunny, please don't forget to carry your sunglasses!"}  
"""

print("Welcome to the Chain of Thought Prompting Demo!\n")

# Make structured output parsing with Pydantic


class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: START, PLAN, TOOL, OBSERVED, OUTPUT.")
    content: Optional[str] = Field(
        None, description="The optional string content.")
    tool: Optional[str] = Field(
        None, description="The ID of the tool to be called.")
    input: Optional[str] = Field(
        None, description="The input string for the tool.")


# Automate message history for chain of thought prompting
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]
r = sr.Recognizer()  # speech to text

with sr.Microphone() as source:  # Access user microphone
    r.adjust_for_ambient_noise(source)  # cutting background noise
    r.pause_threshold = 2

    while True:
        print("Speak something...")
        audio = r.listen(source)
        
        print("Processing audio (STT)...")
        user_query = r.recognize_google(audio)
        message_history.append({"role": "user", "content": user_query})

        while True:
            response = client.chat.completions.parse(
                model="gpt-4.1",
                response_format=MyOutputFormat,
                messages=message_history
            )

            row_result = response.choices[0].message.content
            message_history.append({"role": "assistant", "content": row_result})

            parsed_result = response.choices[0].message.parsed

            if parsed_result.step == "START":
                print("🔥", parsed_result.content)
                continue

            if parsed_result.step == "TOOL":
                tool_to_call = parsed_result.tool
                tool_input = parsed_result.input
                tool_response = available_tools[tool_to_call](tool_input)
                print(
                    f"🛠️ : {tool_to_call} called with input: {tool_input} = {tool_response}")
                observed_result = {"step": "OBSERVED", "tool": tool_to_call,
                                "input": tool_input, "output": tool_response}
                message_history.append(
                    {"role": "developer", "content": json.dumps(observed_result)})
                continue

            if parsed_result.step == "PLAN":
                print("🧠", parsed_result.content)
                continue

            if parsed_result.step == "OUTPUT":
                print("🤖", parsed_result.content)
                asyncio.run(tts(speech=parsed_result.content))
                break
