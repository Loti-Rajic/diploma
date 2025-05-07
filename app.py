import os
import json
import spacy
import fitz
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from spacy.tokens import Span
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY

# Naloži model
nlp = spacy.load("sl_core_news_trf")
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
def anonymize_entities(doc, label_map):
    with doc.retokenize() as retok:
        for ent in doc.ents:
            label = label_map.get(ent.label_, None)
            if label:
                retok.merge(ent, attrs={"LEMMA": label, "ENT_TYPE": ent.label_})

    tokens = []
    for token in doc:
        if token.ent_type_ in label_map:
            tokens.append(label_map[token.ent_type_])
        else:
            tokens.append(token.text)
        tokens.append(token.whitespace_)
    return "".join(tokens)

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_txt(text, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

def read_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def write_docx(text, out_path):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(out_path)

def read_pdf(path):
    doc = fitz.open(path)
    return "".join(page.get_text() for page in doc)

def write_pdf(text, out_path):
    """
    Zapiše polno poravnan (justified) PDF z enakimi marginami na levi in desni strani.
    """
    # nastavi dokument z 50 pt marginami
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    # Pripravi slog: DejaVuSans, velikost 12, leading 14, justified
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Justify',
        fontName='DejaVuSans',
        fontSize=12,
        leading=14,
        alignment=TA_JUSTIFY
    ))

    flowables = []
    # Razdeli na odstavke (prazna vrstica = nov odstavek)
    for para in text.split('\n\n'):
        # nadomesti enojne prelome z <br/> za vstavke znotraj istega odstavka
        clean = para.replace('\n', '<br/>').strip()
        if not clean:
            continue
        flowables.append(Paragraph(clean, styles['Justify']))
        flowables.append(Spacer(1, 12))  # razmik med odstavki

    # Ustvari PDF
    doc.build(flowables)

def process_file(file_path, output_dir, label_map):
    ext = os.path.splitext(file_path)[1].lower()
    # 1) Preberi
    if ext == ".txt":
        text = read_txt(file_path)
    elif ext == ".docx":
        text = read_docx(file_path)
    elif ext == ".pdf":
        text = read_pdf(file_path)
    else:
        raise ValueError(f"Nepodprt tip datoteke: {ext}")

    # 2) Anonimiziraj
    doc = nlp(text)
    anonymized = anonymize_entities(doc, label_map)

    # 3) Pripravi izhodno pot in zapiši isti format
    base = os.path.splitext(os.path.basename(file_path))[0]
    out_path = os.path.join(output_dir, f"{base}_anonimizirano{ext}")

    if ext == ".txt":
        write_txt(anonymized, out_path)
    elif ext == ".docx":
        write_docx(anonymized, out_path)
    elif ext == ".pdf":
        write_pdf(anonymized, out_path)

    return out_path

if __name__ == "__main__":
    # Vhodna mapa
    directory = "D:\\faks\\fri-fu\\diploma\\aplikacija\\testno_gradivo"
    # Izhodna podmapa
    output_dir = os.path.join(directory, "anonimizirano")
    os.makedirs(output_dir, exist_ok=True)

    # Naloži konfiguracijo
    with open("config.json", encoding="utf-8") as c:
        label_map = json.load(c)

    # Iteriraj čez vse datoteke
    for fname in os.listdir(directory):
        in_path = os.path.join(directory, fname)
        if os.path.isdir(in_path) or fname == "config.json":
            continue
        try:
            saved = process_file(in_path, output_dir, label_map)
            print(f"Obdelana datoteka shranjena kot {saved}")
        except Exception as e:
            print(f"Napaka pri {fname}: {e}")
