# (instalar) pip install ntscraper

import re
import nltk
from nltk.corpus import stopwords
import pickle
from ntscraper import Nitter
nltk.download('stopwords')
import pandas as pd
from tqdm import tqdm

def limpieza(texto):
  texto = texto.lower()
  texto = re.sub(r'\\[a-z]',' ',texto)
  texto = re.sub(r'[^a-z]',' ',texto)
  texto = re.sub(r'\s+[a-z]\s+',' ',texto)
  texto = re.sub(r'\s+',' ',texto)
  patern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
  texto = patern.sub('', texto)
  texto = texto.strip()
  return texto

name = input("ingresa el nombre a ser escaneado: ")

with open('python_pkl\scrap_instance.pkl','rb') as f:
    scrap2 = pickle.load(f)
 
tweets = scrap2.get_tweets(name, mode='user', number=15)


final_tweets = []
for x in tweets['tweets']:
    data = [x['text'],x['date']]
    final_tweets.append(data)
    
dat = pd.DataFrame(final_tweets, columns =['text','date'])


texto_lista = list(dat['text'])

lista_limpia = []
for texto in tqdm(texto_lista) :
  lista_limpia.append(limpieza(texto))

dat['text']=lista_limpia

condicion = dat['text'] == ""
dat = dat.loc[~condicion]

df = dat.copy()

df['date'] = pd.to_datetime(df['date'], format='%b %d, %Y · %I:%M %p UTC')
df['mes'] = df['date'].dt.month_name()
df['dia'] = df['date'].dt.day
df['año'] = df['date'].dt.year
df['hora'] = df['date'].dt.hour
df['minuto'] = df['date'].dt.minute
df['periodo'] = df['date'].dt.strftime('%p')


dat= df.drop(columns=['date', 'minuto', 'periodo'],axis=1 )
  

print (dat)