import requests
from bs4 import BeautifulSoup

# Define una instancia alternativa de Nitter
nitter_instance = "https://nitter.it"

def scrapping(url):
    # Asegúrate de que la URL comience con la instancia de Nitter seleccionada
    if not url.startswith(nitter_instance):
        # Extrae el identificador de usuario o parte final de la URL original
        username = url.split('/')[-1]
        # Construye la URL con la instancia de Nitter especificada
        url = f"{nitter_instance}/{username}"
    
    try:
        # Realiza la solicitud HTTP con un tiempo de espera de 10 segundos
        response = requests.get(url, timeout=10)
        
        # Verifica que la solicitud fue exitosa
        if response.status_code == 200:
            # Parsear el contenido HTML de la página
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Ejemplo: Obtener y mostrar el texto del primer tweet
            tweet = soup.find('div', {'class': 'tweet-content'})
            if tweet:
                print("Primer tweet:", tweet.text.strip())
            else:
                print("No se encontraron tweets.")
        else:
            print(f"Error al acceder a {url}: {response.status_code}")
    except requests.exceptions.ConnectTimeout:
        print(f"Conexión a {url} agotada.")
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a {url}: {e}")

# Ejemplo de uso
url = "https://x.com/JulianMaciasT"
scrapping(url)
