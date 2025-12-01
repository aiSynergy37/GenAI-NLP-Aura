# Exercise 2: Create a chain that extracts multiple entities with validation + auto-repair

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

class Person(BaseModel):
    name: str = Field(description="Full name of the person")
    age: int = Field(description="Age in years, must be realistic", ge=0, le=150)
    occupation: str

class Extraction(BaseModel):
    people: List[Person]
    location: str = Field(description="Main location mentioned")
    topic: str = Field(description="Main topic of the text")

# Build a chain that:
# 1. Uses the new PydanticOutputParser (not the old JsonOutputParser)
# 2. Handles parsing errors gracefully and retries with correction instructions
# 3. Uses streaming if possible

llm = ChatOpenAI(model="gpt-4o", temperature=0)

prompt = ChatPromptTemplate.from_template(
    "Extract the following from the text:\n{format_instructions}\n\nText: {text}"
)

text = """
Yesterday in Berlin, Maria Gonzalez (38) who works as a senior NLP researcher at DeepMind 
met with John Park, a 29-year-old startup founder building autonomous agents. 
They discussed the future of reasoning models over coffee.
"""

# YOUR CODE HERE: Build the chain with automatic retry on validation error
chain = None  # implement

result = chain.invoke({"text": text})
print(result)