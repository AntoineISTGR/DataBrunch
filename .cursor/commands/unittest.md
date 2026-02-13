# unittest

Title: Generate Unit Tests (/unit_test)

Description: Creates unit tests to validate the correctness of functions and ensure future changes do not introduce regressions.

Steps:

1. **Select targets for testing.** Identify core functions, methods and classes that represent the critical logic of the application. Prioritise areas with complex logic, calculations or critical side effects.

2. **Choose a testing framework.** Use `pytest` for Python or `Jest` for React projects. Install the necessary packages and ensure the framework is configured in the project (e.g., add `pytest.ini` or configure `jest.config.js`).

3. **Write test cases using the Arrange‑Act‑Assert pattern.** For each function, set up input data (Arrange), call the function (Act), and verify the output or side effects (Assert) using assertions. Use parametrisation to test multiple input/output pairs.

4. **Test error handling and edge cases.** Write tests that supply invalid inputs or simulate failures to ensure the code handles errors gracefully. Use `pytest.raises` to assert exceptions or `expect(...).toThrow()` in Jest.

5. **Use fixtures and mocks to isolate dependencies.** When a function interacts with external systems (file system, network, database), use fixtures or mocking libraries (`unittest.mock`, `pytest-mock`, `jest.mock`) to provide controlled substitutes.

6. **Integrate tests into CI.** Add a test stage in your continuous integration pipeline to run the test suite on every commit. Configure the pipeline to fail when tests fail or coverage drops below a threshold.

7. **Pain Points:**

   - **Over‑mocking** can hide integration issues. Use mocks sparingly and prefer integration tests for critical paths.
   - **Brittle tests** that tightly couple to implementation details can break unnecessarily when refactoring. Test behaviour rather than internal steps; update tests alongside code changes.