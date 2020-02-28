from align_paragraphs import english_paragraphs
from nltk.tokenize.stanford import StanfordTokenizer

tokenizer = StanfordTokenizer()

english_paragraphs = english_paragraphs[11:]

# for i in range(87):
    # print(' '.join(tokenizer.tokenize(english_paragraphs[i])))

# print(str(english_paragraphs[0])))
for l in range(0, 87):
    print(' '.join([s for s in tokenizer.tokenize(english_paragraphs[l].prettify()) if s[0] != '<']))

