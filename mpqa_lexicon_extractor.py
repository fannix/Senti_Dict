"""
A script to extract sentiment words from MPQA Lexicon

The inconsistency in the original data have been fixed, but no information is lost.
"""

dict_file = "MPQA_lexicon/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff"

lines = open(dict_file).readlines()
for aline in lines:
    arecord = aline.split()
    record_type, record_len, word, pos, stemmed, polarity = \
            [e.split("=")[1] for e in arecord]

    if record_type == "strongsubj" and polarity != "neutral":
        print word + "\t" + polarity
