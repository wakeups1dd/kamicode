from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Any
from datetime import date
import uuid

class TestCase(BaseModel):
    input: str
    expected: str

class ProblemTestCases(BaseModel):
    sample: List[TestCase]
    hidden: List[TestCase]

class ProblemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    description: str
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    constraints: Optional[str] = None
    tags: List[str] = []

class ProblemCreate(ProblemBase):
    test_cases: ProblemTestCases

class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    constraints: Optional[str] = None
    tags: Optional[List[str]] = None
    test_cases: Optional[ProblemTestCases] = None

class ProblemResponse(ProblemBase):
    id: str
    daily_date: Optional[date] = None
    sample_test_cases: List[TestCase]

    @model_validator(mode="before")
    @classmethod
    def extract_sample_tests(cls, data: Any) -> Any:
        if isinstance(data, dict):
            tc = data.get("test_cases", {})
            data["sample_test_cases"] = tc.get("sample", []) if isinstance(tc, dict) else []
            return data
        
        tc = getattr(data, "test_cases", {})
        sample_tests = tc.get("sample", []) if isinstance(tc, dict) else []
            
        return {
            "id": getattr(data, "id", None),
            "title": getattr(data, "title", None),
            "slug": getattr(data, "slug", None),
            "description": getattr(data, "description", None),
            "difficulty": getattr(data, "difficulty", None),
            "constraints": getattr(data, "constraints", None),
            "tags": getattr(data, "tags", []),
            "daily_date": getattr(data, "daily_date", None),
            "sample_test_cases": sample_tests
        }

    class Config:
        from_attributes = True

class ProblemListResponse(BaseModel):
    id: str
    title: str
    slug: str
    difficulty: str
    tags: List[str]
    daily_date: Optional[date] = None

    class Config:
        from_attributes = True
