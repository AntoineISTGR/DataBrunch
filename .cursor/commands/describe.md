# describe

Title: Describe Codebase (/describe)

Description: Provides an overview of the current codebase, including structure, key modules, dependencies and environment setup, to help contributors quickly understand how the system works.

Steps:

1. **Explore existing documentation.** Read `README.md`, `CONTRIBUTING.md`, `pyproject.toml`, `package.json`, or any other project documentation to understand the intended structure and tooling. Note the Python version and any required services (databases, message brokers, etc.).

2. **List the repository structure.** Generate a high‑level tree of the repository (for example, `tree -L 2`) to list top‑level directories and files. Summarise the purpose of each major module in plain language (e.g., `src/` contains application code, `tests/` contains unit tests).

3. **Identify dependencies.** Catalogue external libraries and frameworks (Django, FastAPI, React, etc.) along with their versions and roles. Highlight any custom utilities or third‑party integrations that may not be obvious from the imports.

4. **Document how to run the project.** Describe how to set up and run the project locally: installation commands, required environment variables, how to start servers or scripts, and how to execute tests. If there are multiple entry points (CLI, web server, worker), list each.

5. **Highlight critical areas.** Identify parts of the code responsible for database access, network calls, external APIs, or configuration loading. Note any areas with poor documentation or high complexity that may require further investigation.

6. **Record assumptions and open questions.** If anything is unclear, clearly state the assumptions you’ve made and suggest verifying them with maintainers or by reading additional documentation. Avoid guessing behaviour without evidence.

Pain Points:

- **Missing documentation** can leave important behaviours unknown. When documentation is absent, plan follow‑up tasks to produce it.
- **Hidden configuration** (environment variables, `.env` files) might be required to run the project. Ensure these are documented or included in examples.
- **Non‑standard layouts** can confuse newcomers. If the project uses an unusual structure, explain why and link to any conventions used.