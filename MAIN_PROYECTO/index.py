from flask import Flask, render_template, request, jsonify,send_file
import os

from scripts.Scrapping import scrapping
from scripts.useModel import hacerPred
from scripts.pruebas import diagrama_pastel

app = Flask(__name__)

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
        df = hacerPred(df)
    
        diagrama_pastel_path = diagrama_pastel(df)

        result = df.to_json(orient='records')

        return jsonify(success=True, result=result, diagrama_pastel=diagrama_pastel_path)

    except Exception as e:
        return jsonify(success=False, error=str(e))
    
    
@app.route('/get_diagrama_pastel')
def get_diagrama_pastel():
    path = request.args.get('path')
    if os.path.isfile(path):
        return send_file(path, mimetype='image/png')
    else:
        return "Archivo no encontrado", 404

@app.route('/result')
def result():
    data = request.args.get('data')
    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

