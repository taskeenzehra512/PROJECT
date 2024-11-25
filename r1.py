import os
import re
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, delete, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import random
import string

import logging

# Database connection setup
DATABASE_URI = 'mysql+pymysql://d2s:D2s_1234!@0.0.0.0:3307/emumba_qor'
engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Base class for declarative class definitions
Base = declarative_base()

# Define tables based on headers
class MainStats(Base):
    __tablename__ = 'Main_Stats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False)
    run_name = Column(String(100), nullable=False)  # New column
    revision_commit = Column(String(100), nullable=False)  # New column
    stats_name = Column(String(100), nullable=False)
    stats_value = Column(String(100), nullable=False)

class RuntimeAnalysisStats(Base):
    __tablename__ = 'Runtime_Analysis_Stats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False)
    run_name = Column(String(100), nullable=False)  # New column
    revision_commit = Column(String(100), nullable=False)  # New column
    stats_name = Column(String(100), nullable=False)
    stats_value = Column(String(100), nullable=False)

class GeometricAnalysisStatsFermi(Base):
    __tablename__ = 'Geometric_Analysis_Stats_Fermi'
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False)
    run_name = Column(String(100), nullable=False)  # New column
    revision_commit = Column(String(100), nullable=False)  # New column
    stats_name = Column(String(100), nullable=False)
    stats_value = Column(String(100), nullable=False)

class Statistical_AnalysisEPETargetvsMaskSimulationNegdose(Base):
    __tablename__ = 'Mask_Simulation_Negdose'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique identifier for each entry
    run_id = Column(String(50), nullable=False)  # To store the run ID
    run_name = Column(String(100), nullable=False)  # New column
    revision_commit = Column(String(100), nullable=False)  # New column
    stats_name = Column(String(100), nullable=False)  # Name of the statistic
    stats_value = Column(String(100), nullable=False)  # Value of the statistic

class Statistical_AnalysisEPETargetvsMaskSimulationNegfocus(Base):
    __tablename__ = 'Mask_Simulation_Negfocus'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False)
    run_name = Column(String(100), nullable=False)  # New column
    revision_commit = Column(String(100), nullable=False)  # New column
    stats_name = Column(String(100), nullable=False)
    stats_value = Column(String(100), nullable=False)

class Statistical_AnalysisEPETargetvsMaskSimulationPosdose(Base):
    __tablename__ = 'Mask_Simulation_Posdose'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False)
    run_name = Column(String(100), nullable=False)  # New column
    revision_commit = Column(String(100), nullable=False)  # New column
    stats_name = Column(String(100), nullable=False)
    stats_value = Column(String(100), nullable=False)

class Statistical_AnalysisEPETargetvsMaskSimulationPosfocus(Base):
    __tablename__ = 'Mask_Simulation_Posfocus'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False)
    run_name = Column(String(100), nullable=False)  # New column
    revision_commit = Column(String(100), nullable=False)  # New column
    stats_name = Column(String(100), nullable=False)
    stats_value = Column(String(100), nullable=False)

class Statistical_AnalysisEPETargetvsNominalMaskSimulationf0d0(Base):
    __tablename__ = 'Mask_Simulation_f0d0'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False)
    run_name = Column(String(100), nullable=False)  # New column
    revision_commit = Column(String(100), nullable=False)  # New column
    stats_name = Column(String(100), nullable=False)
    stats_value = Column(String(100), nullable=False)

class Statistical_AnalysisWidthofPVBandbyDose(Base):
    __tablename__ = 'Width_of_PV_Band_by_Dose'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False)
    run_name = Column(String(100), nullable=False)  # New column
    revision_commit = Column(String(100), nullable=False)  # New column
    stats_name = Column(String(100), nullable=False)
    stats_value = Column(String(100), nullable=False)

class Statistical_AnalysisWidthofPVBandbyFocus(Base):
    __tablename__ = 'Width_of_PV_Band_by_Focus'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False)
    run_name = Column(String(100), nullable=False)  # New column
    revision_commit = Column(String(100), nullable=False)  # New column
    stats_name = Column(String(100), nullable=False)
    stats_value = Column(String(100), nullable=False)



# Logging setup
logging.basicConfig(
    filename='/home/emumba/Documents/PROJECT/record.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def parse_and_record_data(file_path, run_id, run_name, revision_commit):
    """Parse organized stats and record them to the database."""
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        logging.error(f"File not found: {file_path}")
        return

    # Clear previous entries for this run_id
    for table in [MainStats, RuntimeAnalysisStats, GeometricAnalysisStatsFermi, Statistical_AnalysisEPETargetvsMaskSimulationNegdose, Statistical_AnalysisEPETargetvsMaskSimulationNegfocus, Statistical_AnalysisEPETargetvsMaskSimulationPosdose, Statistical_AnalysisEPETargetvsMaskSimulationPosfocus, Statistical_AnalysisEPETargetvsNominalMaskSimulationf0d0, Statistical_AnalysisWidthofPVBandbyDose, Statistical_AnalysisWidthofPVBandbyFocus]:
        session.execute(delete(table).where(table.run_id == run_id))
    session.commit()

    # Open and read organized stats file
    with open(file_path, 'r') as file:
        current_table = None
        for line in file:
            line = line.strip()

            # Detect section headers
            if line.startswith("[") and line.endswith("]"):
                section_name = line[1:-1]  # Remove square brackets
                if section_name == "Main_Stats":
                    current_table = MainStats

                elif section_name == "Runtime_Analysis_Stats":
                    current_table = RuntimeAnalysisStats

                elif section_name == "Geometric_Analysis_Stats_Fermi":
                    current_table = GeometricAnalysisStatsFermi

                elif section_name == "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Negdose":
                    current_table = Statistical_AnalysisEPETargetvsMaskSimulationNegdose

                elif section_name == "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Negfocus":
                    current_table = Statistical_AnalysisEPETargetvsMaskSimulationNegfocus

                elif section_name == "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Posdose":
                    current_table = Statistical_AnalysisEPETargetvsMaskSimulationPosdose

                elif section_name == "Statistical_Analysis:EPE_Target_vs_Mask_Simulation_Posfocus":
                    current_table = Statistical_AnalysisEPETargetvsMaskSimulationPosfocus

                elif section_name == "Statistical_Analysis:EPE_Target_vs_Nominal_Mask_Simulation_f0d0":
                    current_table = Statistical_AnalysisEPETargetvsNominalMaskSimulationf0d0

                elif section_name == "Statistical_Analysis:Width_of_PV_Band_by_Dose":
                    current_table = Statistical_AnalysisWidthofPVBandbyDose

                elif section_name == "Statistical_Analysis:Width_of_PV_Band_by_Focus":
                    current_table = Statistical_AnalysisWidthofPVBandbyFocus
             
                else:
                    current_table = None  # Ignore unknown sections
                continue

            # Process lines within a section
            if current_table and "=" in line:
                stats_name, stats_value = map(str.strip, line.split("=", 1))
                # Insert data into the relevant table
                new_entry = current_table(run_id=run_id, run_name=run_name, revision_commit=revision_commit, stats_name=stats_name, stats_value=stats_value)
                session.add(new_entry)

                session.add(new_entry)

    # Commit changes to the database
    session.commit()
    logging.info(f"Data recorded successfully for run_id: {run_id}")


def reset_auto_increment():
    """Reset auto-increment for each table."""
    tables = [
        MainStats, RuntimeAnalysisStats, GeometricAnalysisStatsFermi,
        Statistical_AnalysisEPETargetvsMaskSimulationNegdose,
        Statistical_AnalysisEPETargetvsMaskSimulationNegfocus,
        Statistical_AnalysisEPETargetvsMaskSimulationPosdose,
        Statistical_AnalysisEPETargetvsMaskSimulationPosfocus,
        Statistical_AnalysisEPETargetvsNominalMaskSimulationf0d0,
        Statistical_AnalysisWidthofPVBandbyDose,
        Statistical_AnalysisWidthofPVBandbyFocus
    ]
    
    # Clear the table before resetting auto-increment
    for table in tables:
        # Delete all rows before resetting auto-increment
        session.execute(delete(table))
        session.commit()  # Commit after clearing the table
        
        # Reset the auto-increment counter
        session.execute(text(f"ALTER TABLE {table.__tablename__} AUTO_INCREMENT = 1;"))
        session.commit()  # Commit after resetting auto-increment



#Function to collect all 'organized_stats' files and their run_ids
def collect_organized_stats_files(base_directory):
    file_paths = []
    folder_run_ids = []
    
    for root, dirs, files in os.walk(base_directory):
        # Collect numeric folder names as run_ids
        if root == base_directory:  # Check only the immediate subdirectories
            folder_run_ids = [folder for folder in dirs if folder.isdigit()]
        # Collect file paths for 'organized_stats' files
        for file in files:
            if "organized_stats" in file and file.endswith(".txt"):
                file_paths.append(os.path.join(root, file))
    
    return folder_run_ids, file_paths


def printTemp(a1,a2,a3,a4):
    print(a1,a2,a3,a4)  

# Base rsync directory
base_directory = "/home/emumba/Documents/PROJECT/rsync"

# Initialize an array to store file paths
organized_stats_files = []


reset_auto_increment()


# Collect rsun_ids and file paths
run_ids, file_paths = collect_organized_stats_files(base_directory)
#run_ids.sort()  # Sort run_ids to ensure consistency
#print(run_ids,file_paths)

for run_id, file_path in zip(run_ids,file_paths):
    run_name = ''+run_id+'_rn'
    revision_commit = ''+run_id+'_rc'
   
    parse_and_record_data(file_path, run_id, run_name, revision_commit)
    printTemp(run_id,run_name,revision_commit,file_path)
# Close session
session.close()
