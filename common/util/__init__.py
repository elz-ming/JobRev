## Helper functions
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


## This function will automatically run click load more in the url attached below
## After no more button, we need manually inspect the source code and copy the html to txt file
def jobstreet_web_scraper():
    service = Service("/Users/nickytan/Development/chromedriver")
    driver = webdriver.Chrome(service=service)

    url = "https://www.jobstreet.com.my/en/companies/browse-reviews"

    driver.get(url)
    time.sleep(5)

    close_button = driver.find_element(By.CLASS_NAME, "gwCwc3YZYufjgIcBtu0l")
    close_button.click()

    count = 0
    while True:
        try:
            next_button = driver.find_element(By.CLASS_NAME, "Gk2xjdpX_s0S3hsfi__X")
            next_button.click()
            print("Next Button Clicked!")
            count += 1
            print(count)
            time.sleep(2)
        except:
            print("No more next button")
            print(count)
            break



