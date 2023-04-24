import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import json
from datetime import date

load_dotenv()
app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


@app.route('/hello/<username>', methods=['POST'])
def hello_post(username):
    CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT, dob DATE);"
    INSERT_USERS_TABLE = "INSERT INTO users (name, dob) VALUES (%s, %s)"

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            val = (username, request.json["dateOfBirth"])
            cursor.execute(INSERT_USERS_TABLE, val)
            connection.commit()
    return "No Content", 204


@app.route('/hello/<username>', methods=['GET'])
def hello_get(username):
    sql_select_query = """select * from users"""
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_select_query)
            record = cursor.fetchall()
    for each_record in record:
        if each_record[1] == username:
            print("record found")
            dob = record[0][2]
            today = date.today()
            dob_replaced = dob.replace(year=today.year + 1)
            days_until = abs(today - dob_replaced)
            if days_until == 0:
                response = '{"message": "Hello,' + \
                    username + ' Happy birthday!"}'
                return response, 201
            else:
                response = '{"message": "Hello,' + username + \
                    '! Your birthday is in ' + str(days_until) + '  day(s)"}'
                return response, 201
        else:
            return "Record Not found", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
