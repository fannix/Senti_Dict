#!/usr/bin/python

"""
Generating bigrams for words in English sentiment lexicon.

The ngrams service is provided by "N-Gram Frequency Tables for Wikipedia and Gutenberg"
"""

import requests
import sys

def read_entries():
    """
    Read entries from the lexicon
    """
    li = []
    for line in sys.stdin:
        word = line.strip()
        li.append(word)

    return li


def generate_bigrams(word):
    """
    Generate bigrams for a word
    """

    url = "https://api.datamarket.azure.com/Data.ashx/winwaed/ngram/v1/bigram_gutn?"
    url += "$filter=word1%20eq%20%27" + word + "%27&$top=2000&$format=json"
    user_id = "bd94a2a3-d5df-41cb-ab8f-a4c1b57629e0"
    password = "0TZrVm6OMTSsrs9+tv6ky4J98dE1RGRq4W0iv61d3ow="
    response = requests.get(url, auth=(user_id, password))

    print response
    json_content = response.json['d']['results']

    for item in json_content:
        print item['word1'], item['word2'], item['count']


if __name__ == "__main__":
    words = read_entries()

    for a_word in words:
        generate_bigrams(a_word)
