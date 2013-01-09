import sys
from sklearn.metrics import classification_report, zero_one_score


def read_dict(pos_dict, neg_dict):
    """Read positive and negative dictionary
    """
    di = {}
    li = open(pos_dict).readlines()
    for e in li:
        e = e.strip()
        di[e] = 1

    li2 = open(neg_dict).readlines()
    for e in li2:
        e = e.strip()
        di[e] = -1

    return di


def predict(text, di):
    """Predict text polarity with dictionary di
    """
    li = text.split()
    score = 0
    wordset = set(li)
    for e in wordset:
        if e in di:
            score += di[e]
            print e, di[e],

    print score

    if score < 0:
        polarity = -1
    else:
        polarity = 1

    return polarity


def predict_with_negation_rule(text, senti_di, negation_di):
    """Adding negation dictionary and rules
    """
    li = text.split()
    score = 0

    true_score = li[0]

    text_len = len(li)
    for i, e in enumerate(li):
        sign = 1
        if e in senti_di:
            for j in range(max(0, i-2), min(text_len, i+2)):
                if li[j] in negation_di:
                    sign = -1
                    break
            score += sign * senti_di[e]
            print e, senti_di[e],

    print "score", score, true_score

    if score < 0:
        polarity = -1
    else:
        polarity = 1

    return polarity

if __name__ == "__main__":
    context_di = read_dict("positive_submit.txt", "negative_submit.txt")
    #translate_di = read_dict("positive.txt", "negative.txt")
    #translate_di = read_dict("multi_positive.txt", "multi_negative.txt")
    #translate_di = read_dict("non_stem_positive.txt", "non_stem_negative.txt")
    translate_di = read_dict("single_positive.txt", "single_negative.txt")

    negation_di = set()
    with open("chinese_negator.txt") as f:
        for line in f:
            negation_di.add(line.strip())

    context_answer = []
    translate_answer = []
    true_answer = []
    all_lines = sys.stdin.readlines()

    for line in all_lines:
        line = line.strip()
        li = line.split()
        true_answer.append(int(li[0]))
        text = " ".join(li[0:])
        #context_answer.append(predict(text, context_di))
        #translate_answer.append(predict(text, translate_di))

        translate_answer.append(predict_with_negation_rule(text, translate_di, negation_di))
        context_answer.append(predict_with_negation_rule(text, context_di, negation_di))

    print classification_report(true_answer, translate_answer)
    print zero_one_score(true_answer, translate_answer)

    print classification_report(true_answer, context_answer)
    print zero_one_score(true_answer, context_answer)
