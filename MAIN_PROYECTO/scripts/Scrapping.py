import os
import re
import time
import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords
from ntscraper import Nitter
import nltk

nltk.download('stopwords')

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

def get_user(user):
    user = str(user)
    user = user.split('://')[-1]
    user = user.split('/')[-1]
    return user

def scrapping(url):
    print(url)
    name = get_user(url)
    print(name)
    
    try:
        # Especificar una instancia de Nitter para evitar la limitación de tasa
        scrap = Nitter()
        tweets = scrap.get_tweets(name, mode='user', number=15)
        
        final_tweets = []
        for x in tweets['tweets']:
            data = [x['text'], x['date'], x['link'], x['is-retweet']]
            final_tweets.append(data)
            
        df = pd.DataFrame(final_tweets, columns=['text', 'date', 'link', 'rep'])
        df = df.loc[df['rep'] != True]
            
        texto_lista = list(df['text'])

        lista_limpia = []
        for texto in tqdm(texto_lista):
            lista_limpia.append(limpieza(texto))

        df['text'] = lista_limpia
        
        print(df)
        condicion = df['text'] == ""
        df = df.loc[~condicion]
    
        df['date'] = pd.to_datetime(df['date'], format='%b %d, %Y · %I:%M %p UTC')
        df['formatted_date'] = df['date'].dt.strftime('%H:%M/%d/%m/%y')

        df = df.drop(columns=['date', 'rep'], axis=1)
        
        return df

    except Exception as e:
        print(f"Error al obtener tweets: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

# Ejemplo de uso:
if __name__ == '__main__':
    url = "https://x.com/XusShiv"
    # url = "https://x.com/realDonaldTrump"
    df = scrapping(url)
    print(df)
