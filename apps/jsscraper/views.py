# ========== IMPORT-ANTS ========== #

from django.shortcuts import render

# ====

def jsscraper1():
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import pandas as pd

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    url = 'https://www.jobstreet.com.my/en/companies/browse-reviews'

    driver.get(url)

    counter = 0
    while counter < 100:
        try:
            driver.find_element(By.CLASS_NAME, 'Gk2xjdpX_s0S3hsfi__X').click()
            counter += 1
            try:
                time.sleep(0.5)
                driver.find_element(By.CLASS_NAME, 'gwCwc3YZYufjgIcBtu0l').click()
            except:
                continue
        except:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    all_company_info = soup.find_all(name="div", class_="_WfdmOZ2wLBd0x_TFyKO")

    company_list = []
    company_url_list = []
    company_rating = []

    for i in range(len(all_company_info)):
        company_list.append(all_company_info[i].find(name="a", class_="_9d6_WXgVpZWn7HaXEgs").getText())

    ## Get company jobstreet main url
    endpoint = "https://www.jobstreet.com.my"
    for i in range(len(all_company_info)):
        company_url_list.append(endpoint + all_company_info[i].find(name="a", class_="_9d6_WXgVpZWn7HaXEgs")["href"])


    for i in range(len(all_company_info)):
        company_rating.append(float(all_company_info[i].find_all(name="span", class_="j6BF91AmxWn9vS_m399j")[1].getText().split("out")[0]))

    data = {
        "company_name" : company_list,
        "company_js_url" : company_url_list,
        "company_rating" : company_rating
    }

    df = pd.DataFrame(data=data)
    
    return df

def jsscraper2(Dataframe):
    from bs4 import BeautifulSoup
    import pandas as pd
    import requests

    df = Dataframe

    five_star_list = []
    four_star_list = []
    three_star_list = []
    two_star_list = []
    one_star_list = []
    salary_rate_list = []
    recommendation_rate_list = []

    for url in df['company_js_url']:
        response = requests.get(url)
        data = response.text
        soup = BeautifulSoup(data, "html.parser")

        try:
            salary_rate = soup.find_all(name="div", class_="RL2EfHhuwPsO8xlgwG_S")[0].getText()
            salary_rate_list.append(salary_rate)
        except:
            salary_rate_list.append("No Info")

        try:
            recommendation_rate = soup.find_all(name="div", class_="RL2EfHhuwPsO8xlgwG_S")[1].getText()
            recommendation_rate_list.append(recommendation_rate)
        except:
            recommendation_rate_list.append("No Info")

        try:
            five_star = soup.find_all(name="span", class_="DCaw56gNq5O1IBoC5xcz")[0].getText()
            five_star_list.append(five_star)
        except:
            five_star_list.append("0")

        try:
            four_star = soup.find_all(name="span", class_="DCaw56gNq5O1IBoC5xcz")[1].getText()
            four_star_list.append(four_star)
        except:
            four_star_list.append("0")

        try:
            three_star = soup.find_all(name="span", class_="DCaw56gNq5O1IBoC5xcz")[2].getText()
            three_star_list.append(three_star)
        except:
            three_star_list.append("0")

        try:
            two_star = soup.find_all(name="span", class_="DCaw56gNq5O1IBoC5xcz")[3].getText()
            two_star_list.append(two_star)
        except:
            two_star_list.append("0")

        try:
            one_star =  soup.find_all(name="span", class_="DCaw56gNq5O1IBoC5xcz")[4].getText()
            one_star_list.append(one_star)
        except:
            one_star_list.append("0")

    df["five_star_rating"] = five_star_list
    df["four_star_rating"] = four_star_list
    df["three_star_rating"] = three_star_list
    df["two_star_rating"] = two_star_list
    df["one_star_rating"] = one_star_list
    df["salary_rate"] = salary_rate_list
    df["recommendation_rate"] = recommendation_rate_list
    
    return df


# ========== PUT THIS IN MAIN() ========== #




    