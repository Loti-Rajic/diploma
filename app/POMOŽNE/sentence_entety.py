import spacy
import json
import os

# Naloži spaCy model za slovenščino
nlp = spacy.load("sl_core_news_trf")

# Pot do vhodnega direktorija
input_dir = 'D:\\faks\\fri-fu\\diploma\\aplikacija\\24ur_articles\\1-sklop'

# Pot do izhodnega direktorija
output_dir = 'D:\\faks\\fri-fu\\diploma\\aplikacija\\24ur_articles\\1-sklop\\output'
os.makedirs(output_dir, exist_ok=True)

# Pojdi čez vse txt datoteke v direktoriju
for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.jsonl")

        # Preberi besedilo iz vhodne datoteke
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Obdelaj besedilo s spaCy
        doc = nlp(text)

        # Shrani rezultate v JSONL datoteko
        with open(output_file_path, 'w', encoding='utf-8') as jsonl_file:
            for sent in doc.sents:
                entities = [[ent.start_char - sent.start_char, ent.end_char - sent.start_char, ent.label_] for ent in sent.ents]
                sentence_entry = {'text': sent.text, 'ents': entities}
                jsonl_file.write(json.dumps(sentence_entry, ensure_ascii=False) + '\n')

        print(f"Rezultati za '{filename}' so shranjeni v '{output_file_path}'.")