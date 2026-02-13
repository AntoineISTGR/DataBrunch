# securityscan

Title: Run Security Scan (/security_scan)

Description: Performs automated security checks on the codebase and dependencies to identify vulnerabilities and compliance issues as part of the development workflow.

Steps:

1. **Define the scope and tools.** Identify which parts of the project need scanning: source code (static analysis) and dependencies (vulnerability databases). Choose tools suitable for the stack: for Python, `bandit`, `safety` or `pip-audit`; for JavaScript, `npm audit` or `snyk`.

2. **Install and configure scanners.** Add security tools as development dependencies. For Python:

   ```bash
   pip install bandit safety pip-audit
   ```

   Create configuration files (`.bandit`, etc.) to customise rules and exclude irrelevant directories (e.g., tests, build outputs).

3. **Run static analysis on code.** Execute Bandit on the application code:

   ```bash
   bandit -r src -f json -o bandit-report.json
   ```

   Review the report and categorise findings by severity. For high‑severity issues (e.g., use of `eval`, insecure random), create tasks to address them immediately.

4. **Scan dependencies for known vulnerabilities.** Use Safety or pip‑audit to check your `requirements.txt` or `pyproject.lock`:

   ```bash
   pip-audit -r requirements.txt
   safety check --full-report
   ```

   For Node projects, run `npm audit --production` or integrate Snyk. Update vulnerable dependencies or apply patches.

5. **Integrate security checks into CI/CD.** Add a step in your pipeline to run these scans automatically. Configure the build to fail on high‑severity vulnerabilities and warn on medium. Publish scan reports as artefacts for review.

6. **Handle false positives and exceptions.** Not all reported issues are exploitable. Investigate each finding; if it’s a false positive or an acceptable risk, document why and suppress the warning in the config file. Regularly update the vulnerability database to reduce false negatives.

7. **Pain Points:**

   - **False positives** can cause alert fatigue. Review findings manually and tune tool configurations.
   - **Out‑of‑date vulnerability databases** may miss recent issues. Schedule periodic updates of the tools and their advisory databases.
   - **Ignoring warnings** can lead to real vulnerabilities. Establish a policy to track and remediate security findings within a reasonable timeframe.