default: all

all: preprocess

preprocess: MPQA_lexicon
	python 0preprocess/mpqa_lexicon_extractor.py > 0preprocess/mpqa_pos_neg_words.txt
	grep positive 0preprocess/mpqa_pos_neg_words.txt |cut -f1 |sort |uniq > 0preprocess/positive.txt
	grep negative 0preprocess/mpqa_pos_neg_words.txt |cut -f1 |sort |uniq > 0preprocess/negative.txt
