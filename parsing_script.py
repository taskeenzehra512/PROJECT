import argparse
import os
import re
import logging

# Set up logging
logging.basicConfig(filename="parse_log.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def parse_all_stats(log_file, output_file, location, run_id):
    try:
        results = []
        pattern = r"(\w+)\s*=\s*([^\n]+)"

        with open(log_file, "r") as file:
            content = file.read()
            results = re.findall(pattern, content)

        logging.info(f"Number of results parsed: {len(results)}")

        with open(output_file, "w") as out_file:
            out_file.write(f"Location: {location}\n")
            out_file.write(f"Run ID: {run_id}\n\n")
            for key, value in results:
                out_file.write(f"{key}: {value}\n")

        logging.info("fermi_stat.txt written successfully.")
        logging.info(f"Parsing completed successfully for location: {location}, run ID: {run_id}.")
    except Exception as e:
        logging.error(f"Error occurred while parsing the file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Parse log file and generate fermi_stat.txt with all stats.")
    parser.add_argument("-l", type=str, required=True, help="Location of the run")
    parser.add_argument("-id", type=str, required=True, help="ID of the run")
    parser.add_argument("-p", action="store_true", required=True, help="Parse the file and create fermi_stat.txt")

    args = parser.parse_args()

    # Define the path for fermi_stat.txt inside the existing qor directory
    qor_directory = os.path.expanduser("~/Documents/PROJECT/9871/qor")
    output_file = os.path.join(qor_directory, "fermi_stat.txt")

    if args.p:
        # Specify the full path to the dummy_logfile.txt
        dummy_logfile_path = os.path.expanduser("~/Documents/PROJECT/9871/logs/optimization/dummy_logfile.txt")
        parse_all_stats(dummy_logfile_path, output_file, args.l, args.id)

    # Log the completion of file parsing
    logging.info(f"File parsing completed successfully. fermi_stat.txt created in the existing QOR folder.")

if __name__ == "__main__":
    main()
