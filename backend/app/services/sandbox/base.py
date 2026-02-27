from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, Optional

class TestCaseResult(BaseModel):
    input: str
    expected: str
    actual: Optional[str] = None
    passed: bool
    runtime_ms: int
    error: Optional[str] = None

class ExecutionResult(BaseModel):
    verdict: str  # accepted, wrong_answer, tle, mle, runtime_error
    runtime_ms: int
    memory_kb: int
    passed_count: int
    total_count: int
    results: List[TestCaseResult]

class BaseSandbox(ABC):
    @abstractmethod
    async def execute(self, code: str, language: str, test_cases: List[dict], timeout: float = 2.0) -> ExecutionResult:
        pass
