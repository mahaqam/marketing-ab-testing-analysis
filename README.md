# Marketing A/B Testing & Conversion Analysis

Experimentation project using the public **Marketing A/B Testing** dataset. The data compares users shown advertising (`ad`) with a control group shown a public-service announcement (`psa`) and records whether they converted.

## Questions
- What are treatment and control conversion rates?
- What are the absolute and relative observed uplifts?
- Is the difference statistically significant?
- What is the 95% confidence interval for the conversion-rate difference?
- How do observed conversion rates vary by day and hour of highest ad exposure?

## Dataset
Download `marketing_AB.csv` from Kaggle's **Marketing A/B Testing** dataset and save it under `data/raw/`.

Expected fields are `user id`, `test group`, `converted`, `total ads`, `most ads day`, and `most ads hour`.

## Run
```bash
python -m venv .venv
pip install -r requirements.txt
python src/ab_test_analysis.py --input data/raw/marketing_AB.csv
```

The analysis generates group summaries, a two-proportion z-test, absolute/relative uplift, a 95% confidence interval, day/hour segment summaries and a conversion chart.

## SQL
`sql/ab_test_analysis.sql` provides reusable group, day and hour conversion queries.

## Interpretation
Statistical significance is evaluated alongside effect size and uncertainty. The repository intentionally does not invent revenue, incentive cost or profitability values that are absent from the source data.
