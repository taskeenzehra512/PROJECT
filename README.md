

# Project Overview

This repository includes multiple scripts and applications designed for parsing, organizing, recording data, and integrating with databases and web applications. The repository also supports CI/CD automation and email reporting workflows.

---

## Parsing Script

### Overview
The parsing script performs the following tasks:
- Organizes statistical data based on a predefined template.
- Creates directories and copies necessary files for specific runs.
- Logs all activities for easier debugging.

### Features
1. **Organize Stats**:
   - Reads a template file (e.g., `Fermi_stats.txt`) to define the structure.
   - Fetches unordered stats from a data file (e.g., `dummy_logfile.txt`).
   - Generates an organized stats file (`organized_stats_<run_id>.txt`).

2. **Directory Handling**:
   - Creates a directory structure if the `-r` flag is provided.
   - Copies the `qor` folder to the newly created directory.

3. **Logging**:
   - Logs all actions into `parse.log`.

### Command-line Arguments
| Argument | Type   | Description                                           |
|----------|--------|-------------------------------------------------------|
| `-l`     | String | Location of the run (mandatory).                      |
| `-id`    | String | Run ID (mandatory).                                   |
| `-p`     | String | Specifies parsing of files and stats generation.      |
| `-r`     | Flag   | Creates a directory for rsync and copies the qor folder. |

### Usage

python3 script_name.py -l /home/emumba/Documents/PROJECT -id 9871 -p parse_file -r



# RECORDING SCRIPT

---

## Overview

The **Recording Script** is a Python program designed to parse data from files named `organized_stats` and store the extracted information in a MySQL database. It automates data processing, database integration, and file organization, making it easier to handle and analyze statistical data.

---

## Features

### 1. **Database Connection**
- Establishes a connection to a MySQL database using SQLAlchemy.
- Ensures robust and efficient interaction with the database.

### 2. **Table Definitions**
- Defines multiple database tables to store parsed statistics.
- Each table contains:
  - `id`: Primary key (auto-incremented).
  - `run_id`: ID of the run.
  - `run_name`: Name of the run.
  - `revision_commit`: Commit ID of the revision.
  - `stats_name`: Name of the statistic.
  - `stats_value`: Value of the statistic.

### 3. **File Parsing**
- Reads and processes data files named `organized_stats`.
- Extracts key information including:
  - Run ID
  - Run name
  - Revision commit
  - Stats name
  - Stats value

### 4. **Data Insertion**
- Inserts parsed data into relevant database tables efficiently.

### 5. **Auto-Increment Reset**
- Resets the auto-increment value for the primary key in each table after clearing table data.

### 6. **File Collection**
- Recursively scans a directory to collect paths of all `organized_stats` files.
- Returns a list of file paths and associated run IDs.

---

## Tables in Database

The script uses the following tables to store the parsed data:
- `Main_Stats`
- `Runtime_Analysis_Stats`
- `Geometric_Analysis_Stats_Fermi`
- `Mask_Simulation_Negdose`
- `Mask_Simulation_Negfocus`
- `Mask_Simulation_Posdose`
- `Mask_Simulation_Posfocus`
- `Mask_Simulation_f0d0`
- `Width_of_PV_Band_by_Dose`
- `Width_of_PV_Band_by_Focus`

---

## Functions

### 1. `parse_and_record_data(file_path, run_id, run_name, revision_commit)`
- Reads a `organized_stats` file.
- Parses its content.
- Inserts parsed data into the corresponding database tables.

### 2. `reset_auto_increment()`
- Resets the auto-increment value for the primary key of each table after clearing the table data.

### 3. `collect_organized_stats_files(base_directory)`
- Scans a base directory recursively to find all `organized_stats` files.
- Returns:
  - A list of file paths.
  - Corresponding run IDs.

---

## Usage
pyhton3 r1.py




# Flask Application with SQLAlchemy and MySQL Integration

---

## Overview

This Flask web application allows users to query multiple database tables in a MySQL database using SQLAlchemy. Users can search for data across several statistics-related tables and view the queried results dynamically on the frontend.

---

## Features

- **Dynamic Querying:** Users can input parameters (e.g., `run_id`, `run_name`, `revision_commit`) to query multiple tables in the MySQL database.
- **Real-Time Data Display:** Query results are displayed on the frontend using a dynamic HTML template.
- **SQLAlchemy ORM Integration:** Simplifies database interaction through object-relational mapping.
- **User-Friendly Interface:** A form for users to enter query parameters and view the results in an intuitive manner.

---

## Setup

--**MySQL Database:**
Set up MySQL database with the following credentials:
Username: d2s
Password: D2s_1234!
Database: emumba_qor

The app uses several tables for storing statistics data. These tables should be created in your MySQL database. Models are defined in the app, which automatically maps to these tables.

---

## Database Configuration
The app connects to a MySQL database using SQLAlchemy. The database URI is configured as follows in the script:

Username: d2s
Password: D2s_1234!
Database Name: emumba_qor
Host: localhost

---

## Flask Routes
/ (GET, POST)
GET Request: Displays the initial form where users can input parameters.
POST Request: Executes SQL queries based on the input parameters (run_id, run_name, revision_commit) and displays the matching records.

---

## HTML Template
The app uses an index.html template to render the results dynamically on the frontend. The results are passed as a dictionary to the template, where each key represents a table name, and the corresponding value is the query result.

---

## Example Input Form
Users can input the following parameters in the form:

run_id: ID of the run (optional)
run_name: Name of the run (optional)
revision_commit: Revision commit identifier (optional)

---
## Example Form Submission:
When a user submits the form with parameters, the application:

Queries the database for matching records in each table.
Displays the results in an organized table format

---


# Dockerized Flask Application with SQLAlchemy and MySQL

## Overview

This repository contains a Flask web application that connects to a MySQL database using SQLAlchemy. The application allows users to query multiple database tables based on various parameters and dynamically displays the results. The project is dockerized to simplify deployment and manage dependencies using Docker and Docker Compose.

---

## Project Structure

- **d5_api.py**: Main Flask application file that handles routes and database queries.
- **Dockerfile**: Defines the web service container.
- **docker-compose.yml**: Manages both the web and MySQL database containers.
- **requirements.txt**: Contains the Python dependencies for the application.
- **index.html**: HTML template used to display the results of the database queries.

---

## Build and Run Docker Containers

docker-compose up --build

Build the containers as per the Dockerfile.
Start the web application and MySQL containers.


---

## Access the Application
Once the containers are running, you can access the Flask application by visiting:

http://localhost:5000


---

## User Input Fields
You can enter the following input fields to query the MySQL database:

run_id (Optional): ID of the run.
run_name (Optional): Name of the run.
revision_commit (Optional): Revision commit identifier.
Based on the values entered, the application will query the appropriate tables and return the results dynamically.

---

## Stopping the Containers

docker-compose down
This will stop the containers and remove any associated resources.




# Newman Postman Collection Runner with Email Report

This project automates the process of running a Postman collection using **Newman**, generating an HTML report, and sending the report via email. The process is automated using a **Bash script** to run the Newman tests and a **Python script** to send the HTML report via email after the tests are completed.

---

## Features

- **Run Postman Collection**: Executes a Postman collection with Newman.
- **Generate HTML Report**: Creates an HTML report after the collection run.
- **Email Report**: Sends the generated HTML report via email once the tests are finished.

---

## Setup


- **Node.js** and **Newman** must be installed on your system. 
---



## Usage

### Run the Newman Collection

**Execute the Bash Script**: The script `newman_report.sh` is used to run the Postman collection and generate the report.

.............................................................

------------------------


-------------------------
hiiiiiiiiiiiiiiiiiiii


CI/CD Pipeline Overview:
This document describes the CI/CD pipeline configuration for automating the deployment process of an application. The pipeline is defined in a GitHub Actions workflow and consists of multiple stages: Build and Test, Deploy, and Notify.

Workflow Trigger
The pipeline triggers under the following conditions:

Push events on the master branch.
Pull request events targeting the master branch.
Jobs in the CI/CD Pipeline

Build and Test:
The build_and_test job is responsible for checking out the code, setting up the Python environment, installing dependencies, verifying the Docker Compose installation, and running tests.

Steps:
Checkout code: Retrieves the code from the repository using actions/checkout.
Set up Python: Installs Python version 3.10 using actions/setup-python.
Install dependencies:
Removes existing Docker and related dependencies.
Installs nodejs (via NodeSource), docker.io, and docker-compose if not already installed.
Installs newman globally via npm (for running Postman collections).
Installs Python dependencies from requirements.txt using pip.
Verify Docker Compose installation: Ensures that Docker Compose is installed correctly by checking its version.
Deploy the app with Docker Compose: Runs docker-compose up --build -d to build and start the application in detached mode.
Run tests and send report: Executes the runtest.sh script, which runs Newman to execute API tests and sends a report.

Deploy:
The deploy job runs after the successful completion of the build_and_test job. It redeems the code, ensures Docker Compose is installed, and deploys the application.

Steps:
Checkout code: Retrieves the latest version of the code for deployment.
Install Docker Compose: Ensures Docker Compose is installed if not already present.
Verify Docker Compose: Checks the Docker Compose version.
Deploy the app: Runs docker-compose up --build -d to build and deploy the application.

Notify:
The notify job sends an email notification to a specified email address upon successful deployment.

Steps:
Install mailutils: Installs the mailutils package to allow sending emails.
Send email on success: Sends an email with the subject "CI/CD Pipeline Success" and a success message to taskeen.zehra@emumba.com.
