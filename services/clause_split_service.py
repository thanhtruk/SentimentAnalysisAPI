import re
from py_vncorenlp import VnCoreNLP

import os

absolute_path = os.path.abspath('vncorenlp')
model = VnCoreNLP(save_dir=absolute_path)


def split_text_into_sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]


# def split_clauses(words, pos_tags, min_clause_len=2):
#     splits = []
#     length = len(words)
#
#     conjunction_tags = {"C", "E"}  # Rule 1 & 2: mở rộng để bao gồm "vì" (E)
#     punctuation_tags = {"CH"}
#
#     # Rule 1 Split at conjunction if preceded by a verb
#     for i in range(1, length):
#         if pos_tags[i] in conjunction_tags:
#             # check có clause nào được chia chưa
#             if splits:
#                 has_verb_before = any(pos_tags[j] in {"V", "A"} for j in range(splits[-1], i))
#             else:
#                 has_verb_before = any(pos_tags[j] in {"V", "A"} for j in range(0, i))
#             if has_verb_before:
#                 splits.append(i)
#
#     # Rule 2 Do not split if conjunction is at the beginning
#     if 0 in splits:
#         splits.remove(0)
#
#     # Rule 3 Split at comma if both sides have noun + verb/adj
#     for i in range(1, length - 1):
#         if words[i] == "," or (pos_tags[i] == "CH" and words[i] == ","):
#             # check có clause nào được chia chưa
#             if splits:
#                 left_noun = any(pos_tags[j] in {"N", "Np", "Nu", "P"} for j in range(splits[-1], i))
#                 left_verb = any(pos_tags[j] in {"V", "A"} for j in range(splits[-1], i))
#             else:
#                 left_noun = any(pos_tags[j] in {"N", "Np", "Nu", "P"} for j in range(0, i))
#                 left_verb = any(pos_tags[j] in {"V", "A"} for j in range(0, i))
#             right_noun = any(pos_tags[j] in {"N", "Np", "Nu", "P"} for j in range(i + 1, length))
#             right_verb = any(pos_tags[j] in {"V", "A"} for j in range(i + 1, length))
#             if left_noun and left_verb and right_noun and right_verb:
#                 splits.append(i)
#     print(splits)
#
#     # Remove duplicates and sort
#     splits = sorted(set(splits))
#
#     # Apply splitting
#     clauses = []
#     prev = 0
#     for split in splits:
#         if split - prev >= min_clause_len:
#             clause = words[prev:split]
#             clauses.append(" ".join(clause))
#             prev = split
#     final_clause = words[prev:]
#     if len(final_clause) >= min_clause_len:
#         clauses.append(" ".join(final_clause))
#
#     return clauses


def split_clauses(words, pos_tags, min_clause_len=2):
    length = len(words)
    splits = []
    clauses = []

    conjunction_tags = {"C", "E"}  # liên từ
    punctuation_tags = {"CH"}  # dấu câu

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
        annotations = model.annotate_text(sentence)
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
