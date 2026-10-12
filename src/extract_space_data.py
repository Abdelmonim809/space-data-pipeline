import json
import logging
from datetime import datetime
from azure.storage.blob import BlobServiceClient

def run_extraction(connection_string, container_name):
    logging.info("🚀 PHASE 1: Initializing synthetic data ingestion pipeline...")
    
    mock_data = {
        "status": "success",
        "market": "crypto_spot",
        "ingested_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        "transactions": [
            {"asset": "BTC", "price_usd": 64250.50, "volume_24h": 28450120},
            {"asset": "ETH", "price_usd": 3450.25, "volume_24h": 14200780},
            {"asset": "SOL", "price_usd": 145.80, "volume_24h": 8900450}
        ]
    }

    try:
        date_str = datetime.utcnow().strftime('%Y-%m-%d')
        filename = f"raw_crypto_{date_str}.json"
        
        logging.info("☁️ Establishing secure socket link with local Azure Cloud Storage (Azurite)...")
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            logging.info(f"📁 Infrastructure Bucket '{container_name}' missing. Executing auto-provisioning routine...")
            container_client.create_container()
        
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        blob_client.upload_blob(json.dumps(mock_data), overwrite=True)
        
        logging.info(f"✅ PHASE 1 SUCCESS: Telemetry array successfully streamed to blob target: {filename}")
        return True
            
    except Exception as e:
        logging.error(f"❌ PHASE 1 FATAL: Data migration payload rejected by Azure storage stack: {e}")
        return False
