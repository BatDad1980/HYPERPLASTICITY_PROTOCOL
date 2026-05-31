from aegis_api import AegisAPI

def run_retail_demo():
    print("==================================================")
    print("PROJECT AEGIS: COMMERCIAL RETAIL HEAT-MAPPING DEMO")
    print("==================================================")
    print("Scenario: A buyer installs Aegis in a grocery store to track foot traffic.")
    print("Requirement: Absolute privacy. No faces or identifiable video recorded.\n")
    
    # Buyer initializes the API on a camera pointing at Aisle 4
    api = AegisAPI(camera_id="STORE_7_AISLE_4")
    
    # Start the stream (simulating 5 seconds of footage)
    api.stream_data(duration_seconds=5)
    
if __name__ == "__main__":
    run_retail_demo()
