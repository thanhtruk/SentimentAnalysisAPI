import json
import re

with open("data/field_keywords.txt", "r", encoding="utf-8") as f:
    keyword_dict = json.load(f)


def detect_fields_in_text(text: str) -> tuple:
    matched_fields = {}

    for field, keywords in keyword_dict.items():
        contained_keywords = []
        for kw in keywords:
            pattern = re.escape(kw.lower())
            if re.search(rf"\b{pattern}\b", text):
                contained_keywords.append(kw)
        if contained_keywords:
            matched_fields[field] = contained_keywords

    sorted_matched = sorted(
        matched_fields.items(), key=lambda item: len(item[1]), reverse=True
    )

    if sorted_matched:
        best_field, matched_keywords = sorted_matched[0]
        return best_field, matched_keywords
    else:
        return "Khác", []