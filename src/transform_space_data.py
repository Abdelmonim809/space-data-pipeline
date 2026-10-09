import json
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient

def run_transformation():
    print("🧹 Step 2: Starting cloud data transformation...")
    
    # FIX: Changed '127.0.0.1' to 'localhost' to match the updated extractor
    CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://localhost:10000/devstoreaccount1;"
    CONTAINER_NAME = "raw-crypto-data"
    
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    raw_blob_name = f"raw_crypto_{date_str}.json"
    clean_local_filename = f"data/clean_crypto_market_{date_str}.csv"
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=raw_blob_name)
        
        print(f"☁️ Downloading {raw_blob_name} from Azure Cloud...")
        blob_data = blob_client.download_blob().readall()
        payload = json.loads(blob_data)
        
        transactions_list = payload.get('transactions', [])
        ingestion_time = payload.get('ingested_at')
        
        csv_rows = ["crypto_asset,price_usd,volume_24h,pipeline_run_date"]
        for tx in transactions_list:
            asset = tx.get('asset')
            price = tx.get('price_usd')
            volume = tx.get('volume_24h')
            csv_rows.append(f'"{asset}",{price},{volume},"{ingestion_time}"')
            
        with open(clean_local_filename, 'w') as f:
            f.write("\n".join(csv_rows))
            
        print(f"✅ Step 2 Success: Transformed data saved locally to: {clean_local_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Step 2 Failed: Unable to transform cloud data: {e}")
        return False
