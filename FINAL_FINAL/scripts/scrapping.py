import os
import re
import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords
import praw
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

def get_reddit_comments(subreddit_name, limit=20):
    reddit = praw.Reddit(client_id='xopGjRv-nvIaf0ba6bM-uQ',
                         client_secret='ieJxpSJ_sonhrB54RU7FbjZoqugZhA',
                         user_agent='Xscrapping')
    
    comments_list = []
    subreddit = reddit.subreddit(subreddit_name)
    total_comments = 0

    for submission in subreddit.hot(limit=100):  # Obtén las publicaciones más populares
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            if total_comments >= limit:
                break
            comments_list.append({
                'text': comment.body,
                'user': comment.author.name if comment.author else 'N/A',
                'date': comment.created_utc
            })
            total_comments += 1
        if total_comments >= limit:
            break
    
    return comments_list

def get_subreddit_name(url):
    # Extrae el nombre del subreddit de la URL
    match = re.search(r'reddit\.com/r/([^/]+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("URL inválida. Asegúrate de que sea una URL de un subreddit de Reddit.")

def scrapping(url):
    try:
        subreddit_name = get_subreddit_name(url)
        comments = get_reddit_comments(subreddit_name)
        
        lista_limpia = []
        for comment in tqdm(comments):
            comment['cleaned_text'] = limpieza(comment['text'])
            lista_limpia.append(comment)

        df = pd.DataFrame(lista_limpia)
        
        print(df)
        condicion = df['cleaned_text'] == ""
        df = df.loc[~condicion]

        # Convertir la fecha a un formato legible
        df['date'] = pd.to_datetime(df['date'], unit='s')
        df['formatted_date'] = df['date'].dt.strftime('%H:%M/%d/%m/%y')
        
        return df

    except Exception as e:
        print(f"Error al obtener comentarios: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

# Ejemplo de uso:
if __name__ == '__main__':
    url = "https://www.reddit.com/r/depression/"
    df = scrapping(url)
    print(df)
