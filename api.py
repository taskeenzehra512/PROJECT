from flask import Flask, request, render_template_string
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

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
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>Get Statistics by Run ID</h1>
    <form action="/" method="post">
        <label for="run_id">Run ID:</label>
        <input type="number" id="run_id" name="run_id" required>
        <input type="submit" value="Submit">
    </form>

    {% if run_id is not none %}
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
                            <td>{{ record[0] }}</td>
                            <td>{{ record[1] }}</td>
                            <td>{{ record[2] }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <p>No records found for the specified Run ID.</p>
        {% endif %}
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    session = Session()  # Create a new session for database interaction
    all_records = []  # Initialize list to hold all records for the run_id
    run_id = None  # Initialize run_id to be used in the template

    if request.method == 'POST':
        run_id = request.form.get('run_id', type=int)
        if run_id is not None:  # Check if run_id is provided
            try:
                # Fetch records directly from the database
                query = text("SELECT run_id, stat_name, stat_value FROM fermi WHERE run_id = :run_id")
                result = session.execute(query, {'run_id': run_id})
                all_records = result.fetchall()  # Fetch all results as a list of tuples
                
                # Debugging statement to check the number of records fetched
                print(f"Number of records fetched for run_id {run_id}: {len(all_records)}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    
    session.close()  # Ensure the session is closed

    # Render the HTML template with results and all records
    return render_template_string(HTML_TEMPLATE, all_records=all_records, run_id=run_id)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
