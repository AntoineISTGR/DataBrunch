# debug

Title: Debug Code (/debug)

Description: Diagnoses and resolves bugs systematically, ensuring the root cause is identified, fixed and tested against regression.

Steps:

1. **Gather context.** Clarify the expected versus actual behaviour. Collect error messages, stack traces, logs and any input that triggers the bug. Note the environment (OS, Python version, package versions).

2. **Reproduce the issue.** Create a minimal reproducible example. If the bug is intermittent, add logging or instrumentation to capture state when it occurs.

3. **Explore and isolate.** Use debugging tools (`pdb`, `ipdb`, IDE debuggers) to step through the code. Inspect variable values, watch for unexpected state changes, and follow the control flow.

4. **Form hypotheses and test them.** Based on observations, propose possible causes (race conditions, null values, incorrect assumptions) and write small tests or scripts to confirm or refute them.

5. **Implement a fix.** Once the root cause is understood, modify the code accordingly. Write a concise commit message explaining the cause and the fix.

6. **Write a regression test.** Add tests that would fail if the bug reappears. Integrate these into the test suite to prevent future regressions.

7. **Document findings.** Record the bug’s cause, how it was detected and how it was resolved. Include any environment setup needed to reproduce.

Pain Points:

- **Intermittent bugs** (e.g., concurrency issues) can be difficult to reproduce. Use deterministic seeds, add delays, or simulate concurrency to surface the issue.
- **External dependencies** (APIs, databases) may introduce instability. Use mocks or fakes to isolate the code under test.