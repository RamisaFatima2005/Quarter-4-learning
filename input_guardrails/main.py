import os
import asyncio
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,
    InputGuardrailTripwireTriggered, TResponseInputItem, input_guardrail, GuardrailFunctionOutput
)
from agents.run import RunConfig
import rich
from dotenv import load_dotenv
from pydantic import BaseModel

# -----------------------------
# Load API Keys
# -----------------------------
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not present in .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)


class TimingsChange(BaseModel):
    reasoning: str
    isChange: bool
    
admin_agent= Agent(
    name="CheckerAgent",
    instructions="""
    You are a checker. Your job is to analyze if the student is asking
    to change, shift, or move their class timings.
    If yes → set isChange=True, otherwise False.
    """,
    model=model,
    output_type=TimingsChange
)

@input_guardrail
async def timings_change(ctx, agent:Agent, input:str | list[TResponseInputItem])->GuardrailFunctionOutput:
    result= await Runner.run(admin_agent,input, context=ctx)
    rich.print("Guardrail Check Output: ", result.final_output)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.isChange
    )

teacher_agent= Agent(
    name="Teacher Agent",
    instructions="You are a teacher agent. Help students with their academic questions only.",
    input_guardrails=[timings_change],
    model=model
)

async def main():
    try:
        result = await Runner.run(
            starting_agent=teacher_agent,
            # 👇 Prompt (change class timings request → tripwire should trigger)
            # input="Sir can you please explain me topic again?",
            input="Sir, can you please change my class timings😭😭",
            # run_config=config
        )
        rich.print("[bold green]Final Output:[/bold green]", result.final_output)

    except InputGuardrailTripwireTriggered:
        rich.print("[bold red]LOGS: Input Guardrail Triggered (Class Timing Change Detected)[/bold red]")

if __name__ == "__main__":
    asyncio.run(main())