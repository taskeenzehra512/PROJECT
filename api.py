from flask import Flask, request, render_template_string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from recording_script import Fermi  # Importing the Fermi class from recording_script.py

app = Flask(__name__)

# Set up the database connection using SQLAlchemy
DATABASE_URL = "mysql+mysqlconnector://d2s:D2s_1234!@localhost/emumba_qor"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# HTML Template for the form and the data table
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Statistics Query</title>
    <style>
        table {
            width: 100%; /* Make the table full width */
            border-collapse: collapse; /* Merge table borders */
        }
        table, th, td {
            border: 1px solid black; /* Add borders to the table, headers, and cells */
        }
        th, td {
            padding: 8px; /* Add padding to table headers and cells */
            text-align: left; /* Align text to the left */
        }
    </style>
</head>
<body>
    <h1>Get Statistics by Run ID</h1>
    <form action="/api/statistics" method="post">
        <label for="run_id">Run ID:</label>
        <input type="number" id="run_id" name="run_id" required> <!-- Input field for run_id -->
        <input type="submit" value="Submit"> <!-- Submit button -->
    </form>
    <div id="results">
        {{ results|safe }} <!-- Display results message if applicable -->
    </div>
    {% if all_records %}
    <h2>Statistics for Run ID: {{ run_id }}</h2>
  <table>
    <thead>
        <tr>
            <th>Run ID</th>
            <th>Stat Name</th>
            <th>Stat Value</th>
        </tr>
    </thead>
    <tbody>
        {% for record in all_records %}
            <tr>
                <td>{{ record.run_id }}</td>
                <td>{{ record.stat_name }}</td>
                <td>{{ record.stat_value }}</td>
            </tr>
        {% endfor %}
    </tbody>
</table>

    {% else %}
    <p>No records found for the specified Run ID.</p> <!-- Message if no records found -->
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    # Render the home page with an empty results section and no records
    return render_template_string(HTML_TEMPLATE, results='', all_records=[], run_id='')

@app.route('/api/statistics', methods=['POST'])
def get_statistics():
    # Get the run_id from the form data
    run_id = request.form.get('run_id', type=int)
    session = Session()  # Create a new session for database interaction
    results = ''  # Initialize results message
    all_records = []  # Initialize list to hold all records for the run_id
    try:
        # Query the Fermi table for all records with the specified run_id
        all_records = session.query(Fermi).filter_by(run_id=run_id).all()
        
        # Debugging statement to check the number of records fetched
        print(f"Number of records fetched for run_id {run_id}: {len(all_records)}")
        
        if not all_records:
            results = "No records found for the given run_id."  # Update results if no records found
    except Exception as e:
        results = f"An error occurred: {str(e)}"  # Capture any exceptions
    finally:
        session.close()  # Ensure the session is closed to release resources
    
    # Render the HTML template with results, all records, and the run_id
    return render_template_string(HTML_TEMPLATE, results=results, all_records=all_records, run_id=run_id)


if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)