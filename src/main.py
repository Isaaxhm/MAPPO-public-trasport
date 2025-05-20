# Import the GPU module to check tensor operations
from utils.gpu.gpu import check_tensor_operations
from utils.csv.process_gtfs import load_gtfs_data, process_routes, save_route_summaries
import os

def main():
    """
    Main function to execute GPU-related operations.
    """
    # Call the GPU check function
    device = check_tensor_operations()
    print(f"Main function executed on device: {device}")

    def check_data_files(required_files=None):
        """
        Checks if the 'data' directory exists and contains the specified files.
        If required_files is None, checks if the directory is not empty.
        """
        data_dir = "data"
        if not os.path.isdir(data_dir):
            print(f"Directory '{data_dir}' does not exist.")
            return False

        files_in_data = os.listdir(data_dir)
        if required_files is None:
            if not files_in_data:
                print(f"No files found in '{data_dir}'.")
                return False
            print(f"Files found in '{data_dir}': {files_in_data}")
            return True

        missing_files = [f for f in required_files if f not in files_in_data]
        if missing_files:
            print(f"Missing files in '{data_dir}': {missing_files}")
            return False

        print(f"All required files are present in '{data_dir}'.")
        return True


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
