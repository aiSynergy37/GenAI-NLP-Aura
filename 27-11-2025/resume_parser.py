# resume_parser.py
from pathlib import Path
from typing import List
import json
from pydantic import BaseModel, Field, EmailStr, validator
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import PyPDF2
import docx

class WorkExperience(BaseModel):
    company: str
    role: str
    duration_years: float = Field(..., ge=0.1, le=50)
    technologies: List[str]

class CandidateResume(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(..., regex=r"^\+?[\d\s\-\(\)]{10,20}$")
    years_of_experience: float = Field(..., ge=0)
    skills: List[str] = Field(..., min_items=3)
    work_history: List[WorkExperience]
    highest_education: str
    linkedin_url: str | None = None

    @validator("skills")
    def lowercase_skills(cls, v):
        return [s.strip().lower() for s in v if s.strip()]

# Task: Implement this function
def extract_text_from_file(file_path: Path) -> str:
    """Support PDF and DOCX"""
    # YOUR CODE HERE
    pass

def build_resume_extraction_chain():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    parser = PydanticOutputParser(pydantic_object=CandidateResume)
    
    prompt = ChatPromptTemplate.from_template(
        "Extract candidate info from this resume. Return ONLY valid JSON.\n"
        "{format_instructions}\n\n"
        "Resume text:\n{text}\n\n"
        "If information is missing or unclear, use null/empty where appropriate."
    )
    # Return chain that auto-retries on validation error (up to 2 times)
    # YOUR CODE HERE
    pass

def process_resumes_folder(input_folder: str = "resumes/", output_valid: str = "candidates.jsonl"):
    chain = build_resume_extraction_chain()
    input_path = Path(input_folder)
    
    valid_count = rejected_count = 0
    rejected_dir = Path("rejected")
    rejected_dir.mkdir(exist_ok=True)
    
    for file_path in input_path.glob("*.pdf"):
        # YOUR CODE HERE: full pipeline
        pass

# Run with sample resumes (create 3 fake ones to test)
# Expected: valid candidates in JSONL, malformed/invalid moved + logged