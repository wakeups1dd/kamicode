"""
AIClient – wraps the Gemini API using a direct httpx call so we can apply
strict per-phase timeouts (connect / read / write / pool) that actually fire
even when the remote host is unreachable.
"""

import json
import re
import time

import httpx

from app.core.config import get_settings

settings = get_settings()

# Per-phase timeouts (seconds)
_TIMEOUT = httpx.Timeout(connect=5.0, read=25.0, write=10.0, pool=5.0)

_PLACEHOLDER_PREFIXES = ("sk-your-", "your-", "YOUR_")


def _is_placeholder(key: str) -> bool:
    return not key or any(key.startswith(p) for p in _PLACEHOLDER_PREFIXES)


class AIClient:
    def __init__(self):
        api_key = settings.GEMINI_API_KEY or ""
        base_url = settings.GEMINI_BASE_URL.rstrip("/")

        if _is_placeholder(api_key):
            self.client = None
            self._headers = {}
            self._url = ""
        else:
            self.client = True  # non-None sentinel — real calls enabled
            self._api_key = api_key
            self._url = f"{base_url}/chat/completions"
            self._headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _extract_json(self, text: str) -> str:
        """
        Robustly extract a JSON object from model output that may be wrapped
        in markdown code fences or surrounded by prose.
        """
        fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if fenced:
            return fenced.group(1).strip()

        start = text.find("{")
        if start == -1:
            raise ValueError(f"No JSON object in model response: {text[:200]!r}")

        depth = 0
        for i, ch in enumerate(text[start:], start=start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start : i + 1]

        raise ValueError(f"Unbalanced JSON in model response: {text[:200]!r}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def generate_json(self, system_prompt: str, user_prompt: str, model: str = None) -> str:
        model = model or settings.AI_MODEL

        # ── Mock path ──────────────────────────────────────────────────
        if not self.client:
            print(f"⚠️  GEMINI_API_KEY not configured. Returning mock for: {user_prompt[:50]}...")
            return self._mock_response(system_prompt, user_prompt)

        # ── Live Gemini call via httpx (enforced timeouts) ─────────────
        augmented_system = (
            system_prompt.rstrip()
            + "\n\nIMPORTANT: Respond with a valid JSON object ONLY — no markdown fences, no extra commentary."
        )

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": augmented_system},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.7,
        }

        async with httpx.AsyncClient(timeout=_TIMEOUT) as http:
            response = await http.post(self._url, headers=self._headers, json=payload)
            response.raise_for_status()

        data = response.json()
        raw = data["choices"][0]["message"]["content"] or ""
        return self._extract_json(raw)

    # ------------------------------------------------------------------
    # Mock helpers
    # ------------------------------------------------------------------

    def _mock_response(self, system_prompt: str, user_prompt: str) -> str:
        if "Rush" in system_prompt or "puzzle" in user_prompt.lower():
            return json.dumps({
                "puzzles": [
                    {
                        "type": "MCQ",
                        "difficulty": 1,
                        "content": {
                            "question": "What is the time complexity of pushing to a stack?",
                            "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
                            "answer": "O(1)",
                        },
                        "explanation": "Pushing to a stack is a constant time operation.",
                        "tags": ["stack", "basic"],
                    },
                    {
                        "type": "FILL_BLANK",
                        "difficulty": 1,
                        "content": {
                            "question": "The ______ data structure follows LIFO (Last-In-First-Out).",
                            "answer": "stack",
                        },
                        "explanation": "Stacks are LIFO structures.",
                        "tags": ["data-structures"],
                    },
                ]
            })

        return json.dumps({
            "title": "Mock Inverse Array",
            "slug": f"mock-inverse-array-{int(time.time())}",
            "description": "Reverse the given array of integers.",
            "difficulty": "easy",
            "test_cases": {
                "sample": [{"input": "1 2 3", "expected": "3 2 1"}],
                "hidden": [{"input": "5 4\n3", "expected": "3\n4 5"}],
            },
            "constraints": "1 <= n <= 100",
            "tags": ["array", "basic"],
        })
