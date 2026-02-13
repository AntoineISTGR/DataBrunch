# code

Title: Generate Code (/code)

Description: Implements planned features or functions using clean, idiomatic Python (or JavaScript when relevant), adhering to best practices for maintainability and testability.

Steps:

1. **Review the plan.** Re‑read the `/plan` output to understand requirements and ensure all ambiguities are addressed. Seek clarification before writing code if anything is unclear.

2. **Write small, pure functions or components.** Decompose tasks into functions that perform one job. Use descriptive names, type hints and docstrings. For React, create focused components with clear props and minimal internal state.

3. **Separate concerns.** Keep business logic separate from I/O. For example, read inputs and write outputs outside of core logic functions. Use dependency injection to pass in collaborators (database connections, HTTP clients), making testing easier.

4. **Handle errors thoughtfully.** Anticipate failure modes (invalid inputs, network errors, unavailable resources). Catch exceptions where recovery is possible; otherwise allow them to propagate. Provide clear, actionable error messages.

5. **Write tests alongside code.** Create unit tests for each function and component. Test normal cases, edge cases and error conditions. Use mocks or fixtures to isolate dependencies.

6. **Run quality checks frequently.** Use linters (`ruff`, `eslint`), type checkers (`mypy`, TypeScript), and test runners (`pytest`, Jest) on every change. Refactor incrementally to improve readability and reduce complexity.

7. **Pain points:**

   - **Mixing responsibilities** (e.g., performing network requests inside business logic) makes code hard to test. Mitigate by clearly separating layers.
   - **No tests** leads to fragile code. Write tests before or alongside implementation.
   - **Overengineering** can slow development. Implement the simplest solution that meets requirements, then refactor when needed.