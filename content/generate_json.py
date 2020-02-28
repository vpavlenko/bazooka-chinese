import re
from collections import Counter
import json

from parse_dictionary import get_translation
from align_paragraphs import english_paragraphs
ch1_alignment = open("ch1_alignment.txt").readlines()
english_tokenized = [line.strip().split() for line in open("english_tokenized.txt").readlines()]

CHAPTERS_TO_PROCESS = 1
NEWCHAPTER = 'NEWCHAPTER\n'
ENGLISH_PARAGRAPHS_OFFSET = 11

segmented_lines = open('segmented_book.txt').readlines()
PUNCTUATION = "！？｡。＂＃＄％＆＇（）＊-＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."

current_chapter = 1

line_counter = 0
while current_chapter <= CHAPTERS_TO_PROCESS:
    chapter_lines = []
    while segmented_lines[line_counter] != NEWCHAPTER:
        chapter_lines.append(segmented_lines[line_counter])
        line_counter += 1
    line_counter += 1

    c = Counter()
    for line in chapter_lines:
        words = re.sub(rf'[{PUNCTUATION}]+', ' ', line).split()
        c.update(words)

    lines_translated = []

    for line_number, line in enumerate(chapter_lines):
        # print(f'{ch1_alignment[line_number]=}')
        # print(f'{line=}')
        # print(f'{english_tokenized[line_number]=}')
        alignment_line = ch1_alignment[line_number].strip()
        ch1_arr = {}
        if alignment_line:
            ch1_arr = {int(pair.split("-")[0]): int(pair.split("-")[1]) for pair in alignment_line.split(" ")}
        used_alignment_tokens = set()
        tokens = []
        line = line[:-1] + ' '
        for char_number, character in enumerate(line.split()):
            if character in PUNCTUATION:
                tokens.append(('punctuation', character))
            else:
                translation = get_translation(character)
                aligned_english_word = ''
                # if for word index we have something in alignment - add it
                if char_number in ch1_arr:
                    # print(f'{line_number=}')
                    # print(f'{english_tokenized[line_number]=}')
                    # print(f'{char_number=}')
                    # print(f'{ch1_arr[char_number]=}')
                    # print(f'{english_tokenized[line_number][ch1_arr[char_number]]=}')
                    if english_tokenized[line_number] and english_tokenized[line_number][ch1_arr[char_number]] not in used_alignment_tokens:
                        aligned_english_word = english_tokenized[line_number][ch1_arr[char_number]]
                        used_alignment_tokens.add(english_tokenized[line_number][ch1_arr[char_number]])
                if not translation:
                    print(f'ZERO-LENGTH TRANSLATION: {word=}')
                if translation[0] == '*':
                    translation = ' '.join([get_translation(c) for c in word])
                    tokens.append(('translation_characters', translation, aligned_english_word))
                else:
                    tokens.append(('translation_word', translation, aligned_english_word))

        lines_translated.append({
            'chinese_source': line,
            'translation': tokens,
            'english_source': english_paragraphs[ENGLISH_PARAGRAPHS_OFFSET + line_number].prettify()
        })

    current_chapter += 1

    chapter_json = {
        'lines': lines_translated,
        'frequencies': c.most_common(),
    }

    print('''import { Chapter } from "./types";

export const CHAPTER = ''', end='')
    print(json.dumps(chapter_json, indent=2, sort_keys=True, ensure_ascii=False))
