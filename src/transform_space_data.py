import json
import os
from datetime import datetime

def run_transformation():
    print("🧹 Step 2: Starting data transformation...")
    
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    raw_filename = f"data/raw_astros_{date_str}.json"
    clean_filename = f"data/clean_astros_{date_str}.csv"
    
    if os.path.exists(raw_filename):
        with open(raw_filename, 'r') as f:
            payload = json.load(f)
            
        raw_people_list = payload.get('people', [])
        ingestion_time = payload.get('ingested_at')
        
        csv_rows = ["astronaut_name,spacecraft_name,pipeline_run_date"]
        for person in raw_people_list:
            name = person.get('name')
            craft = person.get('craft')
            csv_rows.append(f'"{name}","{craft}","{ingestion_time}"')
            
        with open(clean_filename, 'w') as f:
            f.write("\n".join(csv_rows))
            
        print(f"✅ Step 2 Success: Transformed data saved to {clean_filename}")
        return True
    else:
        print("❌ Step 2 Failed: Raw data file not found!")
        return False
