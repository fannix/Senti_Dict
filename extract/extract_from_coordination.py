#encoding: utf-8
"""
Extract from coordination phrase
"""
import sys
import string


def output(word):
    """
    Only output correct sentiment word and filter others
    """
    for e in word:
        if e in string.ascii_letters:
            return
    if len(word) < 2 or len(word) > 6:
        return

    print word.encode("utf-8")

def extract(phrase):
    words = phrase.split()
    #4 characters idioms
    if len(words) ==1 and len(phrase) == 4:
        output(phrase)
    #if len(words) == 3 and (words[1] == u'，' or words[1] == u'和'):
    for i, e in enumerate(words):
        if e == u'，' or e == u'和':
            output("".join(words[:i]))
            output("".join(words[i+1:]))

if __name__ == "__main__":
    seg_file = sys.argv[1]
    seg_phrase_li = []
    with open(seg_file) as f:
        for line in f:
            seg_phrase_li.append(line.strip().decode("utf-8"))

    for phrase in seg_phrase_li:
        extract(phrase)
