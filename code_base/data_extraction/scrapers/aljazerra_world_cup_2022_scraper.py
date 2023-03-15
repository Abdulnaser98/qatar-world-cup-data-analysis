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
path_to_raw_data_folder = "/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/raw_data/"

# Path to the folder , where the links that were extracted from the news media outlets are saved
path_to_article_links_folder = "/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/article_links/"

# contains the links of the bbc news regarding the qatar world cup 2022
article_links = []
article_dates = []
titles = []
head_title = []
main_contents = []



header_path = "//main[contains(@id, 'main-content-area')]//header[contains(@class, 'article-header') or contains(@class, 'gallery-header')]"
main_content_path = "//main[contains(@id, 'main-content-area')]"


def aljazerra_web_scraping_main():

    # extract the links
    extract_links()
    # remove links that are irrelevant to our task , like sound links and etc
    remove_unwanted_links()
    # extract the relevant article data , like date , title , main content
    extract_article_data()
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




def remove_unwanted_links():
    print("Removing irrelevant links: ")
    unwanted_links = pd.read_csv("/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/unwanted_links/aljazerra_unwanted_links.csv")
    article_links_temp = []
    for link in article_links:
        if link not in unwanted_links:
            article_links_temp.append(link)
    article_links =  article_links_temp
    #article_links = [x for x in article_links if x not in unwanted_links]
    print("Irrelevant links are removed")


def extract_article_data():
    print("Extracting the articles data: ")
    for link in tqdm(article_links):
        driver.get(link)
        time.sleep(6)

        date = extract_article_date()
        title = extract_article_title()
        head_title = extract_head_title
        main_content = extract_main_content()

        article_dates.append(date)
        titles.append(title)
        head_title.append(head_title)
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
    df.to_csv(path_to_raw_data_folder + "aljazerra_qatar_data.csv", index=False)



"""
# Opening the website using the `get` method
driver.get("https://www.aljazeera.com/qatar-world-cup-2022/")

# Adding a time delay of 3 seconds for the page to load
time.sleep(3)

links = []

# extract featured articles first
featured_articles_links = driver.find_elements("xpath","//ul[contains(@class, 'featured-articles-list')]/li//a[@href]")

print("We have {} fetaured items: ".format(len(featured_articles_links)))
for e in featured_articles_links:
    links.append(e.get_attribute("href"))

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
    links.append(e.get_attribute("href"))


print("We have collected {} links".format(len(links)))

df = pd.DataFrame(links,columns =['link'])

df.to_csv('aljazerra_articles_new_links.csv')

"""


"""
# read the links
links = pd.read_csv('/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/aljazerra_articles_new_links.csv',sep = ',')
print("the columns are")
print(links.columns)
links = links[~links['link'].str.contains("liveblog")]


# Extract the following informations from each article date , author , title , head_title , main_content
article_dates = []
authors = []
titles= []
head_titles = []
main_contents = []

unwanted_links = ["https://www.aljazeera.com/program/between-us/2022/12/6/world-cup-inside-qatar", "https://www.aljazeera.com/sports/2022/12/6/which-teams-have-reached-the-world-cup-quarter-finals"
                  , "https://www.aljazeera.com/features/longform/2022/12/5/zhen-kitchen-a-chinese-familys-restaurant-legacy-in-doha",  "https://www.aljazeera.com/sports/2022/12/3/the-five-most-infamous-world-cup-penalty-shoot-outs",
                  "https://aljazeera.com/wc2022experience/?utm_source=www.aljazeera.com&utm_medium=website&utm_campaign=ucms", "https://www.aljazeera.com/sports/2022/11/17/football-penalty-kicks-explained", "https://www.aljazeera.com/features/longform/2022/11/7/authentic-desi-food-in-doha-the-story-of-punjab-2",
                  "https://interactive.aljazeera.com/aje/2022/qatar-football-world-cup-2022-quiz/?utm_source=www.aljazeera.com&utm_medium=website&utm_campaign=ucms","https://www.aljazeera.com/sports/2022/10/19/host-qatars-world-cup-carbon-neutral-claims-under-fire",
                  "https://www.aljazeera.com/sports/2022/10/11/fifa-world-cup-1930","https://interactive.aljazeera.com/aje/2022/visit-qatar-2022-football-world-cup/?utm_source=aljazeera.com&utm_medium=section_page&utm_campaign=world_cup_2022",
                  "https://www.aljazeera.com/program/newsfeed/2022/7/19/no-pitch-no-problem-young-senegalese-footballers-train-on-roofs", "https://interactive.aljazeera.com/aje/2021/fifa-arab-cup-2021/index.html?utm_source=www.aljazeera.com&utm_medium=website&utm_campaign=ucms"]


for link in tqdm(links['link'][800:]):
    print("Link")
    print(link)

    if  link  not in unwanted_links:
        driver.get(link)
        # Adding a time delay of 3 seconds for the page to load
        time.sleep(3)
        # Extract title
        header_path = "//main[contains(@id, 'main-content-area')]//header[contains(@class, 'article-header') or contains(@class, 'gallery-header')]"
        main_content_path = "//main[contains(@id, 'main-content-area')]"
        title = driver.find_element("xpath", header_path+"/h1").text
        try:
            head_title = driver.find_element("xpath",header_path+"//p[contains(@class, 'article__subhead css-1wt8oh6')]/em | //h2[contains(@class,'gallery-header__subhead')]").text
        except:
            head_title = ""
        main_content_element = driver.find_elements("xpath",main_content_path+"//div[contains(@class, 'wysiwyg wysiwyg--all-content css-ibbk12') or contains(@class,'gallery-content wysiwyg wysiwyg--all-content css-ibbk12')]/p")
        main_content = ""
        for p in main_content_element:
            main_content = main_content + " ." + p.text
        date =  driver.find_element("xpath",main_content_path + "//div[contains(@class, 'article-info-block css-ti04u9') or contains(@class, 'article-info-block')]/div[contains(@class,'article-b-l')]//div[contains(@class,'date-simple css-1yjq2zp')]/span[@class='screen-reader-text']").text

        article_dates.append(date)
        titles.append(title)
        head_titles.append(head_title)
        main_contents.append(main_content)



data = {'date': article_dates, 'title': titles, 'head_titel': head_titles, 'main_content': main_contents }
df = pd.DataFrame(data)
df.to_csv("processed_data_very_new_6.csv", index=False)

"""





