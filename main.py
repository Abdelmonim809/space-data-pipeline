import os
from dotenv import load_dotenv
from src.extract_space_data import run_extraction
from src.transform_space_data import run_transformation

def main():
    print("--- STARTING DATA PIPELINE RUN ---")
    
    # 1. The central orchestrator loads the configuration keys once
    load_dotenv()
    connection_string = os.getenv("AZURE_CONNECTION_STRING")
    container_name = os.getenv("CRYPTO_CONTAINER_NAME")
    
    # Defensive programming: Stop immediately if the .env variables are missing
    if not connection_string or not container_name:
        print("🛑 Pipeline stopped: Central orchestrator could not load keys from .env file!")
        return

    # 2. Run the extraction process, passing the configuration keys down into it
    extraction_success = run_extraction(connection_string, container_name)
    
    # 3. Only run transformation if the extraction stage successfully finished
    if extraction_success:
        transformation_success = run_transformation(connection_string, container_name)
        if transformation_success:
            print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        else:
            print("🚨 Pipeline failed during the transformation stage.")
    else:
        print("🛑 Pipeline stopped immediately because extraction failed.")

if __name__ == "__main__":
    main()
