# Exercise 4: Custom Output Parser with Self-Correction Loop (2025 production pattern)

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, ValidationError

class SelfCorrectingParser(BaseOutputParser):
    pydantic_model: type[BaseModel]
    max_retries: int = 3
    
    def parse(self, text: str) -> BaseModel:
        # Implement a parser that tries to parse, 
        # if fails → sends error back to LLM to fix
        # returns valid instance or raises after max_retries
        pass

# Use it in a chain that extracts sentiment + entities + confidence scores