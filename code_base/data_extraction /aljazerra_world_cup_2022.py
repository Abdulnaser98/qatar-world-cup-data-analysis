# Importing the necessary modules
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Instantiating the Chrome browser object using webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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


while True:
    try:
        # Finding the "Show More" button element using xpath
        show_more = driver.find_element("xpath", "//button[contains(@class, 'show-more-button big-margin')]")
        # Clicking the "Show More" button using JavaScript
        driver.execute_script("arguments[0].click();", show_more)
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

df.to_csv('aljazerra_articles_links.csv')




