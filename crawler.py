import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        # Pošlji zahtevo na spletno stran
        response = requests.get(url)
        if response.status_code == 200:
            # Razčleni HTML kodo strani
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Izloči vse besedilo, izključi skripte in stile
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()
            
            # Pridobi čisto besedilo iz preostale HTML strukture
            text = soup.get_text(separator=' ')
            
            # Odstrani odvečne praznine
            clean_text = ' '.join(text.split())
            return clean_text
        else:
            return f"Napaka pri dostopu do {url}: {response.status_code}"
    except Exception as e:
        return f"Napaka: {str(e)}"

# Primer uporabe
url = "https://www.glu-sg.si/en/exhibition/nina-tovornik-metonimije/?from=front"
vsebina = extract_text_from_url(url)

with open("vsebina.txt", "w", encoding="utf-8") as file:
    file.write(vsebina)

