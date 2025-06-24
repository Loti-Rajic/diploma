import argparse
import csv
import json
from collections import defaultdict
import pandas as pd
from pathlib import Path
import spacy

def xlsx_to_train_dev(input_xlsx, train_jsonl):
    df = pd.read_excel(input_xlsx)
    train_grouped = defaultdict(list)

    for _, row in df.iterrows():
        error = row.get("ERROR", "")
        if pd.isna(error):
            error = ""
        error = str(error).strip().lower()
        text = str(row["sentence"]).strip()
        start = int(row["start_char"])
        end = int(row["end_char"])
        label = str(row.get("pred_label", "")).strip()
        
        if not text or not label:
            continue
        key = text  # <-- samo po textu, brez doc_id
        entry = [text[start: end], start, end, label, error]
        train_grouped[key].append(entry)


    def write_jsonl(grouped, output_path):
        with open(output_path, "w", encoding="utf-8") as fout:
            for text, ents in grouped.items():
                unique = sorted({tuple(e) for e in ents}, key=lambda x: x[0])
                obj = {"text": text, "ents": [list(e) for e in unique]}
                fout.write(json.dumps(obj, ensure_ascii=False) + "\n")

    write_jsonl(train_grouped, train_jsonl)

xlsx_to_train_dev(
    "D:\\faks\\fri-fu\\diploma\\aplikacija\\errorlog6-2.xlsx",
    "extractedfromexcel6-2.jsonl"
)