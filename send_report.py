import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import glob

# Email configuration
sender_email = "taskeen.zehra@emumba.com"
receiver_email = "taskeen.zehra@emumba.com, mustafa.amjad@emumba.com"
subject = "Newman HTML Report"
smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
smtp_port = 587  # Usually 587 for TLS
password = "stcu algn opzz syda"  # Use an app-specific password for Gmail

# Path to the newman folder
newman_folder = "/home/emumba/Documents/PROJECT/newman/"

# Find the most recent HTML report in the newman folder
html_files = glob.glob(os.path.join(newman_folder, "*.html"))
if not html_files:
    print("No HTML reports found.")
    exit()

# Sort files by modification time (latest first)
latest_report = max(html_files, key=os.path.getmtime)

# Create the email
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Add email body
body = "Please find the attached Newman HTML report. Open the attachment in a browser to view the report."
message.attach(MIMEText(body, "plain"))

# Attach the latest HTML report
with open(latest_report, "rb") as attachment:
    part = MIMEBase("text", "html")  # Specify the correct MIME type for HTML
    part.set_payload(attachment.read())

# Encode the file to base64
encoders.encode_base64(part)

# Add headers for the attachment
part.add_header(
    "Content-Disposition",
    f"attachment; filename={os.path.basename(latest_report)}",
)
message.attach(part)

# Send the email
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Start TLS encryption
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
