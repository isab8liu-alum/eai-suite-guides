#!/usr/bin/env python3
"""
Redact personal information (names and emails) from screenshots using pytesseract OCR.
Targets: Isabelle Liu, Matt Elliott, and their email addresses/usernames.
"""

import os
import re
import sys
import pytesseract
from PIL import Image, ImageDraw

# Folder with images to process
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "aai_workshop_images")

# Terms to redact (case-insensitive matching)
REDACT_PATTERNS = [
    r'\bisabelle\b',
    r'\biliu\b',
    r'\biliu@',
    r'isabelle\.liu',
    r'isabelle_liu',
    r'i\.liu',
    r'\belliott\b',
    r'\bmelliott\b',
    r'matt\.elliott',
    r'matt_elliott',
    r'm\.elliott',
    r'isabelleliu',
    r'mattelliott',
    r'[a-z\.]+@amd\.com',
    r'[a-z\.]+@advanced',
]

compiled_patterns = [re.compile(p, re.IGNORECASE) for p in REDACT_PATTERNS]

PADDING = 4  # extra pixels around each box


def should_redact(text: str) -> bool:
    for pat in compiled_patterns:
        if pat.search(text):
            return True
    return False


def redact_image(path: str) -> tuple:
    img = Image.open(path).convert("RGB")

    # Get word-level bounding boxes
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    n_boxes = len(data['text'])
    redactions = []
    boxes_to_redact = set()

    # Single-word matches
    for i in range(n_boxes):
        word = data['text'][i].strip()
        if not word:
            continue
        conf = int(data['conf'][i])
        if conf < 0:
            continue
        if should_redact(word):
            boxes_to_redact.add(i)
            redactions.append(word)

    # Two-word combination check (e.g. "Isabelle Liu" spanning two tokens)
    for i in range(n_boxes - 1):
        w1 = data['text'][i].strip()
        w2 = data['text'][i + 1].strip()
        if not w1 or not w2:
            continue
        if (data['block_num'][i] == data['block_num'][i + 1] and
                data['line_num'][i] == data['line_num'][i + 1]):
            combined = f"{w1} {w2}"
            if should_redact(combined):
                boxes_to_redact.add(i)
                boxes_to_redact.add(i + 1)
                if combined not in redactions:
                    redactions.append(combined)

    draw = ImageDraw.Draw(img)
    for idx in boxes_to_redact:
        x = max(0, data['left'][idx] - PADDING)
        y = max(0, data['top'][idx] - PADDING)
        w = data['width'][idx] + 2 * PADDING
        h = data['height'][idx] + 2 * PADDING
        draw.rectangle([x, y, x + w, y + h], fill=(30, 30, 30))

    img.save(path)
    return len(boxes_to_redact), redactions


def main():
    files = sorted(f for f in os.listdir(IMAGE_DIR) if f.lower().endswith('.png'))
    print(f"Processing {len(files)} images in {IMAGE_DIR}\n")

    total_redactions = 0
    summary = []

    for fname in files:
        fpath = os.path.join(IMAGE_DIR, fname)
        try:
            count, tokens = redact_image(fpath)
            if count > 0:
                print(f"  [REDACTED {count} regions] {fname}: {tokens}")
                total_redactions += count
                summary.append((fname, tokens))
            else:
                print(f"  [clean] {fname}")
        except Exception as e:
            print(f"  [ERROR] {fname}: {e}", file=sys.stderr)

    print(f"\nDone. Total redacted regions: {total_redactions}")
    if summary:
        print("\nFiles with redactions:")
        for fname, tokens in summary:
            print(f"  {fname}: {tokens}")


if __name__ == "__main__":
    main()
