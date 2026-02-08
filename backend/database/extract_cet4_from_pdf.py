#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract CET-4 vocabulary from PDF and update word_libraries.json.
"""

import json
import os
import re
from typing import List, Dict

from PyPDF2 import PdfReader


PDF_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "CET-4.pdf"))
OUTPUT_WORDS_PATH = os.path.join(os.path.dirname(__file__), "cet4_words_from_pdf.json")
LIBRARIES_PATH = os.path.join(os.path.dirname(__file__), "word_libraries.json")


POS_PATTERN = re.compile(r"^([a-zA-Z./]+)\s+(.*)$")


def _extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    parts = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text:
            parts.append(text)
    return "\n".join(parts)


def _parse_entries(text: str) -> List[Dict]:
    # Remove headers
    text = text.replace("序号单词 注音 释义", " ")
    text = re.sub(r"\s+", " ", text).strip()

    # Match: index + word + phonetic + definition (up to next index)
    pattern = re.compile(
        r"(?:^|\s)(\d{1,4})\s*([A-Za-z][A-Za-z\-]*)\s+([^\s]+)\s+(.*?)(?=\s+\d{1,4}\s*[A-Za-z][A-Za-z\-]*\s+[^\s]+\s+|$)",
        re.DOTALL,
    )

    results: List[Dict] = []
    seen = set()

    for _idx, word, phonetic, definition in pattern.findall(text):
        word_norm = word.strip()
        if not word_norm:
            continue
        key = word_norm.lower()
        if key in seen:
            continue
        seen.add(key)

        definition = definition.strip()
        part_of_speech = ""
        english_definition = ""

        pos_match = POS_PATTERN.match(definition)
        if pos_match:
            pos_token = pos_match.group(1).strip()
            rest = pos_match.group(2).strip()
            if "." in pos_token:
                part_of_speech = pos_token
                definition = rest

        results.append(
            {
                "word": word_norm,
                "phonetic": phonetic.strip(),
                "part_of_speech": part_of_speech,
                "definition": definition,
                "english_definition": english_definition,
                "difficulty": 2,
            }
        )

    return results


def main() -> None:
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    text = _extract_text_from_pdf(PDF_PATH)
    words = _parse_entries(text)

    with open(OUTPUT_WORDS_PATH, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

    with open(LIBRARIES_PATH, "r", encoding="utf-8") as f:
        libraries = json.load(f)

    libraries["words"]["cet4"] = words
    for lib in libraries.get("libraries", []):
        if lib.get("category") == "cet4":
            lib["total_words"] = len(words)

    with open(LIBRARIES_PATH, "w", encoding="utf-8") as f:
        json.dump(libraries, f, ensure_ascii=False, indent=2)

    print(f"CET-4 extracted words: {len(words)}")
    print(f"Saved words to: {OUTPUT_WORDS_PATH}")
    print(f"Updated libraries: {LIBRARIES_PATH}")


if __name__ == "__main__":
    main()
