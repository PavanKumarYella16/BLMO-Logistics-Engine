import pandas as pd
import os
import config
import matplotlib.pyplot as plt
# 1. Import your brand new Database Manager class
from database_manager import LogisticsDBManager

def load_data(filename):
    """Extraction: Reads CSV from the data folder."""
    path = os.path.join('data', filename)
    return pd.read_csv(path)

def validate_data(df):
    """Quality Control: Removes negative weights or missing destinations."""
    df = df[df['weight'] >= 0]
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
        
    # =====================================================================
        # 🗄️ STEP 5: LIVE DATABASE STREAMING DEMO (POSTGRESQL)
        # =====================================================================
        print("\n[STEP 4] Database Integration: Connecting to PostgreSQL...")
        
        # Set up PostgreSQL connection parameters dynamically using your config file
        DB_HOST = "localhost"
        DB_USER = "postgres"                
        DB_PASSWORD = config.DB_PASSWORD     # 🔒 Password hidden safely inside config!
        DB_DATABASE = "thesis_demo_db"    
        
        db = LogisticsDBManager(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE)
        db.connect()
        
        if db.connection:
            # Automatically build/verify the Phase 2 schema tables and dummy parent rows
            db.initialize_schema()
            
            print("\n🔄 Streaming optimized dataframe records into PostgreSQL...")
            
            # Loop through your actual processed pandas dataframe rows!
            for index, row in full_df.iterrows():
                # Convert categorical 'High' / 'Standard' into system integers
                priority_val = 1 if row['priority'] == 'High' else 2
                
                # Simulated assignment IDs for this data pipeline loop
                simulated_driver_id = 1
                simulated_destination_id = index + 1  
                
                # Pass each record cleanly through our database guardrail check
                db.verify_and_insert_order(
                    weight=float(row['weight']),
                    priority=priority_val,
                    driver_id=simulated_driver_id,
                    dest_id=simulated_destination_id
                )
                
            db.close_connection()
            print("\n🏁 Pipeline execution complete. Data stream closed cleanly.")
        else:
            print("❌ Database connection failed. Skipping data stream.")
            
    except FileNotFoundError:
        print("Critical Error: 'shipments.csv' missing from the 'data' folder.")
    except Exception as e:
        print(f"Pipeline Error: {e}")

if __name__ == "__main__":
    main()