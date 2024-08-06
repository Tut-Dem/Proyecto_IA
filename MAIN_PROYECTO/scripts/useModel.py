import pickle
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

def hacerPred(dataframe):
    # Cargar el tokenizer desde el archivo pickle
    with open('utils/token_fin.pkl', 'rb') as f:
        tokenizer = pickle.load(f)

    # Cargar el modelo desde el archivo .h5
    modelo_cargado = load_model('utils/models/depresionAM.h5')
        
    # Convertir el texto en secuencias de enteros usando el tokenizer
    dataframe['text'] = tokenizer.texts_to_sequences(dataframe['text'])
    
    # Preparar los datos para la predicción
    X = list(dataframe['text'])
    longitud_maxima = 50  # Asegúrate de que coincida con el valor usado en el entrenamiento
    X = pad_sequences(X, maxlen=longitud_maxima, padding='post')
    X = np.array(X)
    
    # Realizar la predicción
    prediccion = modelo_cargado.predict(X)
    prediccion = (prediccion > 0.4)  # Convertir las probabilidades en valores booleanos

    # Añadir la columna de predicción al DataFrame
    dataframe['prediccion'] = prediccion.astype(bool).flatten()  
    

    return dataframe


