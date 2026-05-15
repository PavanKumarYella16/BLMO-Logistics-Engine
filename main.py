import pandas as pd
import os
import config
import matplotlib.pyplot as plt

def load_data(filename):
    """Extraction: Reads CSV from the data folder."""
    path = os.path.join('data', filename)
    return pd.read_csv(path)

def validate_data(df):
    """Quality Control: Removes negative weights or missing destinations."""
    # Ensure weight is a positive number
    df = df[df['weight'] >= 0]
    # Remove rows where crucial info is missing
    df = df.dropna(subset=['destination', 'weight'])
    print("\n[STEP 1] Validation: Data quality check complete.")
    return df

def transform_logistics_data(df):
    """Transformation: Adds business logic (Priority Labels)."""
    df['priority'] = df['weight'].apply(lambda x: 'High' if x > 500 else 'Standard')
    heavy = df[df['weight'] > 400]
    print("[STEP 2] Transformation: Priority logic applied.")
    return df, heavy

def calculate_kpis(df):
    """Analysis: Generates summary statistics."""
    stats = {
        'Total Shipments': len(df),
        'Average Weight': round(df['weight'].mean(), 2),
        'Max Weight': df['weight'].max(),
        'Total High Priority': len(df[df['priority'] == 'High'])
    }
    return stats

def create_visuals(df):
    """Reporting: Generates a professional bar chart."""
    plt.figure(figsize=(10, 6))
    plt.bar(df['destination'], df['weight'], color='skyblue', edgecolor='navy')
    plt.xlabel('Destination City')
    plt.ylabel('Weight (kg)')
    plt.title('Thesis Project: Shipment Weights by Destination')
    
    plt.savefig('shipment_chart.png')
    print("[STEP 3] Visualization: 'shipment_chart.png' updated.")

def main():
    print(f"--- Starting Thesis Project Pipeline | User: {config.DB_USER} ---")
    
    try:
        # 1. Ingestion & Validation
        raw_data = load_data('shipments.csv')
        clean_data = validate_data(raw_data)
        
        # 2. Transformation
        full_df, heavy_df = transform_logistics_data(clean_data)
        
        # 3. Analysis & Visualization
        metrics = calculate_kpis(full_df)
        create_visuals(full_df)
        
        # 4. Display Summary
        print("\n--- Logistics KPI Report ---")
        for k, v in metrics.items():
            print(f"{k}: {v}")

        print("\n--- Processed Data Preview ---")
        print(full_df)
        
    except FileNotFoundError:
        print("Critical Error: 'shipments.csv' missing from the 'data' folder.")
    except Exception as e:
        print(f"Pipeline Error: {e}")

if __name__ == "__main__":
    main()