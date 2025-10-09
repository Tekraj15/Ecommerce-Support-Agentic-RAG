"""
Loader for documents (PDF, CSV, JSON) for RAG ingestion pipeline.
"""
import os
import json
import csv
from typing import List, Dict, Any
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

class DocumentLoader:
    def __init__(self, source_dir: str):
        self.source_dir = source_dir

    def load_json(self) -> List[Dict[str, Any]]:
        """Load all JSON files from source_dir."""
        docs = []
        for fname in os.listdir(self.source_dir):
            if fname.lower().endswith('.json'):
                fpath = os.path.join(self.source_dir, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        docs.append(json.load(f))
                except Exception as e:
                    print(f"Error loading {fpath}: {e}")
        return docs

    def load_pdf(self) -> List[str]:
        """Load and extract text from all PDFs in source_dir."""
        texts = []
        if PdfReader is None:
            print("pypdf not installed. PDF loading disabled.")
            return texts
        for fname in os.listdir(self.source_dir):
            if fname.lower().endswith('.pdf'):
                fpath = os.path.join(self.source_dir, fname)
                try:
                    reader = PdfReader(fpath)
                    text = "\n".join(page.extract_text() or "" for page in reader.pages)
                    texts.append(text)
                except Exception as e:
                    print(f"Error loading {fpath}: {e}")
        return texts

    def load_csv(self) -> List[Dict[str, Any]]:
        """Load all CSV files from source_dir."""
        docs = []
        for fname in os.listdir(self.source_dir):
            if fname.lower().endswith('.csv'):
                fpath = os.path.join(self.source_dir, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        docs.extend(list(reader))
                except Exception as e:
                    print(f"Error loading {fpath}: {e}")
        return docs