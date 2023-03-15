# Importing the necessary modules
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from tqdm import tqdm


# Instantiating the Chrome browser object using webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# Path to the raw data folder
path_to_raw_data_folder = "./code_base/data_extraction/raw_data/"

# Path to the folder , where the links that were extracted from the news media outlets are saved
path_to_article_links_folder = "./code_base/data_extraction/article_links/"

# contains the links of the bbc news regarding the qatar world cup 2022
article_dates = []
titles = []
head_titles = []
main_contents = []



header_path = "//main[contains(@id, 'main-content-area')]//header[contains(@class, 'article-header') or contains(@class, 'gallery-header')]"
main_content_path = "//main[contains(@id, 'main-content-area')]"


def aljazerra_web_scraping_main():

    # extract the links
    links = extract_links()
    # remove links that are irrelevant to our task , like sound links and etc
    links_filtered = remove_unwanted_links(links)
    # extract the relevant article data , like date , title , main content
    extract_article_data(links_filtered)
    # save the data in the raw data folder
    save_data()


def extract_links():
    print("Extracting aljazerra articles liks: ")
    # Opening the website using the `get` method
    driver.get("https://www.aljazeera.com/qatar-world-cup-2022/")
    # Adding a time delay of 3 seconds for the page to load
    time.sleep(3)

    # extract featured articles first
    featured_articles_links = driver.find_elements("xpath","//ul[contains(@class, 'featured-articles-list')]/li//a[@href]")
    article_links = []
    print("We have {} fetaured items: ".format(len(featured_articles_links)))
    for e in featured_articles_links:
        article_links.append(e.get_attribute("href"))

    #Adding a time delay of 3 seconds for the next set of articles to load
    time.sleep(3)

    counter = 0
    while True:
        try:
            # Finding the "Show More" button element using xpath
            show_more = driver.find_element("xpath", "//button[contains(@class, 'show-more-button big-margin')]")
            # Clicking the "Show More" button using JavaScript
            driver.execute_script("arguments[0].click();", show_more)
            counter = counter +1
            print(counter)
            print("Show more button clicked")
            # Adding a time delay of 2 seconds for the next set of articles to load
            time.sleep(2)

        except:
            # If the "Show More" button is no longer present, print a message and break out of the loop
            print("No more Show more button")
            break

    # extract news feed links
    news_feed_links = driver.find_elements("xpath","//section[@id='news-feed-container']/article/div[@class='gc__content']/div[@class='gc__header-wrap']/h3[@class='gc__title']//a[@href]")
    for e in news_feed_links:
        article_links.append(e.get_attribute("href"))

    df = pd.DataFrame(article_links,columns =['link'])
    df.to_csv(path_to_article_links_folder + 'aljazerra_articles_new_links.csv')

    print("We have collected {} links".format(len(article_links)))

    return article_links




def remove_unwanted_links(links):
    print("Removing irrelevant links: ")
    unwanted_links = pd.read_csv("./code_base/data_extraction/unwanted_links/aljazerra_unwanted_links.csv")
    article_links_temp = []
    for link in links:
        if link not in unwanted_links:
            article_links_temp.append(link)
    #article_links = [x for x in article_links if x not in unwanted_links]
    print("Irrelevant links are removed")
    return article_links_temp


def extract_article_data(links):
    print("Extracting the articles data: ")
    for link in tqdm(links):
        print(link)
        driver.get(link)
        time.sleep(6)

        date = extract_article_date()
        title = extract_article_title()
        head_title = extract_head_title()
        main_content = extract_main_content()

        article_dates.append(date)
        titles.append(title)
        head_titles.append(head_title)
        main_contents.append(main_content)
    print("The data for all relevant articles are extracted succefually ")



def extract_article_date():
    date =  driver.find_element("xpath",main_content_path + "//div[contains(@class, 'article-info-block css-ti04u9') or contains(@class, 'article-info-block')]/div[contains(@class,'article-b-l')]//div[contains(@class,'date-simple css-1yjq2zp')]/span[@class='screen-reader-text']").text
    return date


def extract_article_title():
    title = driver.find_element("xpath", header_path+"/h1").text
    return title


def extract_head_title():
    try:
        head_title = driver.find_element("xpath",header_path+"//p[contains(@class, 'article__subhead css-1wt8oh6')]/em | //h2[contains(@class,'gallery-header__subhead')]").text
    except:
        head_title = ""


def extract_main_content():
    main_content_element = driver.find_elements("xpath",main_content_path+"//div[contains(@class, 'wysiwyg wysiwyg--all-content css-ibbk12') or contains(@class,'gallery-content wysiwyg wysiwyg--all-content css-ibbk12')]/p")
    main_content = ""
    for p in main_content_element:
        main_content = main_content + " ." + p.text




def save_data():
    data = {'date': article_dates,'title': titles,'head_title':head_title,'main_content': main_contents }
    df = pd.DataFrame(data)
    df.to_csv(path_to_raw_data_folder + "aljazerra_qatar_data_new.csv", index=False)
