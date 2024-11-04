import argparse
import os
import re
import logging

# Set up logging
logging.basicConfig(filename="parse_log.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def parse_all_stats(log_file, output_file, location, run_id):
    try:
        # Dictionary to store parsed results
        results = []

        # Regular expression to capture all lines with key=value format
        pattern = r"(\w+)\s*=\s*([^\n]+)"

        # Read and parse the log file
        with open(log_file, "r") as file:
            content = file.read()
            results = re.findall(pattern, content)

        # Write parsed results to the output file
        with open(output_file, "w") as out_file:
            out_file.write(f"Location: {location}\n")
            out_file.write(f"Run ID: {run_id}\n\n")
            for key, value in results:
                out_file.write(f"{key}: {value}\n")

        logging.info(f"Parsing completed successfully for location: {location}, run ID: {run_id}.")
    except Exception as e:
        logging.error(f"Error occurred while parsing the file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Parse log file and generate fermi_stat.txt with all stats.")
    parser.add_argument("-l", type=str, required=True, help="Location of the run")
    parser.add_argument("-id", type=str, required=True, help="ID of the run")
    parser.add_argument("-p", action="store_true", required=True, help="Parse the file and create fermi_stat.txt")
    parser.add_argument("-r", type=str, help="Optional base directory to create the run ID folder")

    args = parser.parse_args()

    # Set base directory to the specified path or to the current directory if not provided
    base_dir = args.r if args.r else "."
    run_dir = os.path.join(base_dir, args.id)
    qor_directory = os.path.join(run_dir, "QOR")
    os.makedirs(qor_directory, exist_ok=True)

    # Define the output file path within the QOR folder
    output_file = os.path.join(qor_directory, "fermi_stat.txt")

    if args.p:
        # Specify the full path to the dummy_logfile.txt
        dummy_logfile_path = os.path.expanduser("~/Documents/PROJECT/9871/logs/optimization/dummy_logfile.txt")
        parse_all_stats(dummy_logfile_path, output_file, args.l, args.id)

    # Log the completion of folder creation and file parsing
    logging.info(f"Directory structure created at {run_dir}. QOR folder and fermi_stat.txt file placed successfully.")

if __name__ == "__main__":
    main()
