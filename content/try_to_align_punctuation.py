import re

import bs4

START = 0

chinese = open("segmented_book.txt").readlines()[START : START + 100]

CHINESE_PUNCTUATION = (
    "[！？｡。＂＃＄％＆＇（）＊-＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–‘’‛“”„‟…‧﹏.]"
)
ENGLISH_PUNCTUATION = '[!?.":,()]'

soup = bs4.BeautifulSoup(open("hpmor_en.html").read(), "html.parser")

english = soup.find_all("p")[START + 11 : START + 100 + 11]

for c, e in list(zip(chinese, english)):
    c_punct = (
        "".join(re.findall(CHINESE_PUNCTUATION, c))
        .replace("。", ".")
        .replace("…", "...")
        .replace("，", ",")
        .replace("“", '"')
        .replace("”", '"')
        .replace("：", ":")
        .replace("？", "?")
        .replace("！", "!")
    )

    e_punct = "".join(re.findall(ENGLISH_PUNCTUATION, e.prettify()))

    print(c_punct)
    print(e_punct)
    print(c_punct == e_punct)
    print()
