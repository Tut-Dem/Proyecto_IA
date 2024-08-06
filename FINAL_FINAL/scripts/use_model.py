import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

# Cargar el modelo entrenado
model = load_model('utils/depresion_model.h5')

# Cargar el tokenizador
with open('utils/tokenizer.pkl', 'rb') as handle:
    token = pickle.load(handle)

def limpieza(texto):
    texto = texto.lower()
    texto = re.sub(r'\\[a-z]', ' ', texto)
    texto = re.sub(r'[^a-z]', ' ', texto)
    texto = re.sub(r'\s+[a-z]\s+', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    patern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
    texto = patern.sub('', texto)
    texto = texto.strip()
    return texto

def predict(comment):
    # Preprocesar el comentario de entrada de la misma manera que se hizo durante el entrenamiento
    comentario_limpio = limpieza(comment)
    secuencia = token.texts_to_sequences([comentario_limpio])
    secuencia_padded = pad_sequences(secuencia, maxlen=100, padding='post')
    prediccion = model.predict(secuencia_padded)
    return prediccion[0][0] > 0.5
