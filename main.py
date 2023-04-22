import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime, date

from selenium import webdriver

from selenium.webdriver.common.by import By

app = Flask(__name__)
#CORS(app)

# Start the Chrome web browser
browser = webdriver.Chrome()

# Load the web page
browser.get("https://www.bookdepository.com/")

# Find the element you want to scrape'

name = browser.find_elements(By.CLASS_NAME, 'title')
#link = browser.find_elements(By.CLASS_NAME, 'price')

# Print the text of the element

for l in name:
    print(l.text)
else:
    print('ERROR')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
