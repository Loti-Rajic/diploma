import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import spacy
import sl_core_news_trf

# Nalaganje modela
nlp = spacy.load("sl_core_news_trf")

# Slovar za pretvorbo angleških oznak v slovenske
pos_translation = {
    "NOUN": "samostalnik",
    "VERB": "glagol",
    "ADJ": "pridevnik",
    "ADV": "prislov",
    "PRON": "zaimek",
    "PROPN": "lastno ime",
    "DET": "členek",
    "ADP": "predlog",
    "CCONJ": "veznik",
    "SCONJ": "podredni veznik",
    "NUM": "števnik",
    "PART": "členek",
    "INTJ": "medmet",
    "PUNCT": "ločilo",
    "SYM": "simbol",
    "X": "drugo"
}

# Funkcija za anonimizacijo entitet v besedilu
def anonymize_entities(text):
    doc = nlp(text)
    anonymized_text = []
    
    for ent in doc.ents:
        if ent.label_ == "PER":
            anonymized_text.append(f"[IME]")
        elif ent.label_ == "LOC":
            anonymized_text.append(f"[KRAJ]")
        elif ent.label_ == "ORG":
            anonymized_text.append(f"[ORGANIZACIJA]")
        else:
            anonymized_text.append(ent.text)  # Če je entiteta druge vrste, jo ohranimo
    
    # Vzpostavi besedilo z zamenjanimi entitetami
    for token in doc:
        if token.ent_iob_ == "O":  # Če ni del entitete
            anonymized_text.append(token.text)
    
    return " ".join(anonymized_text)

# Preberi besedilo iz datoteke
def process_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Obdelaj besedilo z modelom spaCy
        doc = nlp(text)
        
        # Anonimiziraj imenovane entitete
        anonymized_text = anonymize_entities(text)
        
        # Pretvori oznake delov govora v slovenske izraze
        tokens_pos = [(w.text, pos_translation.get(w.pos_, w.pos_)) for w in doc]
        
        return anonymized_text, tokens_pos

    except Exception as e:
        return f"Napaka pri branju datoteke: {str(e)}"

# Pot do datoteke
for file in "D:\\faks\\fri-fu\\diploma\\aplikacija\\24ur_articles".listdir():
    file_path = file
    process_file(file_path)

# Zapis v datoteko
with open("rezultat.txt", "w", encoding="utf-8") as file:
    file.write(f"Anonimizirano besedilo:\n{anonimizirano}\n\nOznake:\n{rezultat}")
