# Exercise 3: Build a ReAct Agent that MUST return structured output using tools + Pydantic

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city"""
    return f"It's 22°C and sunny in {city} today."

@tool
def calculate_expression(expression: str) -> str:
    """Safely evaluate simple math expressions"""
    import math
    allowed = {"math": math, "pi": math.pi, "e": math.e}
    try:
        return str(eval(expression, {"__builtins__": {}}, allowed))
    except:
        return "Invalid expression"

class TripPlan(BaseModel):
    destination: str = Field(..., description="City name")
    duration_days: int = Field(..., ge=1, le=30)
    activities: list[str]
    estimated_budget_usd: float = Field(..., ge=0)
    weather_summary: str

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Task: Build a ReAct agent that plans a trip and MUST return a valid TripPlan object
# Even if it uses tools multiple times, final answer must be parsed into TripPlan
# Use the new structured output methods (not .with_structured_output on tools!)

query = "Plan a 5-day trip to Tokyo for someone who loves tech museums and ramen. What's the weather like?"

# YOUR CODE HERE
agent = None
executor = None

result = executor.invoke({"input": query})
print(result["output"])
assert isinstance(result["output"], TripPlan)