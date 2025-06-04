import os, csv
import spacy
from pathlib import Path

nlp = spacy.load("sl_core_news_trf")

# Izhodni CSV
fields = [
    "doc_id","sentence",
    "entity_text","start_char","end_char",
    "pred_label"
]
with open("error_log.csv","w",newline="",encoding="utf-8") as fout:
    writer = csv.writer(fout)
    writer.writerow(fields)

    for path in Path("D:\\faks\\fri-fu\\diploma\\aplikacija\\24ur_articles").glob("*.*"):
        text = path.read_text(encoding="utf-8",errors="ignore")
        doc = nlp(text)
        for ent in doc.ents:
            sent = ent.sent.text.strip()
            writer.writerow([
                path.stem,
                sent,
                ent.text,
                ent.start_char - ent.sent.start_char,  # relativni offset
                ent.end_char   - ent.sent.start_char,
                ent.label_
            ])
