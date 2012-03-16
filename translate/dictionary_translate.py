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

def extend(translation_li, new_translations):
    #We do some filtering here since
    #not all translations are useful
    translation_candidates = [e.decode("utf-8") for e in new_translations]
    legal_translations = [e.encode('utf-8') for e in translation_candidates\
            if (e.find(u'.') == -1
                and len(e) > 1
                and len(e) < 6)]
    translation_li.extend(legal_translations)


def translate(single_dict, word_list, multiple_translation, stem):
    """
    Translate translation mapping dictinary

    Parameters
    ----------
    single_dict: mapping dictionary
    word_list: English polarity lexicon
    multiple_translation: Allow a word to translate to multiple words
    stem: True means using stemming

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
                extend(translation_li, translation[1:-1].split('/'))
            else:
                extend(translation_li, [translation])
        elif stemmed in single_dict and stem:
            stem_translation = single_dict[stemmed]
            if multiple_translation:
                extend(translation_li, stem_translation[1:-1].split('/'))
            else:
                extend(translation_li, [stem_translation])
        else:
            print e
    return translation_li

if __name__ == "__main__":
    single_dict, multiple_dict = load_dict()
    pos_file_name = "0preprocess/positive.txt"
    neg_file_name = "0preprocess/negative.txt"
    pos_li = [e.strip() for e in open(pos_file_name).readlines()]
    neg_li = [e.strip() for e in open(neg_file_name).readlines()]

    pos_non_stem_name = "1direct_translation/non_stem_positive.txt"
    neg_non_stem_name = "1direct_translation/non_stem_negative.txt"
    pos_non_stem_li = translate(single_dict, pos_li, False, False)
    neg_non_stem_li = translate(single_dict, neg_li, False, False)
    open(pos_non_stem_name, 'w').write("\n".join(pos_non_stem_li))
    open(neg_non_stem_name, 'w').write("\n".join(neg_non_stem_li))

    pos_single_name = "1direct_translation/single_positive.txt"
    neg_single_name = "1direct_translation/single_negative.txt"
    pos_single_li = translate(single_dict, pos_li, False, True)
    neg_single_li = translate(single_dict, neg_li, False, True)
    open(pos_single_name, 'w').write("\n".join(pos_single_li))
    open(neg_single_name, 'w').write("\n".join(neg_single_li))

    pos_multiple_name = "1direct_translation/multi_positive.txt"
    neg_multiple_name = "1direct_translation/multi_negative.txt"
    pos_multiple_li = translate(multiple_dict, pos_li, True, True)
    neg_multiple_li = translate(multiple_dict, neg_li, True, True)
    open(pos_multiple_name, 'w').write("\n".join(pos_multiple_li))
    open(neg_multiple_name, 'w').write("\n".join(neg_multiple_li))

