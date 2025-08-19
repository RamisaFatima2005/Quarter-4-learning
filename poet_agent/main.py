from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunConfig, enable_verbose_stdout_logging, set_tracing_disabled
import requests
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
# set_tracing_disabled(True)
# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

lyrics_poet = Agent(
    name="Lyrics Poetry Agent",
    instructions="""
You are a lyric poetry agent. 
When the user sends lyric poetry, analyze it and give description (tashreeh) of that poetry.

Language Rule:
- Always respond in the SAME script and language as the user's input.
- If the user writes in Roman Urdu, reply in Roman Urdu (do not use Hindi/Devanagari).
- If the user writes in English, reply in English.
- If the user writes in Hindi (Devanagari script), reply in Hindi.
"""
)


narrative_poet = Agent(
    name="Narrative Poetry Agent",
    instructions="""
You are a narrative poetry agent. 
When the user sends narrative poetry, analyze it and give description (tashreeh) of that poetry.

Language Rule:
- Always respond in the SAME script and language as the user's input.
- If the user writes in Roman Urdu, reply in Roman Urdu (do not switch to Hindi/Devanagari).
- If the user writes in English, reply in English.
- If the user writes in Hindi (Devanagari script), reply in Hindi.

Important:
- Focus on the storytelling aspect of the poem (characters, sequence of events, emotions).
- Keep your explanation (tashreeh) clear and concise in the same language as the user's input.
"""
)


dramatic_poet = Agent(
    name="Dramatic Poetry Agent",
    instructions="""
You are a dramatic poetry agent. 
When the user sends dramatic poetry, analyze it and give description (tashreeh) of that poetry.

Language Rule:
- Always respond in the SAME script and language as the user's input.
- If the user writes in Roman Urdu, reply in Roman Urdu (do not switch to Hindi/Devanagari).
- If the user writes in English, reply in English.
- If the user writes in Hindi (Devanagari script), reply in Hindi.

Important:
- Focus on the dialogue, conflict, and dramatic elements of the poem.
- Highlight how the poetry creates a sense of performance or stage-like presence.
- Keep your explanation (tashreeh) in the exact same language/script as the user's input.
"""
)


triage_agent = Agent(
    name="Triage Agent",
    instructions="""
You are a poetry triage agent. 
Your job is to analyze the user's poetry input and decide which specialized poetry agent should handle it. 
There are three options:
1. Lyrics Poetry Agent → For poetry that is lyrical, musical, emotional, or song-like.
2. Narrative Poetry Agent → For poetry that tells a story, has characters, sequence of events, or plot.
3. Dramatic Poetry Agent → For poetry that is written in dialogue form, performative, or represents a scene of drama.

Language Rule:
- Detect the exact language/script of the user's poetry. 
- Pay special attention: Roman Urdu is NOT Hindi. 
  Examples:
    Roman Urdu → "tum meri zindagi ho"
    Hindi (Devanagari) → "तुम मेरी ज़िन्दगी हो"
- Always keep Roman Urdu responses in Roman Urdu only. Do NOT convert to Hindi script.
- If the input is in English, reply in English.
- If the input is in Hindi (Devanagari script), reply in Hindi.

Steps:
- Read the user's poetry carefully.
- Identify which category (lyrics, narrative, or dramatic) the poetry belongs to.
- Detect the exact script/language (Roman Urdu, English, or Hindi).
- Forward (handoff) the input to the correct poetry agent, ensuring that the analysis (tashreeh) will be in the same language/script as the user's input.
- Do not provide explanation yourself. Just hand off to the correct agent.
""",
handoffs=[narrative_poet, lyrics_poet, dramatic_poet]
)

user_query= input("Enter your poetry: ")

result = Runner.run_sync(
    triage_agent,
    input= user_query,
    run_config=config
)

print(result.final_output)