default: all

all: preprocess

preprocess: MPQA_lexicon
	python 0preprocess/mpqa_lexicon_extractor.py > 0preprocess/mpqa_pos_neg_words.txt
	grep positive 0preprocess/mpqa_pos_neg_words.txt |cut -f1 |sort |uniq > 0preprocess/positive.txt
	grep negative 0preprocess/mpqa_pos_neg_words.txt |cut -f1 |sort |uniq > 0preprocess/negative.txt

direct_translate: 0preprocess
	#python translate/google_translate_webdriver.py 0preprocess/positive.txt > 1direct_translation/positive.txt
	#python translate/google_translate_webdriver.py 0preprocess/negative.txt > 1direct_translation/negative.txt

dictionary_translate: 0preprocess
	python translate/dictionary_translate.py

stat: 0preprocess 1direct_translation
	wc -l 0preprocess/positive.txt 0preprocess/negative.txt 
	wc -l 1direct_translation/positive.txt 1direct_translation/negative.txt
	sort 1direct_translation/positive.txt |uniq | wc -l
	sort 1direct_translation/negative.txt |uniq | wc -l
	sort 1direct_translation/non_stem_positive.txt |uniq | wc -l
	sort 1direct_translation/non_stem_negative.txt |uniq | wc -l
	wc -l 1direct_translation/single_positive.txt
	wc -l 1direct_translation/single_negative.txt
	sort 1direct_translation/single_positive.txt |uniq | wc -l
	sort 1direct_translation/single_negative.txt |uniq | wc -l
	sort 1direct_translation/multi_positive.txt |uniq | wc -l
	sort 1direct_translation/multi_negative.txt |uniq | wc -l
	#cut -f1 bilingual_dictionary/ldc_ec_dict.1.0.utf8.txt 0preprocess/negative.txt | sort | uniq -d | wc -l
	#cut -f1 bilingual_dictionary/ldc_ec_dict.1.0.utf8.txt 0preprocess/positive.txt | sort | uniq -d | wc -l
	sort 7extraction/positive/*.txt | uniq | wc -l
	sort 7extraction/negative/*.txt | uniq | wc -l

bigrams: 0preprocess
	mkdir -p 2bigrams/positive
	mkdir -p 2bigrams/negative

goole_translate: 0preprocess
	for x in 2bigrams/positive/*.txt; do pbcopy < $x; python translate/google_translate_webdriver.py > 3google_translation/positive/$(basename $x); done

punctuation: 0preprocess
	mkdir 5punctuation
	sed s/$/./ < 0preprocess/positive.txt > 5punctuation/positive.txt
	sed s/$/./ < 0preprocess/negative.txt > 5punctuation/negative.txt

coordinate: 0preprocess
	mkdir coordinate_phrase
	export LANG="C" #Otherwise sort program does not handle Chinese properly
	paste 1direct_translation/positive.txt 0preprocess/positive.txt |sort > 6coordinate_phrase/positive.txt
	paste 1direct_translation/negative.txt 0preprocess/negative.txt |sort > 6coordinate_phrase/negative.txt
	join -t "	" 6coordinate_phrase/negative.txt 6coordinate_phrase/negative.txt > 6coordinate_phrase/negative_join.txt
	join -t "	" 6coordinate_phrase/positive.txt 6coordinate_phrase/positive.txt > 6coordinate_phrase/positive_join.txt
	python coordinate_phrase/gen_coordiate_phrase.py < 6coordinate_phrase/positive_join.txt > 6coordinate_phrase/positive_coordinate_phrase.txt
	python coordinate_phrase/gen_coordiate_phrase.py < 6coordinate_phrase/negative_join.txt > 6coordinate_phrase/negative_coordinate_phrase.txt

extract: 0preprocess
	python extract/extract_from_direct_translation.py< 1direct_translation/positive.txt > 7extraction/positive/direct.txt
	python extract/extract_from_direct_translation.py< 1direct_translation/negative.txt > 7extraction/negative/direct.txt
	python extract/extract_from_punctuations.py< 5punctuation/positive_translation.txt > 7extraction/positive/punctuation.txt
	python extract/extract_from_punctuations.py< 5punctuation/negative_translation.txt > 7extraction/negative/punctuation.txt
