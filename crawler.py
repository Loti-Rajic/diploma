import os
import requests
from bs4 import BeautifulSoup
import feedparser

# Nastavimo osnovni URL in direktorij za shranjevanje člankov
BASE_URL = "https://www.24ur.com/popin"
SAVE_DIR = "24ur_articles"
os.makedirs(SAVE_DIR, exist_ok=True)



RSS_URL = "https://www.24ur.com/rss"

def get_article_links():
    """ Pridobi povezave do člankov iz RSS vira 24ur.com """
    feed = feedparser.parse(RSS_URL)
    
    article_links = [entry.link for entry in feed.entries]

    return article_links  # Vrnemo seznam povezav do člankov


import requests
from bs4 import BeautifulSoup

def get_article_content(article_url):
    """ Pridobi naslov in vsebino članka s strani """
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # Poiščemo naslov članka
        title_tag = soup.find("h1")
        if not title_tag:
            print(f"⚠️ Preskakujem (ni članka): {article_url}")
            return None, None
        title = title_tag.get_text(strip=True)

        # Poiščemo glavno telo članka (filtriramo reklame)
        article_body = soup.find("div", class_="article")
        if not article_body:
            print(f"⚠️ Preskakujem (ni vsebine): {article_url}")
            return None, None

        # Zberemo prave odstavke
        content_paragraphs = article_body.find_all("p")
        filtered_content = "\n".join([p.get_text(strip=True) for p in content_paragraphs if len(p.get_text(strip=True)) > 10])

        return title, filtered_content

    except Exception as e:
        print(f"🚨 Napaka pri članku {article_url}: {e}")
        return None, None


    except Exception as e:
        print(f"🚨 Napaka pri članku {article_url}: {e}")
        return None, None

def save_article(title, content, index):
    """ Shrani vsebino članka v .txt datoteko """
    safe_title = "".join(c if c.isalnum() else "_" for c in title)[:50]  # Prilagodi ime datoteke
    file_path = os.path.join(SAVE_DIR, f"{index}_{safe_title}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(title + "\n\n" + content)
    
    print(f"✅ Članek shranjen: {file_path}")

# --- Glavna funkcija ---
def main():
    print("📡 Začenjam iskanje člankov...")
    article_links = get_article_links()
    print(f"🔎 Najdenih {len(article_links)} člankov.")


    count = 0
    for i, article_url in enumerate(article_links):
        title, content = get_article_content(article_url)
        if title and content:
            save_article(title, content, count)
            count += 1
            if count >= 50:
                break

    print(f"✅ Končano! Shranjenih {count} člankov.")

if __name__ == "__main__":
    main()
