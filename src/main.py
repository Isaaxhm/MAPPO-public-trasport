# Import the GPU module to check tensor operations
from utils.gpu.gpu import check_tensor_operations
from utils.csv.process_gtfs import load_gtfs_data, process_routes, save_route_summaries

def main():
    """
    Main function to execute GPU-related operations.
    """
    # Call the GPU check function
    device = check_tensor_operations()
    print(f"Main function executed on device: {device}")

def process_csv():
    """
    Main function to load GTFS data, process routes, and save the results.
    """

    GTFS_DIR = "data/gtfs/CDMX"  # Change this to your GTFS directory path
    OUTPUT_DIR = "data/processed"

    # Load GTFS data
    data = load_gtfs_data(GTFS_DIR)

    # Process routes
    df_routes = process_routes(data)
    print(df_routes.head())
    # Save route summaries
    #save_route_summaries(df_routes, OUTPUT_DIR)
    
if __name__ == "__main__": 
    main()
    process_csv()
