import argparse
import os
import re
import shutil
import logging

# Set up logging
logging.basicConfig(filename="parse_log.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def parse_all_stats(log_file, location, run_id):
    try:
        results = []
        pattern = r"(\w+)\s*=\s*([^\n]+)"

        with open(log_file, "r") as file:
            content = file.read()
            results = re.findall(pattern, content)

        logging.info(f"Number of results parsed: {len(results)}")

        # No need to create fermi_stat.txt separately; it's assumed to exist already
        logging.info(f"Parsing completed successfully for location: {location}, run ID: {run_id}.")
    except Exception as e:
        logging.error(f"Error occurred while parsing the file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Parse log file and handle qor directory.")
    parser.add_argument("-l", type=str, required=True, help="Location of the run")
    parser.add_argument("-id", type=str, required=True, help="ID of the run")
    parser.add_argument("-p", action="store_true", help="Parse the file and generate stats")
    parser.add_argument("-r", action="store_true", help="Create rsync folder with qor copied")

    args = parser.parse_args()

    # Paths
    existing_qor_path = os.path.expanduser("~/Documents/PROJECT/9871/qor")

    if args.r:
        # Create the new folder named <run_id>_r in ~/Documents/PROJECT
        run_id_folder = f"{args.id}_r"
        run_dir = os.path.join(os.path.expanduser("~/Documents/PROJECT"), run_id_folder)
        
        # Create the run ID directory and copy the existing qor folder into it
        os.makedirs(run_dir, exist_ok=True)
        qor_directory = os.path.join(run_dir, "qor")
        shutil.copytree(existing_qor_path, qor_directory, dirs_exist_ok=True)

        logging.info(f"Copied qor folder to {qor_directory} for run ID: {args.id}")

    if args.p:
        # Specify the full path to the dummy_logfile.txt
        dummy_logfile_path = os.path.expanduser("~/Documents/PROJECT/9871/logs/optimization/dummy_logfile.txt")
        parse_all_stats(dummy_logfile_path, args.l, args.id)

    # Log the completion of file parsing or directory creation
    if args.r:
        logging.info(f"Directory structure created at {run_dir} with qor folder copied.")
    else:
        logging.info("File parsing completed successfully.")

if __name__ == "__main__":
    main()
