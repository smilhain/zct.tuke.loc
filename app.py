from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime
import json
from mysql.connector import pooling

app = Flask(__name__)

# Создаем пул соединений
db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=5,
    host="zct-sql.database.windows.net",
    user="zct_login",
    password="!*K-AzyFaFVJm7f",
    database="zct_tuke"
)

@app.route('/')
def index():
    temperature = request.args.get('temperature')
    humidity = request.args.get('humidity')
    recorded_at = datetime.now()

    db_conn = db_pool.get_connection()
    cursor = db_conn.cursor()

    cursor.execute("SELECT * FROM meteo ORDER BY date DESC")
    results = cursor.fetchall()



    if temperature is not None and humidity is not None:
      query = "INSERT INTO meteo (temperature, humidity, date) VALUES (%s, %s, %s)"
      cursor.execute(query, (temperature, humidity, recorded_at))
      db_conn.commit()

    cursor.close()
    db_conn.close()
    return render_template('index.html', results=results)

@app.route('/data')
def get_data():
    # Извлекаем соединение из пула
    db_conn = db_pool.get_connection()

    cursor = db_conn.cursor()
    cursor.execute("SELECT temperature, humidity, date FROM meteo")
    results = cursor.fetchall()
    cursor.close()

    # Возвращаем соединение в пул
    db_conn.close()

    data = []
    for result in results:
        temperature = result[0]
        humidity = result[1]
        date = result[2].strftime("%Y-%m-%d %H:%M:%S")
        data.append({'temperature': temperature, 'humidity': humidity, 'date': date})

    return jsonify(data)

@app.route('/last_record')
def last_record():
    # Извлекаем соединение из пула
    db_conn = db_pool.get_connection()

    cursor = db_conn.cursor()
    query = "SELECT temperature, humidity, date FROM meteo ORDER BY date DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    now_date = result[2].strftime("%Y-%m-%d %H:%M:%S")

    # Возвращаем соединение в пул
    db_conn.close()

    # Создать словарь с данными о последней записи
    record = {
        'temperature': str(result[0])+'°',
        'humidity': str(result[1])+'%',
        'date': now_date
    }
    # Вернуть данные в формате JSON
    return json.dumps(record)



if __name__ == '__main__':
    app.static_folder = 'static'
    app.run()