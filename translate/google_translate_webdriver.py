"""
Translate sentiment lexicon using selenium
"""
from selenium import webdriver
from selenium.webdriver.common import keys
import sys
import time


def translate():
    """
    Obtain English from the clipboard and translate them into Chinese
    """
    driver = webdriver.Firefox()
    base_url = "http://translate.google.cn/"
    driver.get(base_url + "/?hl=en#en|zh-CN|")
    driver.find_element_by_id("source").clear()
    #driver.find_element_by_id("source").send_keys("".join(words)) #don't do that, too slow
    driver.find_element_by_id("source").send_keys(keys.Keys.COMMAND + "v")
    #driver.find_element_by_id("gt-submit").click()
    i = 0
    while i < 10 and len(driver.find_element_by_id("result_box").text) < 3:
        time.sleep(1)
        i += 1
    print driver.find_element_by_id("result_box").text.encode("utf-8")
    driver.quit()

if __name__ == "__main__":
    translate()
