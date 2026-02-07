import asyncio

from dotenv import load_dotenv
import speech_recognition as sr
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer


load_dotenv()

client = OpenAI()
async_client = AsyncOpenAI()


async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Always speak in a cheerful manner with full of delight and happiness.",
        input=speech,
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)


def main():
    r = sr.Recognizer()  # speech to text

    SYSTEM_PROMPT = f"""
                You are an expert voice agent. You are given the transcript of 
                user has said using voice.
                You need to output as if you are an a voice agent and whatever you
                speak will be converted back to the audio using AI and play back to user.
            """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    with sr.Microphone() as source:  # Access user microphone
        r.adjust_for_ambient_noise(source)  # cutting background noise
        r.pause_threshold = 2
        while True:
            print("Speak something...")
            audio = r.listen(source)

            print("Processing audio (STT)...")
            stt = r.recognize_google(audio)

            print("You said: " + stt)

            messages.append({"role": "user", "content": stt})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )

            print("🤖:", response.choices[0].message.content)
            asyncio.run(tts(speech=response.choices[0].message.content))


main()
