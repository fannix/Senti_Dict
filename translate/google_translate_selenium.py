"""
Translate sentiment lexicon using selenium

This version support to start from the previous break point.
"""
from selenium import webdriver
from selenium.webdriver.common import keys
import sys
import time
import pygtk
pygtk.require('2.0')
import gtk

clipboard = gtk.clipboard_get()


def get_chunks(file_src):
    """get a chunk from the source file"""
    li = []
    line_per_chunk = 1000
    for line in file_src:
        li.append(line.strip())
        if len(li) == line_per_chunk:
            break

    return li

def translate():
    """
    Obtain English lines and translate them into Chinese
    """
    driver = webdriver.Firefox()
    base_url = "http://translate.google.cn/"
    driver.get(base_url + "/?hl=en#en|zh-CN|")
    driver.find_element_by_id("source").clear()
    #driver.find_element_by_id("source").send_keys("\n".join(lines))
    driver.find_element_by_id("source").send_keys(keys.Keys.CONTROL + "v")
    #driver.find_element_by_id("gt-submit").click()
    i = 0
    while i < 10 and len(driver.find_element_by_id("result_box").text) < 3:
        time.sleep(1)
        i += 1
    result =  driver.find_element_by_id("result_box").text.encode("utf-8")
    driver.quit()
    return result

if __name__ == "__main__":
    nline_stored = len(open("translated_negative.txt").readlines())
    processed = nline_stored
    with open("negative_bigrams.txt") as file_src:
        for i in range(nline_stored):
            file_src.next()

        while True:
            li = get_chunks(file_src)
            if len(li) == 0:
                break
            nresult = 0
            while True:
                clipboard.set_text('\n'.join(li))
                clipboard.store()
                result = translate()
                nresult = result.count("\n") + 1
                if len(result.strip()) != 0 and len(li) == nresult:
                    break
            print result
            processed += nresult
            print >> sys.stderr, processed
