from selenium import webdriver
import time

browser = webdriver.Chrome()

browser.get("https://hz.lianjia.com/zufang/")
input_str = browser.find_element_by_name("keyword")
input_str.send_keys("瑷颐湾")
time.sleep(1)
input_str.clear()
input_str.send_keys("越秀")
btn = browser.find_element_by_class_name("act-search")
btn.click()
time.sleep(5)
browser.close()
