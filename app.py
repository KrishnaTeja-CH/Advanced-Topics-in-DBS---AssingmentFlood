import textwrap
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pandas as pd
import pyodbc
import timeit
import redis
import hashlib
import pickle
from pymongo import MongoClient

app = Flask(__name__)

driver = '{ODBC Driver 17 for SQL Server}'
server_name = 'thedomain'
database_name = 'Krishna'
username = "itsmekt"
password = "******"
server = '{server_name}.database.windows.net,1433'.format(server_name=server_name)
string_connection = textwrap.dedent('''
    Driver={driver};
    Server={server};
    Database={database};
    Uid={username};
    Pwd={password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
'''.format(
    driver=driver,
    server=server,
    database=database_name,
    username=username,
    password=password
))
connection = pyodbc.connect(connection_string)
crsr = connection.crsr()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/volcdatarange', methods=['GET', 'POST'])
def volc_datarange():
    volcano = []
    if request.method == 'POST':
        estart = request.form.get('srange')
        eend = request.form.get('strange')
        vstart = request.form.get('snumstart')
        vend = request.form.get('stnumstop')
        start_time = timeit.default_timer()
        crsr.execute("select Volcano_Name, Country, Region, Latitude, Longitude, Elev from v where Elev > ? and Elev < ? and Number > ? and Number < ?", estart, eend, vstart, vend)
        for data in crsr:
            volcano.append(data)
        volcanos_len = len(volcano)
        elapsed = timeit.default_timer() - start_time
    return render_template('volc_datarange.html',volcano = volcano, length = volcanos_len, times = elapsed)

if __name__ == '__main__':
    app.run()
