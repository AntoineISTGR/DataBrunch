# refacto

Title: Refactor Code (/refacto)

Description: Reorganises code structure to improve design, extensibility and modularity without changing its observable behaviour.

Steps:

1. **Define the refactoring goal.** Determine why a refactor is needed: reducing coupling, extracting reusable components, implementing a design pattern, or preparing for new features.

2. **Identify problem areas.** Locate duplicated code, large classes or functions, and modules with too many responsibilities. Note dependencies and decide on a target architecture (e.g., layered, hexagonal).

3. **Plan the new structure.** Sketch the desired module and class organisation. Decide which functions or classes will move, which interfaces will be introduced, and how dependencies will be injected.

4. **Refactor incrementally.** Move code in small steps: extract a class or function, update imports, run tests, commit the change. Use IDE refactoring tools (PyCharm, VS Code) or libraries (rope) to minimise errors.

5. **Update tests and documentation.** Adjust tests to reflect the new structure. Ensure they still test behaviour, not implementation details. Update README and any architecture diagrams.

6. **Communicate changes.** Inform the team about the refactoring plan and progress. Coordinate with other feature branches to avoid merge conflicts. Provide migration notes if public APIs change.

7. **Pain Points:**

   - **Lack of test coverage** makes refactoring dangerous. Write tests before making structural changes.
   - **Big‑bang refactors** can cause downtime or broken builds. Prefer iterative approaches and ensure CI pipelines run after each step.