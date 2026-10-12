import json
import hashlib
from datetime import datetime
from azure.storage.blob import BlobServiceClient

def generate_id(text_string):
    """Generates a reliable, unique integer ID from text using hashing"""
    return int(hashlib.md5(text_string.encode('utf-8')).hexdigest(), 16) % (10**8)

# Accepting connection details straight from main.py, bypassing local folder hunting entirely
def run_transformation(connection_string, container_name):
    print("🧹 Step 2: Starting advanced relational data modeling (Star Schema)...")
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    raw_blob_name = f"raw_crypto_{date_str}.json"
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=raw_blob_name)
        
        print(f"☁️ Downloading {raw_blob_name} from Azure Cloud...")
        blob_data = blob_client.download_blob().readall()
        payload = json.loads(blob_data)
        
        transactions_list = payload.get('transactions', [])
        ingestion_time_str = payload.get('ingested_at')
        
        # --- 1. POPULATE DIM_CALENDAR ---
        date_id = generate_id(date_str)
        dim_calendar_rows = [
            "date_id,full_date,year,month,day",
            f"{date_id},{date_str},{date_str[:4]},{date_str[5:7]},{date_str[8:10]}"
        ]
        
        # --- 2. POPULATE DIM_ASSETS & FACT_MARKET_SNAPSHOT ---
        dim_assets_rows = ["asset_id,asset_ticker,asset_name"]
        fact_snapshot_rows = ["snapshot_id,asset_id,date_id,price_usd,volume_24h,ingested_at"]
        
        asset_names = {"BTC": "Bitcoin", "ETH": "Ethereum", "SOL": "Solana"}
        
        for i, tx in enumerate(transactions_list):
            ticker = tx.get('asset')
            price = tx.get('price_usd')
            volume = tx.get('volume_24h')
            
            asset_id = generate_id(ticker)
            snapshot_id = generate_id(f"{ticker}_{date_str}_{i}")
            full_name = asset_names.get(ticker, "Unknown Asset")
            
            dim_assets_rows.append(f"{asset_id},\"{ticker}\",\"{full_name}\"")
            fact_snapshot_rows.append(f"{snapshot_id},{asset_id},{date_id},{price},{volume},\"{ingestion_time_str}\"")
            
        # --- 3. SAVE THE NORMALIZED STAR SCHEMA TABLES ---
        with open(f"data/dim_calendar.csv", 'w') as f:
            f.write("\n".join(dim_calendar_rows))
        with open(f"data/dim_assets.csv", 'w') as f:
            f.write("\n".join(dim_assets_rows))
        with open(f"data/fact_market_snapshot.csv", 'w') as f:
            f.write("\n".join(fact_snapshot_rows))
            
        print("✅ Step 2 Success: Relational Star Schema successfully generated in /data folder!")
        return True
        
    except Exception as e:
        print(f"❌ Step 2 Failed: Unable to transform cloud data: {e}")
        return False
