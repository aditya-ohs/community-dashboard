import pandas as pd
import numpy as np
import datetime
import os

def generate_v2_dataset():
    """
    V2 ETL Pipeline: Simulates complex, multi-dimensional demographic 
    and economic data for the Portugal Brain Drain Atlas.
    """
    print(f"[{datetime.datetime.now()}] Initiating V2 data pull and transformation...")
    
    years = [2020, 2021, 2022, 2023, 2024]
    sectors = ["Engineering/IT", "Healthcare", "Education/Research", "Business/Finance"]
    destinations = ["UK", "Germany", "France", "Netherlands", "Switzerland"]
    age_groups = ["18-24", "25-34", "35-44"]
    genders = ["Male", "Female", "Non-Binary"]
    
    records = []
    
    # Generate realistic variance for the dataset
    for y in years:
        for s in sectors:
            for a in age_groups:
                for g in genders:
                    # Outward Migration (Brain Drain)
                    out_volume = int(np.random.normal(loc=1500 if s == "Engineering/IT" else 800, scale=200))
                    dest = np.random.choice(destinations)
                    pt_salary_out = np.random.normal(loc=19000, scale=2000)
                    eu_salary_dest = pt_salary_out * np.random.uniform(1.8, 3.5)
                    
                    # Inward Migration (Replacement)
                    in_volume = int(out_volume * np.random.uniform(0.4, 1.2)) # How many come in to replace
                    pt_salary_in = pt_salary_out * np.random.uniform(0.6, 0.9) # Inward migrants often accept lower wages
                    
                    # Tax Impact Calculation (Simplified 28% avg income tax bracket logic)
                    lost_tax_revenue = out_volume * pt_salary_out * 0.28
                    
                    records.append({
                        "Year": y,
                        "Sector": s,
                        "Age_Group": a,
                        "Gender": g,
                        "Destination_Country": dest,
                        "Outward_Emigrants": max(50, out_volume),
                        "Inward_Immigrants": max(10, in_volume),
                        "Avg_Salary_PT_EUR": round(pt_salary_out, 2),
                        "Avg_Salary_EU_EUR": round(eu_salary_dest, 2),
                        "Avg_Salary_Inward_Migrant_EUR": round(pt_salary_in, 2),
                        "Lost_Tax_Revenue_EUR": round(lost_tax_revenue, 2)
                    })

    df = pd.DataFrame(records)
    
    # Feature Engineering: Calculate the "Net Skill Deficit"
    df["Net_Migration"] = df["Inward_Immigrants"] - df["Outward_Emigrants"]
    
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/emigration_trends.csv", index=False)
    print("V2 ETL Pipeline completed successfully.")

if __name__ == "__main__":
    generate_v2_dataset()
