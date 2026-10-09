from src.extract_space_data import run_extraction
from src.transform_space_data import run_transformation

def main():
    print("--- STARTING DATA PIPELINE RUN ---")
    extraction_success = run_extraction()
    
    if extraction_success:
        transformation_success = run_transformation()
        if transformation_success:
            print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        else:
            print("🚨 Pipeline failed during transformation.")
    else:
        print("🛑 Pipeline stopped immediately because extraction failed.")

if __name__ == "__main__":
    main()
