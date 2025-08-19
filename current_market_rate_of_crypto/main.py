from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunConfig, enable_verbose_stdout_logging
import requests
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

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
def crypto_price(nameid: str ) -> str:
    """
    Fetch the USD price of a cryptocurrency using CoinGecko API.
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={nameid}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    if nameid in data:
        return f"The price of {nameid} is ${data[nameid]['usd']}."
    else:
        return "Cryptocurrency not found."


crypto_agent = Agent(
    name="Crypto AI Assistant",
    instructions="You are a helpful assistant that provides cryptocurrency prices.When user asks about crypto price invoke the crypto_price function tool. If user asks questions which is not related to crypto price, politely tell them that you only provide info about crypto price.",
    tools=[crypto_price]
)

user_query=input("Enter your query related to crypto: ")
result = Runner.run_sync(    
    crypto_agent, 
    input=user_query,
    run_config=config
)
print(result.final_output) 