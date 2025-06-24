
import spacy
from pathlib import Path

nlp = spacy.load("D:\\faks\\fri-fu\\diploma\\aplikacija\\output\\model-last")
if "parser" not in nlp.pipe_names and "sentencizer" not in nlp.pipe_names:
    nlp.add_pipe("sentencizer")
nlp.max_length = 4000000
fields = ["doc_id", "sentence", "entity_text", "start_char", "end_char", "pred_label"]

#for path in Path("D:\\faks\\fri-fu\\diploma\\aplikacija\\24ur_articles\\1-sklop").glob("*.*"):
path="D:\\faks\\fri-fu\\diploma\\aplikacija\\24ur_articles\\1-sklop\\0_Belgijski_minister__EU_bi_morala_Trumpa_udariti_ta.txt"
text = path.read_text(encoding="utf-8", errors="ignore")
doc = nlp(text)
for ent in doc.ents:
    print(f"{ent.text}, {ent.label_}")
        

