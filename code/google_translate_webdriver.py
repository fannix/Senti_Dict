from selenium import webdriver

driver = webdriver.Firefox()
driver.implicitly_wait(30)
base_url = "http://translate.google.cn/"
driver.get(base_url + "/?hl=en#en|zh-CN|")
driver.find_element_by_id("source").clear()
driver.find_element_by_id("source").send_keys("hello\nworld\ngood bye")
driver.find_element_by_id("gt-submit").click()
print driver.find_element_by_id("result_box").text
driver.quit()
