# refine

Title: Refine Code (/refine)

Description: Improves existing code without changing its external behaviour by cleaning up names, adding documentation and clarifying logic, thereby enhancing maintainability.

Steps:

1. **Locate code to refine.** Use static analysis tools (cyclomatic complexity reports, coverage reports) to identify complex or poorly covered functions. Solicit feedback from colleagues on sections that are difficult to understand.

2. **Rename for clarity.** Change variable, function and class names to better reflect their purpose. Replace ambiguous names (e.g., `x`, `data`) with descriptive ones (e.g., `user_count`, `response_json`).

3. **Extract and simplify.** Break long functions into smaller, single‑purpose functions. Replace deeply nested conditionals with guard clauses or helper functions. Remove dead code and unused imports.

4. **Document intent.** Add or update docstrings and inline comments to explain why the code exists and how it should be used. Follow the project’s docstring style (Google, NumPy or reST).

5. **Add type annotations and assertions.** Use type hints to clarify expected argument and return types. Insert assertions to document and enforce invariants when appropriate.

6. **Run tests.** After each refinement, run the existing test suite to ensure behaviour hasn’t changed. If no tests exist, write them first to provide confidence.

Pain Points:

- **Refining without tests** is risky, as inadvertent behaviour changes may go unnoticed. Mitigate by writing tests before refactoring.
- **Large refactors** disguised as refinements can cause merge conflicts and delays. Scope the refinements narrowly and commit changes incrementally.