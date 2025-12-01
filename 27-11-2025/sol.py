# Exercise 1: Structured Output Parsing for LLM Responses
# Many interview questions revolve around forcing LLMs to return valid JSON/structs.

from pydantic import BaseModel, Field, ValidationError
from typing import List, Literal
import json
import re

class Skill(BaseModel):
    name: str
    level: Literal["beginner", "intermediate", "expert"]
    years_experience: int = Field(..., ge=0, le=50)

class Candidate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    # Pydantic v2: use pattern= instead of regex=
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    years_of_experience: int = Field(..., ge=0)
    skills: List[Skill]
    preferred_role: Literal["ML Engineer", "Data Scientist", "NLP Engineer", "GenAI Engineer"]
    available_for_interview: bool

# Task: Write a function that takes raw LLM text output and safely extracts a Candidate object
def parse_candidate_response(llm_output: str) -> Candidate | str:
    """
    The LLM might return malformed JSON, extra text, etc.
    Extract and validate a Candidate if possible.
    Otherwise return an error message.
    """
    candidates_to_try: list[str] = []

    text = llm_output.strip()

    # 1) Try the whole text
    if text:
        candidates_to_try.append(text)

    # 2) Try JSON inside ``` ``` fences
    fenced = re.search(r"```(?:json)?(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        fenced_content = fenced.group(1).strip()
        if fenced_content:
            candidates_to_try.append(fenced_content)

    # 3) Try every { ... } block in the text
    for match in re.finditer(r"\{.*?\}", text, re.DOTALL):
        block = match.group(0).strip()
        if block:
            candidates_to_try.append(block)

    # 4) Deduplicate while preserving order
    seen = set()
    unique_candidates = []
    for c in candidates_to_try:
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)

    last_validation_error: str | None = None

    # 5) Try parsing each candidate
    for raw in unique_candidates:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue

        try:
            candidate = Candidate(**data)
            return candidate
        except ValidationError as e:
            last_validation_error = f"Validation error: {e}"

    if last_validation_error is not None:
        return last_validation_error

    return "Could not find valid candidate JSON in LLM output."


# Test with messy real-world outputs
messy_responses = [
    '{"name": "Alice", "email": "alice@gmail.com", "years_of_experience": 5, "skills": [{"name": "Python", "level": "expert", "years_experience": 6}], "preferred_role": "GenAI Engineer", "available_for_interview": true}',
    "Here is my info in JSON format:\n```json\n{\"name\": \"Bob\", \"email\": \"bob@outlook.com\", \"years_of_experience\": 3, \"skills\": [{\"name\": \"LangChain\", \"level\": \"intermediate\", \"years_experience\": 1}], \"preferred_role\": \"NLP Engineer\", \"available_for_interview\": true}\n```",
    "I'm Charlie and I know transformers really well...",  # completely invalid
]

for resp in messy_responses:
    print(parse_candidate_response(resp))
