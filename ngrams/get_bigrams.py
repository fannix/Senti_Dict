"""
Obtain bigrams from Microsoft Web N-Gram Service

The following corpora are provided

['bing-anchor/jun09/1', 'bing-anchor/jun09/2', 'bing-anchor/jun09/3', 'bing-anchor/jun09/4',
 'bing-body/jun09/1', 'bing-body/jun09/2', 'bing-body/jun09/3',
 'bing-title/jun09/1', 'bing-title/jun09/2', 'bing-title/jun09/3', 'bing-title/jun09/4',
 'bing-query/jun09/1', 'bing-query/jun09/2', 'bing-query/jun09/3',
 'bing-title/apr10/1', 'bing-title/apr10/2', 'bing-title/apr10/3', 'bing-title/apr10/4', 'bing-title/apr10/5',
 'bing-anchor/apr10/1', 'bing-anchor/apr10/2', 'bing-anchor/apr10/3', 'bing-anchor/apr10/4', 'bing-anchor/apr10/5',
 'bing-body/apr10/1', 'bing-body/apr10/2', 'bing-body/apr10/3', 'bing-body/apr10/4', 'bing-body/apr10/5']
 """

from MicrosoftNgram import LookupService
import time
import os.path

def get_bigrams(polarity, lookup):
    """
    Get bigrams from online services

    polarity: string type, "positive" or "negative"
    lookup: On-line service
    """
    total = 1000
    word_li = open("0preprocess/%s.txt" % polarity).readlines()
    for word in word_li:
        word = word.strip()
        file_name = "2bigrams/%s/%s.txt" % (polarity, word)
        if os.path.exists(file_name):
            continue
        print word
        with open(file_name, 'w') as f:
            for next_word, prob in lookup.Generate(word, total):
                f.write(word + " " + next_word + '\n')
        time.sleep(0.5)

if __name__ == "__main__":
    lookup = LookupService(token="d4cbbdfb-e5e2-4b32-983b-a37d0029c65c")
    lookup = LookupService(model = "bing-title/apr10/2", token="d4cbbdfb-e5e2-4b32-983b-a37d0029c65c")
    get_bigrams("positive", lookup)
    get_bigrams("negative", lookup)
