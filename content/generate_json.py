import re
from collections import Counter
import json

from parse_dictionary import get_translation
from align_paragraphs import english_paragraphs


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
        tokens = []
        line = line[:-1] + ' '
        word = ''
        for character in line:
            if character in PUNCTUATION:
                tokens.append(('punctuation', character))
                word = ''
            elif character == ' ':
                if word:
                    translation = get_translation(word)
                    if not translation:
                        print(f'ZERO-LENGTH TRANSLATION: {word=}')
                    if translation[0] == '*':
                        translation = ' '.join([get_translation(c) for c in word])
                        tokens.append(('translation_characters', translation))
                    else:
                        tokens.append(('translation_word', translation))
                    word = ''
            else:
                word += character

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

export const CHAPTER: Chapter = ''', end='')
    print(json.dumps(chapter_json, indent=2, sort_keys=True, ensure_ascii=False))
