from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy import select

app = Flask(__name__)

# MySQL Database URI
DATABASE_URI = 'mysql+pymysql://d2s:D2s_1234!@localhost/emumba_qor'

# Create engine to connect to MySQL database
engine = create_engine(DATABASE_URI, echo=True)

# Set up sessionmaker to manage database sessions
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

# Base class for models
Base = declarative_base()

# Define Models to Map MySQL Tables
class Geometric_Analysis_Stats_Fermi(Base):
    __tablename__ = 'Geometric_Analysis_Stats_Fermi'  # Name of the table in MySQL
    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key column
    run_id = Column(String(100))
    stats_name = Column(String(100))
    stats_value = Column(String(255))  # Adjust length as needed
    run_name = Column(String(100))
    revision_commit = Column(String(100))

class Main_Stats(Base):
    __tablename__ = 'Main_Stats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(100))
    stats_name = Column(String(100))
    stats_value = Column(String(255))  # Adjust length as needed
    run_name = Column(String(100))
    revision_commit = Column(String(100))

class Mask_Simulation_Negdose(Base):
    __tablename__ = 'Mask_Simulation_Negdose'
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(100))
    stats_name = Column(String(100))
    stats_value = Column(String(255))  # Adjust length as needed
    run_name = Column(String(100))
    revision_commit = Column(String(100))

class Mask_Simulation_Negfocus(Base):
    __tablename__ = 'Mask_Simulation_Negfocus'
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(100))
    stats_name = Column(String(100))
    stats_value = Column(String(255))  # Adjust length as needed
    run_name = Column(String(100))
    revision_commit = Column(String(100))

# Define more models for the remaining tables...

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}  # Initialize results as an empty dictionary

    if request.method == 'POST':
        # Get input values from the form
        input_text1 = request.form.get('input1')  # run_id
        input_text2 = request.form.get('input2')  # run_name
        input_text3 = request.form.get('input3')  # revision_commit
        
        # List of table models to query
        table_models = {
            'Geometric_Analysis_Stats_Fermi': Geometric_Analysis_Stats_Fermi,
            'Main_Stats': Main_Stats,
            'Mask_Simulation_Negdose': Mask_Simulation_Negdose,
            'Mask_Simulation_Negfocus': Mask_Simulation_Negfocus,
            # Add the rest of your models here
        }

        # Initialize session
        session = Session()

        # Loop through all models to query based on inputs
        for table_name, model in table_models.items():
               # Start building the query dynamically
            query = select(model)

            # Dynamically apply filters based on provided inputs
            if input_text1:  # run_id is provided
                query = query.where(model.run_id == input_text1)
            if input_text2:  # run_name is provided
                query = query.where(model.run_name == input_text2)
            if input_text3:  # revision_commit is provided
                query = query.where(model.revision_commit == input_text3)

            # Execute the query to fetch results
            result = session.execute(query).scalars().all()

            # Store the result in the dictionary
            results[table_name] = result

        session.close()  # Close the session after queries are done

    return render_template('index.html', results=results)  # Pass the results to the template

if __name__ == '__main__':
    app.run(debug=True)
