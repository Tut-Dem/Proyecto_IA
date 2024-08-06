from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session
import os
from scripts.scrapping import scrapping
from scripts.use_model import predict
import json
import pandas as pd


app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuración de flask-session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/solicitudes')
def query():
    return render_template('solicitudes.html')

@app.route('/process_username', methods=['POST'])
def process_username():
    url = request.form['username']
    df = scrapping(url)
    result = df.drop(columns=['cleaned_text']).to_dict(orient='records')
    return jsonify(success=True, result=result)

@app.route('/result')
def result():
    data = request.args.get('data')
    if data:
        data = json.loads(data)

    si_count = sum(1 for row in data if row['is_depressive'])
    no_count = sum(1 for row in data if not row['is_depressive'])

    return render_template('result.html', data=data, si_count=si_count, no_count=no_count)

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/graphics')
def grafica():
    return render_template('grafica.html')

if __name__ == '__main__':
    app.run(debug=True)
