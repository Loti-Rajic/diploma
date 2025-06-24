import argparse
import csv
import json
from collections import defaultdict
import pandas as pd
from pathlib import Path
import spacy

# python app\POMOŽNE\preverjanje_napak.py xlsc_to_train_dev --input_xlsx "D:\faks\fri-fu\diploma\aplikacija\EXCEL\errorlog8.xlsx" --output_jsonl train_data4.jsonl
def xlsx_to_train_dev(input_xlsx, train_jsonl, dev_jsonl):
    df = pd.read_excel(input_xlsx)
    train_grouped = defaultdict(list)
    dev_grouped = defaultdict(list)
 
    for _, row in df.iterrows():
        error = row.get("ERROR", "")
        # popravi NaN na ""
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
        entry = [start, end, label]

        if error == "label":
            dev_grouped[key].append(entry)
        elif error == "" or error is None :
            train_grouped[key].append(entry)
        # ostalo ignoriraj

    def write_jsonl(grouped, output_path):
        with open(output_path, "w", encoding="utf-8") as fout:
            for text, ents in grouped.items():
                unique = sorted({tuple(e) for e in ents}, key=lambda x: x[0])
                obj = {"text": text, "ents": [list(e) for e in unique]}
                fout.write(json.dumps(obj, ensure_ascii=False) + "\n")

    write_jsonl(train_grouped, train_jsonl)
    write_jsonl(dev_grouped, dev_jsonl)


# python preverjanje_napak.py extract_csv --input_dir "D:\faks\fri-fu\diploma\aplikacija\24ur_articles\1-sklop" --output_csv error_log4.csv
def csv_to_train_dev(input_csv, train_jsonl, dev_jsonl):
    # Group by sentence and doc_id for train and dev separately
    train_grouped = defaultdict(list)
    dev_grouped = defaultdict(list)

    with open(input_csv, encoding="utf-8") as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            if "ERROR" in row and row["ERROR"].strip() == "FP":
                continue

            doc_id = row.get("doc_id", "").strip()
            text = row["sentence"].strip()
            start = int(row["start_char"])
            end = int(row["end_char"])
            label = row.get("pred_label", "").strip()
            is_corrected = bool(row.get("ERROR", "").strip())

            if not text or not label:
                continue
            key = (doc_id, text)
            entry = [start, end, label]
            if is_corrected:
                dev_grouped[key].append(entry)
            else:
                train_grouped[key].append(entry)

    def write_jsonl(grouped, output_path):
        with open(output_path, "w", encoding="utf-8") as fout:
            for (doc_id, text), ents in grouped.items():
                unique = sorted({tuple(e) for e in ents}, key=lambda x: x[0])
                obj = {"doc_id": doc_id, "text": text, "ents": unique}
                fout.write(json.dumps(obj, ensure_ascii=False) + "\n")

    write_jsonl(train_grouped, train_jsonl)
    write_jsonl(dev_grouped, dev_jsonl)


def extract_to_csv(input_dir, output_csv):
    nlp = spacy.load("D:\\faks\\fri-fu\\diploma\\aplikacija\\output\\model-last")
    if "parser" not in nlp.pipe_names and "sentencizer" not in nlp.pipe_names:
        nlp.add_pipe("sentencizer")
    nlp.max_length = 4000000
    fields = ["doc_id", "sentence", "entity_text", "start_char", "end_char", "pred_label"]
    with open(output_csv, "w", encoding="utf-8", newline="") as fout:
        writer = csv.writer(fout)
        writer.writerow(fields)
        for path in Path(input_dir).glob("*.*"):
            doc_id = path.stem
            text = path.read_text(encoding="utf-8", errors="ignore")
            doc = nlp(text)
            for ent in doc.ents:
                raw_sent = ent.sent.text
                stripped = raw_sent.strip()
                # koliko znakov smo na začetku pobrisali?
                leading = len(raw_sent) - len(raw_sent.lstrip())
                # zdaj rel. offset prilagodi:
                rel_start = ent.start_char - ent.sent.start_char - leading
                rel_end   = ent.end_char   - ent.sent.start_char - leading
                writer.writerow([doc_id, stripped, ent.text, rel_start, rel_end, ent.label_])
    print(f"Extracted entities to CSV: {output_csv}")


def merge_jsonl(input_path, output_path):
    grouped = defaultdict(list)

    # Preberi vse vrstice in grupiraj po (doc_id, text)
    with open(input_path, "r", encoding="utf-8") as fin:
        for line in fin:
            if not line.strip():
                continue
            obj = json.loads(line)
            key = (obj.get("doc_id", ""), obj["text"])
            grouped[key].extend(obj["ents"])

    # Shrani združene (odstrani duplikate entitet, če želiš)
    with open(output_path, "w", encoding="utf-8") as fout:
        for (doc_id, text), ents in grouped.items():
            # Odstrani duplikate, če se ponavljajo [start, end, label]
            unique_ents = sorted({tuple(ent) for ent in ents}, key=lambda x: x[0])
            obj = {
                "doc_id": doc_id,
                "text": text,
                "ents": [list(e) for e in unique_ents]
            }
            fout.write(json.dumps(obj, ensure_ascii=False) + "\n")

# Primer uporabe:
# merge_jsonl("input.jsonl", "output_merged.jsonl")

# python your_script.py csv_to_jsonl --input_csv error_log3.csv --output_jsonl train_data.jsonl

# def csv_to_jsonl(input_csv, output_jsonl):
#     grouped = defaultdict(list)
#     with open(input_csv, encoding="utf-8") as fin:
#         reader = csv.DictReader(fin)
#         for row in reader:
#             text = row["sentence"].strip()
#             start = int(row["start_char"])
#             end = int(row["end_char"])
#             label = row.get("gold_label", row.get("pred_label", "")).strip()
#             doc_id = row.get("doc_id", "")
#             if not text or not label:
#                 continue
#             grouped[(doc_id, text)].append([start, end, label])

#     with open(output_jsonl, "w", encoding="utf-8") as fout:
#         for (doc_id, text), ents in grouped.items():
#             # sort and dedupe ents
#             unique = sorted({(s, e, l) for s, e, l in ents}, key=lambda x: x[0])
#             json_obj = {"doc_id": doc_id, "text": text, "ents": [[s, e, l] for s, e, l in unique]}
#             fout.write(json.dumps(json_obj, ensure_ascii=False) + "\n")
#     print(f"Converted CSV to JSONL: {output_jsonl}")

def main():
    parser = argparse.ArgumentParser(description="Extract NER or convert CSV to JSONL")
    sub = parser.add_subparsers(dest="command")

    p1 = sub.add_parser("extract_csv", help="Extract entities to CSV")

    p2 = sub.add_parser("csv_to_jsonl", help="Convert corrected CSV to JSONL")
    p2.add_argument("--input_csv", required=True, help="Path to corrected CSV")
    p2.add_argument("--output_jsonl", required=True, help="Path to output JSONL")

    p3 = sub.add_parser("xlsx_to_train_dev", help="Združi več JSONL v enega")

    p4 = sub.add_parser("merge_jsonl", help="Merge JSONL files into one")
    p4.add_argument("--input_jsonl", required=True, help="Path to input jsonl file")
    p4.add_argument("--output_jsonl", required=True, help="Path to output JSONL")

    args = parser.parse_args()
    if args.command == "extract_csv":
        extract_to_csv("D:\\faks\\fri-fu\\diploma\\aplikacija\\24ur_articles\\1-sklop", "errorlog9.csv")
    elif args.command == "csv_to_jsonl":
        csv_to_train_dev("error_log3.csv", "train_data.jsonl", "dev_data.jsonl")
        print("Generated train_data.jsonl and dev_data.jsonl.")
        #csv_to_jsonl(args.input_csv, args.output_jsonl)
    elif args.command == "xlsx_to_train_dev":
        xlsx_to_train_dev("D:\\faks\\fri-fu\\diploma\\aplikacija\\EXCEL\\četrtiposkuspopravljen.xlsx", "train_data5.jsonl", "dev_data5.jsonl")
    elif args.command == "merge_jsonl":
        merge_jsonl(args.input_jsonl, args.output_jsonl)
        print(f"Merged JSONL saved to {args.output_jsonl}")
        

if __name__ == "__main__":
    main()
