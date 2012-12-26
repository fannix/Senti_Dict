"""
Generate bigrams from google ngrams corpus
"""

from heapq import heappush, heapreplace
import sys
import gzip
from  collections import defaultdict
from itertools import groupby


def group_by_prefix(words):
    """group the sentiment words by prefix 2-chars.

        words that less than 2 (inclusive) chars are ignored.
    """
    di = defaultdict(list)
    for a_word in words:
        if len(a_word) <= 2:
            continue
        di[a_word[:2]].append(a_word)

    return di

def count_bigram(group):
    """count the total occurences of the bigram
    """
    total = 0
    for line in group:
        total += int(line.split()[-1])

    return total


if __name__ == "__main__":
    words = []
    for line in sys.stdin:
        words.append(line.strip())
        prefix_to_words = group_by_prefix(words)


    for prefix in prefix_to_words:
        #print prefix, prefix_to_words[prefix]
        ngram_file = "google-ngrams/googlebooks-eng-all-2gram-20120701-%s.gz" % prefix
        #print ngram_file
        word_set = set(prefix_to_words[prefix])
        word_heap = defaultdict(list)

        with gzip.open(ngram_file) as f:
            for bigram, group in groupby(f, key=lambda line: " ".join(line.split()[:2])):
                prev_word, next_word = bigram.split()
                if prev_word not in word_set:
                    continue

                bigram_count = count_bigram(group)
                a_heap = word_heap[prev_word]
                top_k = 3000
                new_item = (bigram_count, next_word)
                if len(a_heap) < top_k:
                    heappush(a_heap, new_item)
                else:
                    if new_item[0] > a_heap[0][0]:
                        heapreplace(a_heap, new_item)

        for word in word_set:
            items = sorted(word_heap[word], reverse=True)

            for a_item in items:
                print "\t".join((word, a_item[1], str(a_item[0])))
