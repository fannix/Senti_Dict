"""
Translate sentiment lexicon using selenium
"""
from selenium import webdriver
import sys

def translate(words):
    """
    Translate English words into Chinese

    Parameters
    ----------
    words: English words
    """
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    base_url = "http://translate.google.cn/"
    driver.get(base_url + "/?hl=en#en|zh-CN|")
    driver.find_element_by_id("source").clear()
    driver.find_element_by_id("source").send_keys("".join(words))
    driver.find_element_by_id("gt-submit").click()
    print driver.find_element_by_id("result_box").text
    driver.quit()

if __name__ == "__main__":
    lexicon_file = sys.argv[1]
    #words = open(lexicon_file).readlines()[:100]
    words = open(lexicon_file).readlines()
    print words
    translate(words)
