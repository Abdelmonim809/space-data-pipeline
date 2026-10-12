import json
import hashlib
import logging
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient

def generate_id(text_string):
    return int(hashlib.md5(text_string.encode('utf-8')).hexdigest(), 16) % (10**8)

def write_to_warehouse(file_path, header, rows):
    file_exists = os.path.exists(file_path)
    with open(file_path, 'a') as f:
        if not file_exists:
            f.write(header + "\n")
        f.write("\n".join(rows) + "\n")

def run_transformation(connection_string, container_name):
    logging.info("🧹 PHASE 2: Initializing advanced incremental relational modeling layer...")
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    raw_blob_name = f"raw_crypto_{date_str}.json"
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=raw_blob_name)
        
        logging.info(f"☁️ Pulling target data asset '{raw_blob_name}' down from Azure Cloud environment...")
        blob_data = blob_client.download_blob().readall()
        payload = json.loads(blob_data)
        
        transactions_list = payload.get('transactions', [])
        ingestion_time_str = payload.get('ingested_at')
        
        # --- 1. MODEL AND APPEND DIM_CALENDAR ---
        date_id = generate_id(date_str)
        calendar_header = "date_id,full_date,year,month,day"
        calendar_rows = [f"{date_id},{date_str},{date_str[:4]},{date_str[5:7]},{date_str[8:10]}"]
        write_to_warehouse("data/dim_calendar.csv", calendar_header, calendar_rows)
        
        # --- 2. MODEL AND APPEND DIM_ASSETS & FACT_MARKET_SNAPSHOT ---
        assets_header = "asset_id,asset_ticker,asset_name"
        snapshot_header = "snapshot_id,asset_id,date_id,price_usd,volume_24h,ingested_at"
        
        assets_rows = []
        snapshot_rows = []
        
        asset_names = {"BTC": "Bitcoin", "ETH": "Ethereum", "SOL": "Solana"}
        
        for i, tx in enumerate(transactions_list):
            ticker = tx.get('asset')
            price = tx.get('price_usd')
            volume = tx.get('volume_24h')
            
            asset_id = generate_id(ticker)
            snapshot_id = generate_id(f"{ticker}_{date_str}_{i}")
            full_name = asset_names.get(ticker, "Unknown Asset")
            
            assets_rows.append(f"{asset_id},\"{ticker}\",\"{full_name}\"")
            snapshot_rows.append(f"{snapshot_id},{asset_id},{date_id},{price},{volume},\"{ingestion_time_str}\"")
            
        write_to_warehouse("data/dim_assets.csv", assets_header, assets_rows)
        write_to_warehouse("data/fact_market_snapshot.csv", snapshot_header, snapshot_rows)
            
        logging.info("✅ PHASE 2 SUCCESS: Relational model normalization complete. Target batch appended.")
        return True
        
    except Exception as e:
        logging.error(f"❌ PHASE 2 FATAL: Computational failure during data parsing routine: {e}")
        return False
