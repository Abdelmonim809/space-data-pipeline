import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from src.extract_space_data import run_extraction
from src.transform_space_data import run_transformation

# 1. CONFIGURE THE CENTRAL PRODUCTION LOGGING ENGINE
logging.basicConfig(
    level=logging.INFO, # Capture INFO, WARNING, and ERROR logs
    format='%(asctime)s [%(levelname)s] %(message)s', # Format: YYYY-MM-DD HH:MM:SS [LEVEL] Message
    handlers=[
        logging.FileHandler("pipeline.log"), # Writes the logging journal to this physical file
        logging.StreamHandler() # Simulates print() by also showing the output in your VS Code terminal
    ]
)

def main():
    logging.info("=========================================")
    logging.info("🤖 SYSTEM: STARTING DATA PIPELINE ORCHESTRATION RUN")
    logging.info("=========================================")
    
    # Load configuration profiles
    load_dotenv()
    connection_string = os.getenv("AZURE_CONNECTION_STRING")
    container_name = os.getenv("CRYPTO_CONTAINER_NAME")
    
    if not connection_string or not container_name:
        logging.error("🛑 CRITICAL ARCHITECTURE FAILURE: Central orchestrator could not load secure credentials from environment settings!")
        return

    # Execute Ingestion Stage
    extraction_success = run_extraction(connection_string, container_name)
    
    # Execute Transformation Stage based on dependency state
    if extraction_success:
        transformation_success = run_transformation(connection_string, container_name)
        if transformation_success:
            logging.info("🎉 PIPELINE RUN STATUS: COMPLETED SUCCESSFULLY WITH ZERO ERRORS!")
        else:
            logging.error("🚨 PIPELINE RUN STATUS: EXECUTION CRASHED DURING INTERMEDIATE TRANSFORMATION PHASE.")
    else:
        logging.warning("🛑 PIPELINE RUN STATUS: CORE EXTRACTION FAILURE ENCOUNTERED. TRANFORMATION ABORTED TO PRESERVE STAGING INTEGRITY.")

if __name__ == "__main__":
    main()
