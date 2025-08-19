from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunConfig, enable_verbose_stdout_logging, set_tracing_disabled
import requests
from dotenv import load_dotenv, find_dotenv
import os
# import rich

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

@function_tool
def get_current_location(city:str="Karachi", country:str="Pakistan") -> str:
    return f"Your curent location is city: {city}, {country}"


@function_tool
def get_breaking_news() -> str:
    return f"Heavy rainfall has hit Karachi today, causing waterlogging in several areas and disrupting daily life. Citizens are advised to take precautions and avoid unnecessary travel."



plant_agent=Agent(
    name="Plant Agent",
    instructions="You are plant agent repsonse the user query which is related to plant."
)
agent=Agent(
    name= "Triage Agent",
    instructions="You are a triage agent. Response user query in politely way. When user asks about location always invoke get_current_location tool, When user asks about news always invoke get_breaking_news tool, and when user asks about plantation handoff to the plant agent.",
    tools=[get_current_location, get_breaking_news],
    handoffs=[plant_agent]
)
result = Runner.run_sync(
    agent,
    """ 
        1. tell me the location?
        2. weather news of karachi?
        3. What is photosynthesis
    """,
    run_config=config
)
# print('='*50)
# rich.print("Result: ",result.last_agent.name)
# print(result.new_items)
print("Result: ",result.final_output)
