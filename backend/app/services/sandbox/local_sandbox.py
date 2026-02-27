import asyncio
import time
import subprocess
import tempfile
import os
from typing import List
from app.services.sandbox.base import BaseSandbox, ExecutionResult, TestCaseResult

class LocalSandbox(BaseSandbox):
    def __init__(self):
        # Detect node path if available
        self.node_path = self._find_node()

    def _find_node(self):
        try:
            return subprocess.check_output(["where", "node"]).decode().splitlines()[0]
        except:
            return None

    async def execute(self, code: str, language: str, test_cases: List[dict], timeout: float = 2.0) -> ExecutionResult:
        results = []
        total_runtime = 0
        passed_count = 0
        verdict = "accepted"

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_ext = ".py" if language == "python" else ".js"
            code_file = os.path.join(tmp_dir, f"solution{file_ext}")
            
            with open(code_file, "w") as f:
                f.write(code)

            for tc in test_cases:
                input_data = tc.get("input", "")
                expected = tc.get("expected", "").strip()
                
                start_time = time.perf_counter()
                
                try:
                    if language == "python":
                        cmd = ["python", code_file]
                    elif language == "javascript":
                        if not self.node_path:
                            raise Exception("Node.js not found on system")
                        cmd = [self.node_path, code_file]
                    else:
                        raise Exception(f"Language {language} not supported by LocalSandbox")

                    proc = await asyncio.create_subprocess_exec(
                        *cmd,
                        stdin=asyncio.subprocess.PIPE,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )

                    try:
                        stdout, stderr = await asyncio.wait_for(
                            proc.communicate(input=input_data.encode()),
                            timeout=timeout
                        )
                        run_time = int((time.perf_counter() - start_time) * 1000)
                        total_runtime += run_time
                        
                        actual = stdout.decode().strip()
                        error = stderr.decode().strip()
                        
                        if proc.returncode != 0:
                            passed = False
                            tc_verdict = "runtime_error"
                            error_msg = error or f"Process exited with code {proc.returncode}"
                        else:
                            passed = (actual == expected)
                            tc_verdict = "accepted" if passed else "wrong_answer"
                            error_msg = None

                        results.append(TestCaseResult(
                            input=input_data,
                            expected=expected,
                            actual=actual,
                            passed=passed,
                            runtime_ms=run_time,
                            error=error_msg
                        ))

                        if not passed:
                            if verdict == "accepted":
                                verdict = tc_verdict
                            if tc_verdict == "runtime_error":
                                break # Stop on runtime error

                        if passed:
                            passed_count += 1

                    except asyncio.TimeoutError:
                        proc.kill()
                        total_runtime += int(timeout * 1000)
                        results.append(TestCaseResult(
                            input=input_data,
                            expected=expected,
                            passed=False,
                            runtime_ms=int(timeout * 1000),
                            error="Time Limit Exceeded"
                        ))
                        verdict = "tle"
                        break # Stop on TLE

                except Exception as e:
                    results.append(TestCaseResult(
                        input=input_data,
                        expected=expected,
                        passed=False,
                        runtime_ms=0,
                        error=str(e)
                    ))
                    verdict = "runtime_error"
                    break

        return ExecutionResult(
            verdict=verdict,
            runtime_ms=total_runtime,
            memory_kb=0, # Hard to measure precisely with subprocess on Windows
            passed_count=passed_count,
            total_count=len(test_cases),
            results=results
        )
