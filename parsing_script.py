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
        # Define the patterns for extracting relevant stats and sections
        patterns = {
            "Main_Stats": r"fermi_job_id = 9871[\s\S]*?parsing_time = False",
            "Runtime_Analysis_Stats": r"target_prep_runtime = None[\s\S]*?the_checker_runtime = None",
            "Geometric_Analysis_Stats_Fermi": r"the_checker_runtime = None[\s\S]*?marker_y_fermi = \d+(\.\d+)?",
            "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Negfocus": r"design_size = \d+(\.\d+)? x \d+(\.\d+)?[\s\S]*?run_date_time = \d+-\d+-\d+ \d+:\d+:\d+",
            "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Negdose": r"mean_fermi = \d+(\.\d+)?[\s\S]*?marker_y_fermi = \d+(\.\d+)?",
            "Statistical_Analysis:EPE_Target_vs_Nominal_Mask_Simulation_f0d0": r"high_curvature_internal_checking_count = \d+[\s\S]*?xor_error_of_positive_defocus_greater_than_15_marker_y = \d+",
            "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Posfocus": r"mean_fermi = -?\d+(\.\d+)?[\s\S]*?marker_y_fermi = \d+(\.\d+)?",
            "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Posdose": r"mrc_area_count = \d+[\s\S]*?high_curvature_external_checking_marker_y = \d+",
            "Statistical_Analysis:Width_of_PV_Band_by_Dose": r"mean_fermi = -?\d+(\.\d+)?[\s\S]*?target_file_size = \d+(\.\d+)?",
            "Statistical_Analysis:Width_of_PV_Band_by_Focus": r"machine_name = \w+[\s\S]*?marker_y_fermi = \d+(\.\d+)?"
        }

        # Open the log file
        with open(log_file, "r") as file:
            content = file.read()

        results = []

        for section, pattern in patterns.items():
            # Find the section using the defined pattern
            section_data = re.search(pattern, content)

            if section_data:
                # Extract and process the key-value pairs in the section
                section_content = section_data.group(0)
                lines = section_content.strip().splitlines()

                # Start writing the section header
                results.append(f"[{section}]")
                
                # Process each line as a key-value pair
                for line in lines:
                    if "=" in line:
                        results.append(line.strip())

                results.append("")  # Add a blank line between sections

        # Write the results to fermi_stat.txt
        fermi_stat_path = "/home/emumba/Documents/PROJECT/9871/qor/fermi_stat.txt"
        with open(fermi_stat_path, "w") as fermi_file:
            for line in results:
                fermi_file.write(line + "\n")

        logging.info(f"Parsed and saved statistics to {fermi_stat_path} for location: {location}, run ID: {run_id}.")
    
    except Exception as e:
        logging.error(f"Error occurred while parsing the file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Parse log file and handle qor directory.")
    parser.add_argument("-l", type=str, required=True, help="Location of the run")
    parser.add_argument("-id", type=str, required=True, help="ID of the run")
    parser.add_argument("-p", type=str, required=True, help="Parse the file and generate stats (mandatory)")
    parser.add_argument("-r", action="store_true", help="Create rsync folder with qor copied")

    args = parser.parse_args()

    # Paths
    existing_qor_path = "/home/emumba/Documents/PROJECT/9871/qor"

    if args.r:
        # Create the new folder named <run_id>_r in ~/Documents/PROJECT
        run_id_folder = f"{args.id}_r"
        run_dir = os.path.join("/home/emumba/Documents/PROJECT", run_id_folder)
        
        # Create the run ID directory and copy the existing qor folder into it
        os.makedirs(run_dir, exist_ok=True)
        qor_directory = os.path.join(run_dir, "qor")
        shutil.copytree(existing_qor_path, qor_directory, dirs_exist_ok=True)

        logging.info(f"Copied qor folder to {qor_directory} for run ID: {args.id}")

    # Specify the full path to the dummy_logfile.txt
    dummy_logfile_path = "/home/emumba/Documents/PROJECT/9871/logs/optimization/dummy_logfile.txt"
    parse_all_stats(dummy_logfile_path, args.l, args.id)

    # Log the completion of file parsing or directory creation
    if args.r:
        logging.info(f"Directory structure created at {run_dir} with qor folder copied.")
    else:
        logging.info("File parsing completed successfully.")

if __name__ == "__main__":
    main()
