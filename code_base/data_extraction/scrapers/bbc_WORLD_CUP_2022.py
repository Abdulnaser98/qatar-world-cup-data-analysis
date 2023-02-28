from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from tqdm import tqdm


# get the chrome driver for the bbc website
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# contains the links of the bbc news regarding the qatar world cup 2022
article_links = []
article_dates = []
titles = []
main_contents = []





def main():
    # extract the links
    extract_links()
    # remove links that are irrelevant to our task , like sound links and etc
    remove_unwanted_links()
    # extract the relevant article data , like date , title , main content
    extract_article_data()




def extract_links():
    print("Extracting the links: ")

    url = "https://www.bbc.com/news/topics/cwlw3xz0ze8t?page="
    # there is a total number of 20 pages regarding Qatar in the bbc media outlet
    for page in range(1, 20):
        print("Inspecting the {} to get the articles".format(page))
        driver.get(url + str(page))
        article_links = driver.find_elements("xpath","//main[contains(@id, 'main-content')]//ul/li/div/div/div/div/div/a[@href]")
        for link in article_links:
            article_links.append(link.get_attribute("href"))

    print("The links are succefually extracted")



def remove_unwanted_links():
    print("Removing irrelevant links: ")
    unwanted_links = pd.read_csv("/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/article_links/bbc_unwanted_links.csv")
    article_links = [x for x in article_links if x not in unwanted_links]
    print("Irrelevant links are removed")


def extract_article_data():
    print("Extracting the articles data: ")
    for link in tqdm(article_links):
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
    df.to_csv("bbc_qatar_data.csv", index=False)


main()



"""
# Instantiating the Chrome browser object using webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
article_dates = []
authors = []
titles= []
head_titles = []
main_contents = []
# specify the URL of the website you want to scrape
url = "https://www.bbc.com/news/topics/cwlw3xz0ze8t?page="

# specify the number of pages you want to scrape
num_pages = 19
#num_pages + 1
for page in range(18, 20):
    print(page)
    driver.get(url + str(page))
    article_links = driver.find_elements("xpath","//main[contains(@id, 'main-content')]//ul/li/div/div/div/div/div/a[@href]")
    for link in article_links:
        links.append(link.get_attribute("href"))

unwanted_links = ["https://www.bbc.com/news/live/uk-wales-politics-63907455", "https://www.bbc.com/sounds/play/m001fm0l",
                  "https://www.bbc.com/sport/live/football/63687157","https://www.bbc.com/sounds/play/w3ct312k",
                  "https://www.bbc.com/sounds/play/w3ct3172","https://www.bbc.com/sounds/play/m0017chj",
                  "https://www.bbc.com/sounds/play/p0byy9sr","https://www.bbc.com/sounds/play/p0bypw3j",
                  "https://www.bbc.com/sport/cricket/59590568", "https://www.bbc.com/weather/features/31605227",
                  "https://www.bbc.com/sounds/play/p0767590", "https://www.bbc.com/news/world-us-canada-39732845"
                  "https://www.bbc.com/programmes/p065bxrj", "https://www.bbc.com/news/world-us-canada-39732845",
                  "https://www.bbc.com/sport/football/51072079","https://www.bbc.com/programmes/p065bxrj",
                  "https://www.bbc.com/programmes/p065bx16", "https://www.bbc.com/sounds/play/p062r06l",
                  "https://www.bbc.com/sounds/play/b08x2zf5", "https://www.bbc.com/sounds/play/p0577kby",
                  "https://www.bbc.com/sounds/play/p0558xzg", "https://www.bbc.com/sounds/play/p0550j8m",
                  "https://www.bbc.com/sounds/play/p0524hr4", "https://www.bbc.com/programmes/p051n6q4",
                  "https://www.bbc.com/sounds/play/b04jmrnm"
                ]
counter = 0
for link in tqdm(links):
# | //article/div//p/b | //article/div//p/span
    if link not in unwanted_links:
        driver.get(link)
        counter = counter + 1
        print("Counter: ")
        print(counter)
        time.sleep(3)
        print("link")
        print(link)
        time.sleep(3)
        title = driver.find_element("xpath", "//article//h1[contains(@id,'main-heading') or contains(@id,'page')]").text
        date =  driver.find_element("xpath", "//article//time").text
        main_content_elm = driver.find_elements("xpath", "//article/div//p")
        main_content = ""
        for p in main_content_elm:
            main_content = main_content + " ." + p.text

        article_dates.append(date)
        titles.append(title)
        main_contents.append(main_content)



data = {'date': article_dates, 'title': titles, 'main_content': main_contents }
df = pd.DataFrame(data)
df.to_csv("bbc_data__very_neu_5.csv", index=False)



#all_bbc_data.to_csv("all_bbc_qatar_data.csv")



"""