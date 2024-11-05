from flask import Flask, request, render_template_string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from recording_script import Fermi  # Importing the Fermi class from recording_script.py

app = Flask(__name__)

# Set up the database connection
DATABASE_URL = "mysql+mysqlconnector://d2s:D2s_1234!@localhost/emumba_qor"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# HTML Template for the form
HTML_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Statistics Query</title>
</head>
<body>
    <h1>Get Statistics by Run ID</h1>
    <form action="/api/statistics" method="post">
        <label for="run_id">Run ID:</label>
        <input type="number" id="run_id" name="run_id" required>
        <input type="submit" value="Submit">
    </form>
    <div id="results">
        {{ results|safe }}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_FORM, results='')

@app.route('/api/statistics', methods=['POST'])
def get_statistics():
    run_id = request.form.get('run_id', type=int)  # Get run_id from form data
    session = Session()
    try:
        records = session.query(Fermi).filter_by(run_id=run_id).all()
        if not records:
            return render_template_string(HTML_FORM, results="No records found for the given run_id.")

        # Build a plain text response
        response = []
        for record in records:
            response.append(f"{record.stat_name}: {record.stat_value}")
        return render_template_string(HTML_FORM, results="<br>".join(response))
    except Exception as e:
        return render_template_string(HTML_FORM, results=f"An error occurred: {str(e)}")
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)
