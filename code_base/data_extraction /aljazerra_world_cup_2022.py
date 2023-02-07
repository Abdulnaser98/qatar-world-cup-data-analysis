from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


"""
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://scholar.google.com/citations?user=cp-8uaAAAAAJ&hl=en")


time.sleep(3)
while True:
    try:
        show_more = driver.find_element("xpath", "//button[.//span[text()='Show more'] and not(@disabled)]")
        driver.execute_script("arguments[0].click();", show_more)
        print("Show more button clicked")
        time.sleep(2)
    except:
        print("No more Show more button")
        break

elements = driver.find_elements("xpath","//td[contains(@class, 'gsc_a_t')]//a")

print(len(elements))
for l in elements:
    print(l.text)

"""

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.aljazeera.com/qatar-world-cup-2022/")


time.sleep(3)
count = 0
while True:
    try:
        count = count + 1;
        show_more = driver.find_element("xpath", "//button[.//span[text()='Show more'] and not(@disabled)]")
        driver.execute_script("arguments[0].click();", show_more)
        print("Show more button clicked")
        print(count)
        time.sleep(2)
    except:
        print("No more Show more button")
        break







