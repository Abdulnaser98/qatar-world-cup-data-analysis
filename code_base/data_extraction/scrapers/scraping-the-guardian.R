# This script is used to extract all articles of the category World Cup from The Guardian. It uses the work of the script we discussed in our practice lessons as well as https://ladal.edu.au/webcrawling.html,  with necessary additions for our topic.
# First, we prepare with obligatory options and packages to conduct the web scraping.

options(stringsAsFactors = F)
getwd()
install.packages("webdriver")
library(webdriver)
install_phantomjs()
require(webdriver)
pjs_instance <- run_phantomjs()
pjs_session <- Session$new(port = pjs_instance$port)
require("rvest")

# Then, we examine the overview page and look for a pattern, set it as the base url for later use.
base_url <- "https://www.theguardian.com/football/world-cup-2022?page="
# manually checked how many overview pages there are in total, it's 107
page_numbers <- 1:107
#create character set with all overview urls
paging_urls <- paste0(base_url, page_numbers)
all_links <- NULL
# We download and parse single overview page, extract the links to the articles on that overview page and add it to a vector containing all links.
for (url in paging_urls) {
  pjs_session$go(url)
  rendered_source <- pjs_session$getSource()
  html_document <- read_html(rendered_source)
  links <- html_document %>%
    html_nodes(xpath = "//div[contains(@class, 'fc-item__container')]/a") %>%
    html_attr(name = "href")
  all_links <- c(all_links, links)
}
#To scrape a The Guardian article, we need the url, the title, the content of the article and the date. The same scheme is applied to the other scraping operations.
scrape_guardian_article <- function(url) {
  pjs_session$go(url)
  rendered_source <- pjs_session$getSource()
  html_document <- read_html(rendered_source)
  title_xpath <- "//div[contains(@data-gu-name, 'headline')]//h1"
  title_text <- html_document %>%
    html_node(xpath = title_xpath) %>%
    html_text(trim = T)
  body_xpath <- "//div[contains(@id, 'maincontent')]//p"
  body_text <- html_document %>%
    html_nodes(xpath = body_xpath) %>%
    html_text(trim = T) %>%
    paste0(collapse = "\n")
  date_xpath <- "//meta[contains(@property, 'article:published_time')]"
  date_text <- html_document %>%
    html_node(xpath = date_xpath) %>%
    html_attr(name = "content") %>%
    as.Date()
    cat(format(date_text, "%Y-%m-%d"))
  article <- data.frame(
    url = url,
    date = date_text,
    title = title_text,
    body = body_text
    
  )
  return(article)
}
# Then, the script will perform the previous scraping method to all link articles collected earlier and add it to a data frame
all_articles <- data.frame()
for (i in 1:length(all_links)) {
  cat("Downloading", i, "of", length(all_links), "URL:", all_links[i],
      "\n")
  article <- scrape_guardian_article(all_links[i])
  all_articles <- rbind(all_articles, article)
}
# to extract the data and for further use, we export it to a CSV document
write.csv2(all_articles, file = "guardian_qatar.csv")