#!/bin/bash

# Run the Newman collection and generate both CLI 

newman run ./postman_collection.json \
    --reporters cli,html \
    

# After tests are done, call the Python script to send the email
python3 ./send_report.py