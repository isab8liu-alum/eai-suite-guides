#!/usr/bin/env python3
"""
Redact PII from screenshots using Claude vision API.
Finds bounding boxes for personal info (names, emails) and blacks them out.
"""

import os
import sys
import base64
import json
import re
from PIL import Image, ImageDraw
import anthropic

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "workshop7-images")
PADDING = 4

client = anthropic.Anthropic()


def encode_image(path: str) -> tuple[str, str]:
    """Return (base64_data, media_type)."""
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return data, "image/png"


def find_pii_regions(image_path: str, img_width: int, img_height: int) -> list[dict]:
    """
    Ask Claude to find PII bounding boxes in the image.
    Returns list of {x, y, w, h} dicts (pixel coords).
    """
    b64, media_type = encode_image(image_path)

    prompt = f"""This screenshot is {img_width}x{img_height} pixels.

Carefully examine this image for any personal information such as:
- Real person names (first name, last name, or full name of actual people)
- Email addresses (anything with @)
- Usernames that look like real names
- Any AMD employee names or email addresses

For EACH region containing personal info, provide the bounding box in pixel coordinates.
The image is {img_width} pixels wide and {img_height} pixels tall.

Return ONLY a JSON array. Each element must have these integer fields:
  "x": left pixel coordinate
  "y": top pixel coordinate
  "w": width in pixels
  "h": height in pixels
  "text": the text being redacted (for logging)

If there is NO personal information, return an empty array: []

Do not include any explanation. Return only valid JSON."""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    raw = response.content[0].text.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    raw = raw.strip()

    try:
        regions = json.loads(raw)
        return regions if isinstance(regions, list) else []
    except json.JSONDecodeError:
        print(f"    [WARN] Could not parse response: {raw[:200]}", file=sys.stderr)
        return []


def redact_image(image_path: str) -> tuple[int, list[str]]:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    regions = find_pii_regions(image_path, w, h)

    if not regions:
        return 0, []

    draw = ImageDraw.Draw(img)
    texts = []
    for r in regions:
        x = max(0, int(r.get("x", 0)) - PADDING)
        y = max(0, int(r.get("y", 0)) - PADDING)
        rw = int(r.get("w", 0)) + 2 * PADDING
        rh = int(r.get("h", 0)) + 2 * PADDING
        draw.rectangle([x, y, x + rw, y + rh], fill=(30, 30, 30))
        texts.append(r.get("text", "?"))

    img.save(image_path)
    return len(regions), texts


def main():
    all_images = []
    for root, dirs, files in os.walk(IMAGE_DIR):
        for fname in sorted(files):
            if fname.lower().endswith(".png"):
                all_images.append(os.path.join(root, fname))

    print(f"Processing {len(all_images)} images in {IMAGE_DIR}\n")

    total_redactions = 0
    summary = []

    for fpath in all_images:
        rel = os.path.relpath(fpath, IMAGE_DIR)
        try:
            count, tokens = redact_image(fpath)
            if count > 0:
                print(f"  [REDACTED {count} regions] {rel}: {tokens}")
                total_redactions += count
                summary.append((rel, tokens))
            else:
                print(f"  [clean] {rel}")
        except Exception as e:
            print(f"  [ERROR] {rel}: {e}", file=sys.stderr)

    print(f"\nDone. Total redacted regions: {total_redactions}")
    if summary:
        print("\nFiles with redactions:")
        for fname, tokens in summary:
            print(f"  {fname}: {tokens}")


if __name__ == "__main__":
    main()
