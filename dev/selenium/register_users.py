from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

# Setup driver for Firefox
driver = webdriver.Firefox()
#driver.get("file:///home/johan/Git/TDP013/Social_Website/TDP013/index.html")
driver.get('localhost:5000/register')

for i in range(1, 10):
	print i

driver.find_element_by_id('email').send_keys('test@user.com')

