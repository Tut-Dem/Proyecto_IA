import matplotlib.pyplot as plt
import pandas as pd
import os

def diagrama_pastel(dataframe):

    categorias = dataframe['prediccion'].value_counts()
    
    # Crear el diagrama de pastel
    plt.figure(figsize=(8, 8))
    plt.pie(categorias, labels=categorias.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribución de Categorías')

    # Definir la ruta de la carpeta 'temp' y del archivo
    temp_dir = 'temp'
    temp_path = os.path.join(temp_dir, 'diagrama_pastel.png')
    
    plt.savefig(temp_path)
    plt.close()

    return temp_path
