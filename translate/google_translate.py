"""
This is the remote control version
"""
from selenium import selenium
import unittest, time, re

class google_translate(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://translate.google.cn/")
        self.selenium.start()

    def test_google_translate(self):
        sel = self.selenium
        sel.open("/?hl=en")
        sel.type("id=source", "hello")
        sel.click("id=gt-submit")

    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
