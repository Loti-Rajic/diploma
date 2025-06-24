import spacy
from spacy.tokens import DocBin
import json

nlp = spacy.blank("sl")
doc_bin = DocBin()

with open("D:\\faks\\fri-fu\\diploma\\aplikacija\\TRAINING\\dev_data5.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            eg = json.loads(line)
        except Exception as e:
            print(f"Napaka v vrstici {i}: {e}")
            continue
        doc = nlp.make_doc(eg["text"])
        ents = []
        seen_tokens = set()
        for start, end, label in eg["ents"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                print(f"Warning: Failed to create span for: {eg['text'][start:end]!r} ({start}, {end}, {label}) in line {i}")
                continue
            # Preveri prekrivanje
            span_token_idxs = set(range(span.start, span.end))
            if seen_tokens & span_token_idxs:
                print(f"Warning: Overlapping span skipped in line {i}: {span.text}")
                continue
            seen_tokens.update(span_token_idxs)
            ents.append(span)
        doc.ents = ents
        doc_bin.add(doc)

doc_bin.to_disk("dev_data5.spacy")
