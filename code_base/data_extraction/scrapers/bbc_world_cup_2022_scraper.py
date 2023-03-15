from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from tqdm import tqdm


# get the chrome driver for the bbc website
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# Path to the raw data folder
path_to_raw_data_folder = "./code_base/data_extraction/raw_data/"

# Path to the folder , where the links that were extracted from the news media outlets are saved
path_to_article_links_folder = "./code_base/data_extraction/article_links/"


# contains the links of the bbc news regarding the qatar world cup 2022
article_dates = []
titles = []
main_contents = []



def bbc_web_scraping_main():
    # extract the links
    links = extract_links()
    # remove links that are irrelevant to our task , like sound links and etc
    filtered_links = remove_unwanted_links(links)
    # extract the relevant article data , like date , title , main content
    extract_article_data(filtered_links)
    # save the data in the raw data folder
    save_data()




def extract_links():
    print("Extracting the links: ")
    article_links_temp = []
    url = "https://www.bbc.com/news/topics/cwlw3xz0ze8t?page="
    # there is a total number of 20 pages regarding Qatar in the bbc media outlet
    for page in range(1, 20):
        print("Inspecting the {} to get the articles".format(page))
        driver.get(url + str(page))
        article_links = driver.find_elements("xpath","//main[contains(@id, 'main-content')]//ul/li/div/div/div/div/div/a[@href]")
        for link in article_links:
            article_links_temp.append(link.get_attribute("href"))

    df = pd.DataFrame(article_links,columns =['link'])
    df.to_csv(path_to_article_links_folder + 'bbc_articles_links.csv')


    print("The links are succefually extracted")
    return article_links_temp


def remove_unwanted_links(links):
    print("Removing irrelevant links: ")
    unwanted_links = pd.read_csv("./code_base/data_extraction/bbc_unwanted_links.csv")
    article_links_temp = [x for x in links if x not in unwanted_links]
    print("Irrelevant links are removed")
    return article_links_temp


def extract_article_data(links):
    print("Extracting the articles data: ")
    for link in tqdm(links):
        driver.get(link)
        time.sleep(6)

        date = extract_article_date()
        title = extract_article_title()
        main_content = extract_main_containt()

        article_dates.append(date)
        titles.append(title)
        main_contents.append(main_content)
    print("The data for all relevant articles are extracted succefually ")

def extract_article_date():
    date =  driver.find_element("xpath", "//article//time").text
    return date

def extract_article_title():
    title = driver.find_element("xpath", "//article//h1[contains(@id,'main-heading') or contains(@id,'page')]").text
    return title

def extract_main_containt():
    main_content_elm = driver.find_elements("xpath", "//article/div//p")
    main_content = ""
    for p in main_content_elm:
        main_content = main_content + " ." + p.text
    return main_content


def save_data():
    data = {'date': article_dates, 'title': titles, 'main_content': main_contents }
    df = pd.DataFrame(data)
    df.to_csv(path_to_raw_data_folder + "bbc_qatar_data.csv", index=False)






