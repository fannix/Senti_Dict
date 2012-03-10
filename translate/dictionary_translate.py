"""
Translate using bilingual dictionaries
"""
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
def load_dict():
    """
    Load an English to Chinese dictionary

    Returns
    -------
    single_dict: One to one mapping
    multiple_dict: One to many mapping
    """
    dict_file = "bilingual_dictionary/ldc_ec_dict.1.0.utf8.txt"
    single_dict = {}
    multiple_dict = {}
    #Stemmed form have to be in the dictionary for inflection form
    f = open(dict_file)
    for line in f:
        #print line
        en_word, all_translation = line.strip().split('\t')
        multiple_dict[en_word] = all_translation
        stemmed = stemmer.stem(en_word)
        if stemmed not in multiple_dict:
            multiple_dict[stemmed] = all_translation
        translation_li = all_translation[1:-1].split('/')
        single_dict[en_word] = translation_li[0]
        if stemmed not in single_dict:
            single_dict[stemmed] = translation_li[0]

    return single_dict, multiple_dict

def translate(single_dict, word_list, multiple_translation):
    """
    Translate translation mapping dictinary

    Parameters
    ----------
    single_dict: mapping dictionary
    word_list: English polarity lexicon
    multiple_translation: Allow a word to translate to multiple words

    Returns
    -------
    Translation of polarity lexicon
    """
    translation_li = []
    for e in word_list:
        stemmed = stemmer.stem(e)
        if e in single_dict:
            translation = single_dict[e]
            if multiple_translation:
                translation_li.extend(translation[1:-1].split('/'))
            else:
                translation_li.append(translation)
        elif stemmed in single_dict:
            stem_translation = single_dict[stemmed]
            if multiple_translation:
                translation_li.extend(stem_translation[1:-1].split('/'))
            else:
                translation_li.append(stem_translation)
        else:
            print e
    return translation_li

if __name__ == "__main__":
    single_dict, multiple_dict = load_dict()
    pos_file_name = "0preprocess/positive.txt"
    neg_file_name = "0preprocess/negative.txt"
    pos_li = [e.strip() for e in open(pos_file_name).readlines()]
    neg_li = [e.strip() for e in open(neg_file_name).readlines()]

    pos_single_name = "1direct_translation/single_positive.txt"
    neg_single_name = "1direct_translation/single_negative.txt"
    pos_single_li = translate(single_dict, pos_li, False)
    neg_single_li = translate(single_dict, neg_li, False)
    open(pos_single_name, 'w').write("\n".join(pos_single_li))
    open(neg_single_name, 'w').write("\n".join(neg_single_li))

    pos_multiple_name = "1direct_translation/multi_positive.txt"
    neg_multiple_name = "1direct_translation/multi_negative.txt"
    pos_multiple_li = translate(multiple_dict, pos_li, True)
    neg_multiple_li = translate(multiple_dict, neg_li, True)
    open(pos_multiple_name, 'w').write("\n".join(pos_multiple_li))
    open(neg_multiple_name, 'w').write("\n".join(neg_multiple_li))
