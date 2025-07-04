import re

from services.clause_split_service import model


def split_text_into_sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]


from collections import Counter, OrderedDict


def extract_adj(text: str) -> dict:
    sentences = split_text_into_sentences(text)
    extracted_phrases = []

    for sentence in sentences:
        try:
            annotations = model.annotate_text(sentence)
        except Exception as e:
            print(f"Lỗi khi phân tích câu: {sentence}")
            print(e)
            continue

        if not isinstance(annotations, dict):
            continue

        for sent_id, token_list in annotations.items():
            current_phrase = []
            current_pos = None

            for tok in token_list:
                word = tok["wordForm"].replace("_", " ")
                pos = tok["posTag"]

                if pos in {"A"}:
                    if current_pos == pos:
                        current_phrase.append(word)
                    else:
                        if current_phrase:
                            extracted_phrases.append(" ".join(current_phrase))
                        current_phrase = [word]
                        current_pos = pos
                else:
                    if current_phrase:
                        extracted_phrases.append(" ".join(current_phrase))
                        current_phrase = []
                        current_pos = None

            if current_phrase:
                extracted_phrases.append(" ".join(current_phrase))

    freq = Counter(extracted_phrases)
    return OrderedDict(freq.most_common())
