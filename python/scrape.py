import psycopg2
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime, date

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)
#CORS(app)


@app.route('/index.html')
def index():
    return send_from_directory('app', 'index.html')


@app.route('/scrape', methods=['POST'])
def scrape_data():
    browser = webdriver.Chrome()

    browser.get("https://www.thriftbooks.com/")
    time.sleep(5)

    book_names = browser.find_elements(By.CSS_SELECTOR, ".BookSlide-Title")
    book_authors = browser.find_elements(By.CSS_SELECTOR, ".BookSlide-Author")
    book_prices = browser.find_elements(By.CSS_SELECTOR, ".BookSlider-price")

    # conn = psycopg2.connect(
    #     host='localhost',
    #     database='StoreLoaded-DB',
    #     user='postgres',
    #     password='password',
    #     port=5432
    # )
    conn = psycopg2.connect(
        host='ep-lucky-limit-610252.eu-central-1.aws.neon.tech',
        database='neondb',
        user='moh',
        password='fe61CRBNptZO',
    )

    cursor = conn.cursor()
    data = []

    for i in range(len(book_names)):
        book_data = {
            "bookName": book_names[i].text,
            "bookAuthor": book_authors[i].text,
            "bookPrice":  book_prices[i].text,
        }

        # Remove "from:" prefix from book prices
        book_price_text = book_prices[i].text
        if "from:" in book_price_text:
            book_price_text = book_price_text.replace("from:", "")
        book_data['bookPrice'] = book_price_text

        data.append(book_data)

        sql = "INSERT INTO books (title, author, price) VALUES (%s, %s, %s)"
        cursor.execute(
            sql, (book_data['bookName'], book_data['bookAuthor'], book_data['bookPrice']))

    conn.commit()
    cursor.close()
    conn.close()
    json_string = json.dumps(data).replace("'", "\\'")
    print(json_string)
    return jsonify({'data': data})
    # browser.execute_script("console.log('{}')".format(json_string))


# Get ALL
@app.route('/get_books', methods=['GET'])
def get_data():
    try:
        conn = psycopg2.connect(
            host='ep-lucky-limit-610252.eu-central-1.aws.neon.tech',
            database='neondb',
            user='moh',
            password='fe61CRBNptZO',
        )
        cur = conn.cursor()
        query = '''SELECT * FROM books'''
        data = []
        cur.execute(query)
        results = cur.fetchall()
        for row in results:
            data.append(
                {
                    'id': row[0],
                    'title': row[1],
                    'author': row[2],
                    'price': row[3],
                    'created_at': row[6],
                    'updated_at': row[7]
                })
        cur.close()
        conn.close()
        return data
    except (Exception, psycopg2.Error) as error:
        print(error)
        return jsonify({'error': 'Failed to fetch data from database'}), 500

if __name__ == '__main__':
    app.run(debug=True)
