from typing import List, Dict
import simplejson as json
import requests
import configparser
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

Covidapp = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'CovidRegistration'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Vaccine Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<int:city_id>', methods=['GET'])
def record_view(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['GET'])
def form_edit_get(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['POST'])
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldLat'), request.form.get('fldLong'),
                 request.form.get('fldCountry'), request.form.get('fldAbbreviation'),
                 request.form.get('fldCapitalStatus'), request.form.get('fldPopulation'), city_id)
    sql_update_query = """UPDATE tblCitiesImport t SET t.fldName = %s, t.fldLat = %s, t.fldLong = %s, t.fldCountry = 
    %s, t.fldAbbreviation = %s, t.fldCapitalStatus = %s, t.fldPopulation = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New City Form')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldLat'), request.form.get('fldLong'),
                 request.form.get('fldCountry'), request.form.get('fldAbbreviation'),
                 request.form.get('fldCapitalStatus'), request.form.get('fldPopulation'))
    sql_insert_query = """INSERT INTO tblCitiesImport (fldName,fldLat,fldLong,fldCountry,fldAbbreviation,fldCapitalStatus,fldPopulation) VALUES (%s, %s,%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:city_id>', methods=['POST'])
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblCitiesImport WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['PUT'])
def api_edit(city_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/cities/<int:city_id>', methods=['DELETE'])
def api_delete(city_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp

@app.route('/api/openweathermap/')
def weather_dashboard():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def render_results():
    city_name = request.form['CityName']

    api_key = get_api_key()
    data = get_weather_results(city_name, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]

    return render_template('results.html',
                           location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_results(city_name, api_key):
   api_url = "http://api_url = api.openweathermap.org/" \
             "data/2.5/weather?q={}&units=imperial&appid={}.format(city_name, api_key)"
   r = requests.get(api_url)
   return r.json()

def weather_dashboard():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def render_results1():
    zip_code = request.form['zipcode']

    api_key = get_api_key()
    data = get_weather_results(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]

    return render_template(
                           location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def zip_code(zip_code, api_key):
    api_url = "http://api.openwaethermap.org/data/2.5/weather?zip=()&appid=.format(zip_code, api_key)"
    r = requests.get(api_url)
    return r.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0')