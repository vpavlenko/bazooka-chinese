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
# - every sentence is translated using Yandex.Translate, including pinyin (ALERT: yandex has wrong pinyin)
# (yandex can be replaced by google translate which has a document mode as well)
# (although Google doesn't give pinyin in this mode)
# - the translation is aligned to the source using TsinghuaAligner
# - every word has a CEDICT article attached (maybe use pinyin to filter CEDICT articles)
#
# output format: JSON files, one per chapter
#
# alternatives:
# machine translation can be done by clause, not by sentence. translation itself
# will be less precise, but the alignment will be more precise
#
# why do we require a certain version of Python? tested on Python 3.7
# maybe HanLP only supports 3.7 for now
#
# TODO:
# - run TsinghuaAligner or pick another aligner
# - design a schema
# - implement everything without a pinyin
# - test with eyes

import pprint
import re
from typing import List

import bs4
import hanlp

try:
    from typing import TypedDict  # >=3.8
except ImportError:
    from mypy_extensions import TypedDict  # <=3.7


ENGLISH_PARAGRAPHS_OFFSET = 11


class Chapter(TypedDict):
    title_cn: str
    title_en: str
    paragraphs: List[str]


# Let's design schema of a single paragraph.
example_cn = '墙上的每一寸空间都被书架盖住了。每个书架有六层，几乎碰到天花板。'
example_en_translation = 'Every inch of wall space is covered by a bookcase. Each bookcase has six shelves, going almost to the ceiling.'
hanlp_output = {
  "sentences": [
    "墙上的每一寸空间都被书架盖住了。",
    "每个书架有六层，几乎碰到天花板。"
  ],
  "tokens": [
    ["墙", "上", "的", "每", "一", "寸", "空间", "都", "被", "书架", "盖住", "了", "。"],
    ["每", "个", "书架", "有", "六", "层", "，", "几乎", "碰到", "天花板", "。"]
  ],
  "part_of_speech_tags": [
    ["NN", "LC", "DEG", "DT", "CD", "M", "NN", "AD", "LB", "NN", "VV", "AS", "PU"],
    ["DT", "M", "NN", "VE", "CD", "M", "PU", "AD", "VV", "NN", "PU"]
  ]
}
cn_clauses = [
  ["墙上的每一寸空间都被书架盖住了。",],
  ["每个书架有六层，",
   "几乎碰到天花板。"],
]
yandex_translation = [
    ["Every inch of the wall was covered with bookshelves."],
    ["qiáng shàng de měi yī cùn kōngjiān dū bèi shūjià gàizhù liǎo."],
]
# clauses, yandex.translation, alignment
# cedict


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
            break
    return result[1:]


def map_chapters_to_english_translation():
    soup = bs4.BeautifulSoup(open('hpmor_en.html').read(), "html.parser")
    english_paragraphs = soup.find_all('p')

    # won't work for chapters 2-...
    english_paragraphs[ENGLISH_PARAGRAPHS_OFFSET + line_number].prettify()

    

# pprint.pprint(get_chinese_chapters(2))


tokenizer = hanlp.load('CTB6_CONVSEG')
tagger = hanlp.load(hanlp.pretrained.pos.CTB5_POS_RNN_FASTTEXT_ZH)

pipeline = hanlp.pipeline() \
    .append(hanlp.utils.rules.split_sentence, output_key='sentences') \
    .append(tokenizer, output_key='tokens') \
    .append(tagger, output_key='part_of_speech_tags')

example_cn = '墙上的每一寸空间都被书架盖住了。每个书架有六层，几乎碰到天花板。'
print(pipeline(example_cn))
