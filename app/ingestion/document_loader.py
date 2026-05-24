import logging
import pdfplumber
import docx
import pandas as pd


def load_document(path):
    if path.endswith(".pdf"):
        # Suppress noisy pdfminer/font warnings during text extraction
        loggers = ["pdfminer", "pdfminer.layout", "pdfminer.pdfparser", "fontTools"]
        prev_levels = {}
        for name in loggers:
            logger = logging.getLogger(name)
            prev_levels[name] = logger.level
            logger.setLevel(logging.ERROR)

        try:
            texts = []
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    txt = page.extract_text()
                    if txt:
                        texts.append(txt)
            return "\n".join(texts)
        finally:
            for name, lvl in prev_levels.items():
                logging.getLogger(name).setLevel(lvl)

    elif path.endswith(".docx"):
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    elif path.endswith(".txt"):
        with open(path, encoding="utf-8") as f:
            return f.read()

    elif path.endswith(".csv"):
        df = pd.read_csv(path)
        return df.to_string()

    return ""