# Exercise 1: Structured Output Parsing for LLM Responses
# Many interview questions revolve around forcing LLMs to return valid JSON/structs.

from pydantic import BaseModel, Field, ValidationError
from typing import List, Literal
import json

class Skill(BaseModel):
    name: str
    level: Literal["beginner", "intermediate", "expert"]
    years_experience: int = Field(..., ge=0, le=50)

class Candidate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r"^[^@]+@[^@]+\.[^@]+$")
    years_of_experience: int = Field(..., ge=0)
    skills: List[Skill]
    preferred_role: Literal["ML Engineer", "Data Scientist", "NLP Engineer", "GenAI Engineer"]
    available_for_interview: bool

# Task: Write a function that takes raw LLM text output and safely extracts a Candidate object
def parse_candidate_response(llm_output: str) -> Candidate | str:
    """
    The LLM might return malformed JSON, extra text, etc.
    Your job: extract and validate cleanly.
    Return the Candidate object if valid, otherwise return error message.
    """
    # YOUR CODE HERE
    pass

# Test with messy real-world outputs
messy_responses = [
    '{"name": "Alice", "email": "alice@gmail.com", "years_of_experience": 5, "skills": [{"name": "Python", "level": "expert", "years_experience": 6}], "preferred_role": "GenAI Engineer", "available_for_interview": true}',
    "Here is my info in JSON format:\n```json\n{\"name\": \"Bob\", \"email\": \"bob@outlook.com\", \"years_of_experience\": 3, \"skills\": [{\"name\": \"LangChain\", \"level\": \"intermediate\", \"years_experience\": 1}], \"preferred_role\": \"NLP Engineer\", \"available_for_interview\": true}\n```",
    "I'm Charlie and I know transformers really well...",  # completely invalid
]

for resp in messy_responses:
    print(parse_candidate_response(resp))