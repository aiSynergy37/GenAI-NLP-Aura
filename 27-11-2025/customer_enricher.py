# customer_enricher.py
import pandas as pd
from pydantic import BaseModel, Field, validator
from typing import Literal

class EnrichedCustomer(BaseModel):
    customer_id: int
    raw_company_name: str
    company_name_clean: str = Field(..., description="Normalized company name")
    industry: Literal["Tech", "Finance", "Healthcare", "Retail", "Education", "Other"]
    employee_count_range: Literal["1-10", "11-50", "51-200", "201-1000", "1000+"]
    confidence_score: float = Field(..., ge=0, le=1)
    website: str | None

    @validator("website")
    def valid_url(cls, v):
        if v and not v.startswith(("http://", "https://")):
            return "https://" + v
        return v

# Input: messy_customers.csv
df = pd.DataFrame({
    "customer_id": [1, 2, 3],
    "company": ["openai inc.", "Deepmind", "xAI (formerly Twitter)", "mistralAI"],
    "notes": ["Sam Altman startup", "Google subsidiary London", "Elon Musk new venture", "French startup raised 400M"]
})

# Task: Use LangChain to enrich 1 row at a time (or batch), return validated EnrichedCustomer list
# Save final result as enriched_customers.parquet and invalid_rows.csv