import json
import requests
from datetime import datetime

def run_extraction():
    API_URL = "http://api.open-notify.org/astros.json"
    print("🚀 Step 1: Fetching live astronaut data from API...")
    
    try:
        response = requests.get(API_URL, timeout=10) # Added a timeout so it doesn't hang forever
        
        if response.status_code == 200:
            # Safely attempt to parse the JSON data
            raw_data = response.json()
            
            raw_data['ingested_at'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            date_str = datetime.utcnow().strftime('%Y-%m-%d')
            filename = f"data/raw_astros_{date_str}.json"
            
            with open(filename, 'w') as f:
                json.dump(raw_data, f, indent=4)
                
            print(f"✅ Step 1 Success: Raw data saved to {filename}")
            return True
        else:
            print(f"❌ Step 1 Failed: Server returned bad status code {response.status_code}")
            return False
            
    # If the JSON is broken or empty, catch the error here instead of crashing!
    except requests.exceptions.JSONDecodeError:
        print("❌ Step 1 Failed: The API server returned an empty or broken response. It might be down.")
        return False
    except Exception as e:
        print(f"❌ Step 1 Failed: A network error occurred: {e}")
        return False
