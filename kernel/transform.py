"""Transform the English document to Chinese document using English-Chinese bilingual sentiment dictionary.
"""

def get_word(line):
    """get a word from one line of the sentiment lexicon file
    """
    li = line.strip().split()
    for word in li:
        if word[:5] == "word1":
            return word.split("=")[-1]


def load_sentiment_lexicon(file_name):
    """load the sentiment lexicon
    """
    lex = []
    with open(file_name) as f:
        for line in f:
            lex.append(get_word(line))

    return lex

def load_bilingual_lexicon(file_name):
    """load the bilingual dictionary of Chinese and English
    """
    bi_lex = {}
    with open(file_name) as f:
        for line in f:
            #print line
            en_word, ch_translation = line.strip().split('\t')
            bi_lex[en_word] = ch_translation.replace("/", " ")

    return bi_lex

def transform(text_file, sa_lex, bi_lex):
    """Read an English text file, and output the Chinese translation of the English sentiment words
    """
    with open(text_file) as f:
        for line in f:
            li = line.strip().split()
            label = li[0]
            word_li = set(li[1:])
            print label,
            for word in word_li:
                if word in sa_lex and word in bi_lex:
                    print bi_lex[word],
            print

if __name__ == "__main__":
    senti_lex = "/Users/mxf/paper_codes/senti_dict/MPQA_lexicon/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff"
    bi_lex = "/Users/mxf/paper_codes/senti_dict/bilingual_dictionary/ldc_ec_dict.1.0.utf8.txt"

    sa_lex = load_sentiment_lexicon(senti_lex)
    bi_lex = load_bilingual_lexicon(bi_lex)

    text_file  = "ntcir.en"
    transform(text_file, sa_lex, bi_lex)
