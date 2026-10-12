import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient

# Notice we now pass the variables directly into the function arguments
def run_extraction(connection_string, container_name):
    print("🚀 Step 1: Generating live production data natively...")
    
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
        
        print("☁️ Streaming data package into local Azure Cloud (Azurite)...")
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
        
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        blob_client.upload_blob(json.dumps(mock_data), overwrite=True)
        
        print(f"✅ Step 1 Success: Data streamed to Azure Blob Storage as: {filename}")
        return True
            
    except Exception as e:
        print(f"❌ Step 1 Failed: An unexpected Azure storage error occurred: {e}")
        return False
