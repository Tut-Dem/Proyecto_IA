from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session
import os
from scripts.scrapping import scrapping
from scripts.use_model import predict

import json
import urllib.parse

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
    try:
        username = request.form['username']
        df = scrapping(username)
        
        # Realizar predicciones sobre el DataFrame obtenido
        df['prediction'] = df['cleaned_text'].apply(predict)
        df['formatted_date'] = df['date'].apply(lambda x: x.strftime("%H:%M/%d/%m/%y"))
        
        # Asegúrate de que las fechas sean convertidas a string antes de serializar
        df['date'] = df['date'].astype(str)
        
        result = df.to_dict(orient='records')
        
        # Almacenar el resultado en la sesión
        session['result'] = result

        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/result')
def result():
    data = session.get('result', None)
    if data is None:
        return redirect(url_for('home'))
    
    try:
        json_data = json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return jsonify(success=False, error=str(e))
    
    return render_template('result.html', data=json_data)

@app.route('/loading')
def loading():
    return render_template('loading.html')

if __name__ == '__main__':
    app.run(debug=True)
