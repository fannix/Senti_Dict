default: all

all: preprocess

preprocess: MPQA_lexicon
	python 0preprocess/mpqa_lexicon_extractor.py > 0preprocess/mpqa_pos_neg_words.txt
