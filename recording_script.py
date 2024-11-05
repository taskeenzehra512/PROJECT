import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the database URL with the correct credentials
DATABASE_URL = "mysql+mysqlconnector://d2s:D2s_1234!@localhost/emumba-qor"

# Set up the database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Define the Fermi table structure
Base = declarative_base()

class Fermi(Base):
    __tablename__ = 'fermi'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(Integer, nullable=False)
    stat_name = Column(String(100), nullable=False)
    stat_value = Column(String(100), nullable=False)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# Function to read fermi_stat.txt and save to the database
def save_statistics_to_db(file_path, run_id):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Print each line to check the file's contents
                print(f"Reading line: {line.strip()}")
                # Assuming each line has the format: stat_name: stat_value
                if ':' in line:
                    key, value = line.split(':', 1)
                    stat_name = key.strip()
                    stat_value = value.strip()

                    # Create a new Fermi instance
                    fermi_record = Fermi(run_id=run_id, stat_name=stat_name, stat_value=stat_value)

                    # Add it to the session
                    session.add(fermi_record)

            # Commit all the additions to the database
            session.commit()
            print(f"Committed {session.new} records to the database.")
    except Exception as e:
        print(f"An error occurred while saving to the database: {e}")

# Path to the fermi_stat.txt file
file_path = "/home/emumba/Documents/PROJECT/9871/qor/fermi_stat.txt"
run_id = 9871  # Set run_id to 9871

# Create a session
session = Session()

# Check the database connection
try:
    connection = engine.connect()
    print("Database connection successful.")
    connection.close()
except Exception as e:
    print(f"Database connection failed: {e}")

# Call the function to save statistics to the database
save_statistics_to_db(file_path, run_id)

# Close the session
session.close()
