import re

CLAUSE_BOUNDARY = r'[，。？]'

# We need to resegment Chinese source, so that all names are a single token.
# What are possible methods of Chinese segmentation?
# 霍格沃茨 (Hogwarts) should be a single token.
# Also: 米勒娃·麦格 (Minerva McGonagall), 迈克 (Michael)
#
# Also we want to preserve chapter titles.
# We're gonna use hanlp for segmentation. We can also add a POS tagger to
# highlight Chinese words. Also, machine translation can give us 

paragraphs = open('ch1_chinese_src.txt').readlines()
for paragraph in paragraphs:
    print(*re.split(CLAUSE_BOUNDARY, paragraph), sep='\n')
    print()
