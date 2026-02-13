# datadesc

Title: Describe Data (/data_desc)

Description: Produces a structured description of the dataset used in the project, detailing schema, types, summary statistics and quality checks to support data‑driven development.

Steps:

1. **Load the dataset.** Use pandas or a relevant library to load the data into memory. For large datasets, sample a representative subset to explore.

2. **Document schema.** For each column, record its name, data type (integer, float, string, datetime, category, etc.), and semantic meaning. Note units and expected ranges where applicable. Identify primary keys and relationships.

3. **Compute summary statistics.** Calculate counts, unique values, mean, median, minimum, maximum and standard deviation for numeric columns. For categorical columns, list categories and their counts. Present results in a concise table or chart if helpful.

4. **Assess data quality.** Identify missing values, duplicate rows, outliers and inconsistent formats (e.g., date strings with different formats or time zones). Create a report summarising these issues.

5. **Identify sensitive data.** Look for personally identifiable information (PII) such as names, emails or phone numbers. Recommend anonymisation or pseudonymisation if required by privacy laws.

6. **Suggest cleaning steps.** Based on the quality assessment, propose actions such as imputing missing values, removing or correcting outliers, standardising formats and normalising values. Document these suggestions for the data cleaning workflow.

7. **Pain points:** Large, messy datasets may hide quality issues. Use automated profiling tools (e.g., `pandas-profiling`) to discover anomalies. Always confirm the meaning of columns with domain experts to avoid misinterpretation.