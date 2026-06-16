import pandas as pd
import datetime
import os

def fetch_and_transform_data():
    """
    Simulates an ETL pipeline fetching real-world macroeconomic data.
    In a full production environment, this would hit the OECD SDMX API.
    """
    print(f"[{datetime.datetime.now()}] Initiating data pull...")
    
    # Simulating real-world formatted data combining Portugal metrics with OECD averages
    data = {
        "Year": [2020, 2021, 2022, 2023, 2024] * 3,
        "Sector": ["Engineering/IT"]*5 + ["Healthcare"]*5 + ["Education/Research"]*5,
        "PT_Emigrants": [3200, 3100, 4200, 4800, 5200, 1800, 2100, 2800, 3100, 3400, 950, 1050, 1400, 1600, 1800],
        "PT_Avg_Salary_EUR": [18000, 18500, 19000, 19500, 20000, 16000, 16500, 17000, 17500, 18000, 14000, 14200, 14500, 15000, 15500],
        "OECD_Avg_Salary_EUR": [45000, 46000, 48000, 50000, 52000, 40000, 41000, 44000, 46000, 48000, 35000, 36000, 38000, 40000, 42000],
        "Primary_Destination": ["UK"]*5 + ["Germany"]*5 + ["France"]*5
    }
    
    df = pd.DataFrame(data)
    
    # Transformation: Calculate the Salary Deficit (Policy Indicator)
    df["Salary_Deficit_vs_OECD_Percent"] = ((df["OECD_Avg_Salary_EUR"] - df["PT_Avg_Salary_EUR"]) / df["OECD_Avg_Salary_EUR"]) * 100
    df["Salary_Deficit_vs_OECD_Percent"] = df["Salary_Deficit_vs_OECD_Percent"].round(1)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Load to CSV
    df.to_csv("data/emigration_trends.csv", index=False)
    print("ETL Pipeline completed. Data saved to data/emigration_trends.csv")

if __name__ == "__main__":
    fetch_and_transform_data()