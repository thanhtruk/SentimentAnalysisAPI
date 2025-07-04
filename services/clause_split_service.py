import re
from py_vncorenlp import VnCoreNLP

import os

absolute_path = os.path.abspath('vncorenlp')
model = VnCoreNLP(save_dir=absolute_path)


def split_text_into_sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]

def split_clauses(words, pos_tags, min_clause_len=2):
    length = len(words)
    splits = []
    clauses = []

    conjunction_tags = {"C"}  # liên từ

    prev_split = 0
    i = 1

    while i < length:
        split_now = False

        # --- Rule 1: split tại liên từ nếu trước đó có động/tính từ ---
        if pos_tags[i] in conjunction_tags:
            has_verb_before = any(pos_tags[j] in {"V", "A"} for j in range(prev_split, i))
            if has_verb_before and (i - prev_split) >= min_clause_len:
                splits.append(i)
                clause = words[prev_split:i]
                clauses.append(" ".join(clause))
                prev_split = i
                i += 1
                continue  # skip Rule 3 nếu đã split

        # --- Rule 2: split tại dấu phẩy nếu hai bên đều có noun + verb ---
        if (words[i] == "," or (pos_tags[i] == "CH" and words[i] == ",")) and i < length - 1:
            left_noun = any(pos_tags[j] in {"N", "Np", "Nu", "P"} for j in range(prev_split, i))
            left_verb = any(pos_tags[j] in {"V", "A"} for j in range(prev_split, i))
            right_noun = any(pos_tags[j] in {"N", "Np", "Nu", "P"} for j in range(i + 1, length))
            right_verb = any(pos_tags[j] in {"V", "A"} for j in range(i + 1, length))
            if left_noun and left_verb and right_noun and right_verb and (i - prev_split) >= min_clause_len:
                splits.append(i)
                clause = words[prev_split:i]
                clauses.append(" ".join(clause))
                prev_split = i
                i += 1
                continue

        i += 1

    # Thêm phần còn lại
    final_clause = words[prev_split:]
    if len(final_clause) >= min_clause_len:
        clauses.append(" ".join(final_clause))

    return clauses


def process_text(text):
    sentences = split_text_into_sentences(text)
    all_clauses = []

    for sentence in sentences:
        try:
            annotations = model.annotate_text(sentence)
        except Exception as e:
            print(f"Lỗi khi phân tích câu: {sentence}")
            print(e)
        print(annotations)
        if not isinstance(annotations, dict):
            print("not dic")
            continue

        for sent_id, token_list in annotations.items():
            words = [tok["wordForm"] for tok in token_list]
            print(words)
            pos_tags = [tok["posTag"] for tok in token_list]
            print(pos_tags)

        clauses = split_clauses(words, pos_tags)
        if clauses:
            all_clauses.extend(clauses)
        else:
            all_clauses.append(" ".join(words))

    return all_clauses
