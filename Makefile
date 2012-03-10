default: all

all: preprocess

preprocess: MPQA_lexicon
	python 0preprocess/mpqa_lexicon_extractor.py > 0preprocess/mpqa_pos_neg_words.txt
	grep positive 0preprocess/mpqa_pos_neg_words.txt |cut -f1 |sort |uniq > 0preprocess/positive.txt
	grep negative 0preprocess/mpqa_pos_neg_words.txt |cut -f1 |sort |uniq > 0preprocess/negative.txt

direct_translate: 0preprocess
	#python translate/google_translate_webdriver.py 0preprocess/positive.txt > 1direct_translation/positive.txt
	#python translate/google_translate_webdriver.py 0preprocess/negative.txt > 1direct_translation/negative.txt

stat: 0preprocess 1direct_translation
	wc -l 0preprocess/positive.txt 0preprocess/negative.txt 
	wc -l 1direct_translation/positive.txt 1direct_translation/negative.txt
	sort 1direct_translation/positive.txt |uniq | wc -l
	sort 1direct_translation/negative.txt |uniq | wc -l
