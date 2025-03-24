import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import spacy

# Nalaganje slovenskega modela
nlp = spacy.load("sl_core_news_trf")

# Funkcija za anonimizacijo entitet
def anonymize_entities(doc):
    anonymized_tokens = []
    skip_next = False
    
    for token in doc:
        if skip_next:
            skip_next = False
            continue
        
        if token.ent_type_ == "PER":
            anonymized_tokens.append("[IME]")
            if token.whitespace_:
                anonymized_tokens.append(" ")
        elif token.ent_type_ == "LOC":
            anonymized_tokens.append("[KRAJ]")
            if token.whitespace_:
                anonymized_tokens.append(" ")
        elif token.ent_type_ == "ORG":
            anonymized_tokens.append("[ORGANIZACIJA]")
            if token.whitespace_:
                anonymized_tokens.append(" ")
        else:
            anonymized_tokens.append(token.text)
            if token.whitespace_:
                anonymized_tokens.append(" ")
    
    return ''.join(anonymized_tokens)

# Preberi in obdelaj besedilo iz datoteke
def process_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Obdelaj besedilo z modelom spaCy
        doc = nlp(text)

        # Anonimiziraj imenovane entitete
        anonymized_text = anonymize_entities(doc)

        # Shranjuj anonimizirano besedilo v novo datoteko
        filename=file_path.replace(".txt", "")
        output_path = f"{filename}_anonimizirano.txt"
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(anonymized_text)
            
        return output_path

    except Exception as e:
        return f"Napaka pri branju datoteke: {str(e)}"

# Pot do direktorija
directory = "D:\\faks\\fri-fu\\diploma\\aplikacija\\24ur_articles"

# Uporabi os.listdir() za pridobitev seznama datotek v direktoriju
files = os.listdir(directory)

# Zdaj lahko iteriraš čez seznam datotek
for file in files:
    file_path = os.path.join(directory, file)
    output_path = process_file(file_path)
    print(f"Obdelana datoteka shranjena kot {output_path}")
