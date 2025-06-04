import streamlit as st
import json
import spacy
from spacy.tokens import Span
from io import StringIO
from pdfminer.high_level import extract_text
from docx import Document

nlp = spacy.load("sl_core_news_trf")
with open("config.json", encoding="utf-8") as c:
    label_map = json.load(c)

def read_txt(buffer):
    return buffer.getvalue()

def read_docx(buffer):
    doc = Document(buffer)
    return "\n".join(p.text for p in doc.paragraphs)

def read_pdf(buffer):
    return extract_text(buffer)

def anonymize(text, selected_labels):
    doc = nlp(text)
    lm = {k: v for k, v in label_map.items() if k in selected_labels}
    with doc.retokenize() as retok:
        for ent in doc.ents:
            if ent.label_ in lm:
                retok.merge(ent, attrs={"LEMMA": lm[ent.label_], "ENT_TYPE": ent.label_})
    out = []
    for token in doc:
        if token.ent_type_ in lm:
            out.append(lm[token.ent_type_])
        else:
            out.append(token.text)
        out.append(token.whitespace_)
    return "".join(out)

st.title("Anonimizator uradnih dokumentov")

all_labels = list(label_map.keys())
selected = st.multiselect(
    "Izberite entitete za anonimizacijo",
    options=all_labels,
    default=["PER", "LOC", "ORG"]
)

uploaded = st.file_uploader(
    "Naložite dokument (.txt, .docx, .pdf)",
    type=["txt", "docx", "pdf"]
)

if uploaded is not None and selected:
    ext = uploaded.name.split('.')[-1].lower()
    if ext == "txt":
        text = read_txt(StringIO(uploaded.getvalue().decode("utf-8")))
    elif ext == "docx":
        text = read_docx(uploaded)
    elif ext == "pdf":
        text = read_pdf(uploaded)
    else:
        st.error("Nepodprt format")
        st.stop()

    with st.expander("Prikaz izvornega besedila", expanded=True):
        st.text_area("Izvorno besedilo", text, height=300)

    anonymized = anonymize(text, selected)

    st.subheader("Anonimizirano besedilo")
    st.text_area("", anonymized, height=300)
    st.download_button(
        label="Prenesite anonimizirano datoteko",
        data=anonymized.encode("utf-8"),
        file_name=f"{uploaded.name.rsplit('.',1)[0]}_anonimizirano.{ext}",
        mime="text/plain" if ext=="txt" else (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            if ext=="docx" else "application/pdf"
        )
    )
