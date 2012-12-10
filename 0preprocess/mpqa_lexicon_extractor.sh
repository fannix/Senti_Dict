f=../MPQA_lexicon/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff
grep negative $f  | grep -o "word1=\w\+" |cut -b7- > negative.txt
grep positive $f  | grep -o "word1=\w\+" |cut -b7- > positive.txt
