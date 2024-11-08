import os
import shutil
import logging
import argparse



# Set up logging to write to a file
logging.basicConfig(
    filename='/home/emumba/Documents/PROJECT/parse.log',  # Log file path
    level=logging.INFO,  # Log level (INFO will log info, warnings, errors, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)
# Function to parse and organize stats
def organize_stats(template_file, data_file, output_file):
    # Read the template file to extract category structure
    with open(template_file, 'r') as template:
        template_lines = template.readlines()
    
    # Read the random data file to get the unordered stats
    with open(data_file, 'r') as data:
        data_lines = data.readlines()
    
    # Initialize variable to hold the organized data
    organized_data = ""
    current_category = ""
    
    for line in template_lines:
        stripped_line = line.strip()
        
        # Check if the line is a category header (e.g., "[Main_Stats]")
        if stripped_line.startswith("[") and stripped_line.endswith("]"):
            current_category = stripped_line
            organized_data += f"{current_category}\n"
        # Check if the line is a field line (e.g., "speed:")
        elif stripped_line:
            field_name = stripped_line.split(":")[0].strip()
            # Find matching field in the random data file
            matched = False
            for data_line in data_lines:
                if data_line.startswith(field_name):
                    organized_data += data_line
                    matched = True
                    break
            # If the field name is not found in the data, add an empty line 
            if not matched:
                organized_data += f"{field_name}: None\n"
        else:
            organized_data += "\n"
    
    # Write the organized data to the output file
    with open(output_file, 'w') as output:
        output.write(organized_data)

def main():
    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Parse command-line arguments
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
    
    # Specify the template file path and output file path
    template_file = '/home/emumba/Documents/PROJECT/9871/qor/Fermi_stats.txt'
    output_file = f"/home/emumba/Documents/PROJECT/9871/qor/organized_stats_{args.id}.txt"  # Output file with run_id

    # Call the function to parse and organize stats
    organize_stats(template_file, dummy_logfile_path, output_file)

    # Log the completion of file parsing or directory creation
    if args.r:
        logging.info(f"Directory structure created at {run_dir} with qor folder copied.")
    else:
        logging.info("File parsing completed successfully.")

if __name__ == "__main__":
    main()
