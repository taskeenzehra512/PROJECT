import argparse
import os
import re
import shutil
import logging

# Set up logging
logging.basicConfig(filename="parse_log.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def format_parsed_data(results):
    formatted_sections = []

    # Define all categories and their start and end keys
    categories = {
        "Main_Stats": {
            "start": "fermi_job_id", "end": "parsing_time"
        },
        "Runtime_Analysis_Stats": {
            "start": "target_prep_runtime", "end": "the_checker_runtime"
        },
        "Geometric_Analysis_Stats_Fermi": {
            "start": "mean_fermi", "end": "marker_y_fermi"
        },
        "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Negfocus": {
            "start": "design_size", "end": "run_date_time"
        },
        "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Negdose": {
            "start": "mean_fermi", "end": "marker_y_fermi"
        },
        "Statistical_Analysis:EPE_Target_vs_Nominal_Mask_Simulation_f0d0": {
            "start": "high_curvature_internal_checking_count", "end": "xor_error_of_positive_defocus_greater_than_15_marker_y"
        },
        "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Posfocus": {
            "start": "mean_fermi", "end": "marker_y_fermi"
        },
        "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Posdose": {
            "start": "mrc_area_count", "end": "high_curvature_external_checking_marker_y"
        },
        "Statistical_Analysis:Width_of_PV_Band_by_Dose": {
            "start": "mean_fermi", "end": "target_file_size"
        },
        "Statistical_Analysis:Width_of_PV_Band_by_Focus": {
            "start": "machine_name", "end": "marker_y_fermi"
        }
    }

    # Loop through each category and find matching key-value pairs between start and end
    for section, bounds in categories.items():
        start_key, end_key = bounds["start"], bounds["end"]
        section_data = {}

        # Find the index of start and end keys in the parsed results
        start_index = None
        end_index = None
        for i, (key, value) in enumerate(results):
            if key == start_key:
                start_index = i
            if key == end_key:
                end_index = i

        # If we found both start and end, extract the relevant section
        if start_index is not None and end_index is not None:
            section_data = dict(results[start_index:end_index + 1])
            formatted_section = f"[{section}]"
            for key, value in section_data.items():
                formatted_section += f"\n{key} = {value}"

            formatted_sections.append(formatted_section)

    return "\n\n".join(formatted_sections)

def parse_all_stats(log_file, location, run_id):
    try:
        results = []
        pattern = r"(\w+)\s*=\s*([^\n]+)"

        with open(log_file, "r") as file:
            content = file.read()
            results = re.findall(pattern, content)

        # Format the parsed results
        formatted_data = format_parsed_data(results)

        # Write to fermi_stat.txt
        output_file = "/home/emumba/Documents/PROJECT/9871/qor/fermi_stat.txt"
        with open(output_file, "w") as f:
            f.write(formatted_data)

        logging.info(f"Number of results parsed: {len(results)}")
        logging.info(f"Data written to {output_file} successfully for run ID: {run_id}.")
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
