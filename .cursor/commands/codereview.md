# codereview

Title: Review Code (/code_review)

Description: Performs a structured review of code changes to ensure quality, correctness and maintainability across the project.

Steps:

1. **Determine scope and context.** Identify the commits, pull request or files to review. Read associated tickets or descriptions to understand the intent of the changes.

2. **Assess structure and design.** Evaluate whether modules are logically decomposed and follow project conventions. Look for duplication, large classes or functions and tight coupling.

3. **Verify logic and correctness.** Read through the code to see if it implements the intended behaviour. Check for edge cases, off‑by‑one errors, and unhandled exceptions. Ensure resources (files, network connections) are properly closed.

4. **Check style and readability.** Ensure the code adheres to lint rules (`ruff`, `eslint`) and formatting standards. Names should be descriptive, comments should add value, and docstrings should be present for public functions and classes.

5. **Examine tests.** Verify that unit tests cover the new or changed code. Look for tests that assert edge cases and failure conditions. Suggest additional tests if coverage is insufficient.

6. **Consider non‑functional aspects.** Think about performance (complexity, memory usage), security (input validation, injection risk), and accessibility (for UI). Raise concerns if these aspects are affected.

7. **Provide actionable feedback.** Categorise comments by severity (blocker, major, minor) and propose concrete improvements. Communicate respectfully and focus on the code, not the author.

Pain Points:

- **Focusing on style over substance** can waste reviewer time. Prioritise correctness and design issues before stylistic nits.
- **Bias and inconsistency.** Use a checklist to ensure consistent reviews across different reviewers and avoid personal preferences dominating.