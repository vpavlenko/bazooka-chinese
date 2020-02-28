import re


# https://regex101.com/r/vC86NV/1
PATTERN = r'^([^ ]+) ([^ ]+) \[([^]]+)] /(.+)/'


def trim_translation(word):
    word = word.split('/')[0]
    if word.startswith('to '):
        word = word[3:]
    # remove comments in (braces)
    word = re.sub('\([^)]+\)', '', word).strip()
    return word.replace(' ', '_')


d = {}
for line in open('cedict_ts.u8').readlines():
    traditional, simplified, pronunciation, translation = re.match(PATTERN, line).groups()
    translation = trim_translation(translation)
    if (simplified not in d and not translation.startswith('surname')
        and not translation.startswith('old_variant_of')
        and not translation.startswith('variant_of')
        and translation):
        d[simplified] = translation


def E(word):
    '''
    Does the translation exist?
    '''
    return word in d


def get_translation(word):
    def T(word):
        translation = f'{d[word]}'
        if len(translation) == 0:
            raise Exception(f'WORD WITH ZERO-LENGTH TRANSLATION: {word} {d[word]}')
        return {'w': word, 't': d[word]}


    if E(word):
        translation = [T(word)]
    elif '·' in word:
        translation = [{'w': word, 't': 'NAME?'}]
    elif E(word[:1]) and E(word[1:]):
        translation = [T(word[:1]), T(word[1:])]
    elif E(word[:2]) and E(word[2:]):
        translation = [T(word[:2]), T(word[2:])]
    elif E(word[:3]) and E(word[3:]):
        # Not sure we ever reach it.
        # Also may make sense to code other partitions like 1-1-1, 1-2-1.
        translation = [T(word[:3]), T(word[3:])]
    else:
        translation = [{'w': word, 't': '..'}]
    return translation
