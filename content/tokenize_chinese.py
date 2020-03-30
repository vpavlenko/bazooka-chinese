# input: hpmor_cn_nonsegmented.txt
#
# downsides of using this input: lost bold/italic formatting
# (as presented in https://drive.google.com/drive/folders/0B3KWNcRzg3ErUEdHRFAxVjIzX1k)
# alternative: parse epub from https://drive.google.com/drive/folders/0B3KWNcRzg3ErUEdHRFAxVjIzX1k
# non-critical for now. preserving the formatting is hard because it needs to
# be merged into the segmenter and translation phase.
#
# output:
# - split by chapters with chapter titles avaiable in Chinese/English
# - every line (=paragraph) mapped to the English translation
# - every line is split into senteces and segmented using HanLP with POS tagger info
# - every sentence is additionally split into clauses to improve the alignment
# - every clause is translated using Yandex.Translate, including pinyin
# - the translation is aligned to the source using TsinghuaAligner
# - every word has a CEDICT article attached
#
# output format: JSON files, one per chapter

import re
from typing import List

try:
    from typing import TypedDict  # >=3.8
except ImportError:
    from mypy_extensions import TypedDict  # <=3.7


class Chapter(TypedDict):
    title: str
    paragraphs: List[str]


def get_chinese_chapters(num_chapters: int) -> List[Chapter]:
    lines = open("hpmor_cn_nonsegmented.txt").readlines()
    result: List[Chapter] = []
    paragraphs_for_new_chapter: List[str] = []
    previous_chapter_title = "SENTINEL"
    for line in lines:
        line = line.strip()
        match = re.match("第.+章[：: ](.+)", line)
        if match:
            result.append(
                {
                    "title": previous_chapter_title,
                    "paragraphs": paragraphs_for_new_chapter,
                }
            )
            paragraphs_for_new_chapter = []
            previous_chapter_title = match.group(1)
        elif line:
            paragraphs_for_new_chapter.append(line)
        if len(result) >= num_chapters + 1:
            return result[1:]
    return result[1:]


print(get_chinese_chapters(1))
