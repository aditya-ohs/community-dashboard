import pandas as pd

# Let's engineer a clean tracking dataset for the dashboard
data = {
    "Year": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] * 4,
    "Sector": ["IT/Engineering"]*8 + ["Healthcare"]*8 + ["Research/Academia"]*8 + ["Business/Finance"]*8,
    "Emigrants": [3200, 3400, 2900, 3100, 4200, 4800, 5100, 5500,  # IT
                  1800, 1900, 2100, 2400, 2800, 3100, 3300, 3600,  # Health
                  1200, 1100, 950,  1050, 1400, 1600, 1750, 1900,  # Research
                  2500, 2700, 2200, 2400, 2900, 3200, 3400, 3700], # Business
    "Primary_Destination": ["UK"]*8 + ["Germany"]*8 + ["France"]*8 + ["Netherlands"]*8,
    "Avg_Salary_Multiplier": [3.2, 3.3, 3.4, 3.5, 3.8, 4.0, 4.1, 4.2] * 4
}

df = pd.DataFrame(data)
df.to_csv("data/emigration_trends.csv", index=False)
print("Data pipeline executed successfully: data/emigration_trends.csv created.")
