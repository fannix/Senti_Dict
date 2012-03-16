"""
Extract from direct translation
"""
import sys
import string

def extract(line):
    word = line.strip().decode("utf-8")
    if word[0] in string.ascii_letters:
        return
    if len(word) < 2:
        return
    print word.encode("utf-8")


if __name__ == "__main__":
    for line in sys.stdin:
        extract(line)
