# qatar-world-cup-data-analysis

## Using Natural Language Processing Approaches to compare different media outlets on covering the world cup 2022


___
#### Research question:
> **The FIFA football world cup 2022** was unlike other world cups before. Starting with corruption scandals surrounding the awarding, to the high death toll of construction workers and ongoing human rights abuses, the focus of the media did not seem to be purely on the beautiful game, at least in western countries. But how was the first world cup hosted by an arab/african nation perceived around the world? How did different media outlets report on it? What topics were discussed and what was the sentiment and did the different media outlets discuss different topics or did they discuss similar topics? To answer these questions, we must collect news reports from all over the world, dating way before the first whistle blew in November 2022. 


**Data Schema**:
> Source, date, author , title , content

___

#### Use:
                                               
![alt text](https://github.com/Abdulnaser98/qatar-world-cup-data-analysis/blob/main/figure/6D446898-ACF3-44B6-8F86-70B294262E73.jpeg?raw=true)

When the **"main.py"** file is run , 4 python files will be called: 
1. scraper.py 
2. data_cleaning.py
3. sentiment_analysis.py 
4. Named_entity_recognition.py 

The first python that is called by the main.py is the **scraper.py** is stored in the follwoing folder: **./code_base/data_extraction/scrapers** and there is one scraper python file for each media outlet that can be used to extract the data from the three media outlets **"The guardain", "BBC" and "Al jazeera"** and when the data are extracted , they will be stored in the follwing folder: **./code_base/data_extraction/raw_data**

The second python file that is called by the main.py is the data_cleaning.py that is used to clean the extracted raw data and then the cleaned data will be 
stored in the follwing folder: ./code_base/data_extraction/data_cleaned 

The third python file that is called by the main.py is the sentimetn_analysis.py that is used to conduct sentimet analysis on the cleaned data and the generated sentiment scores statistics will be stored in the follwoing folder: ./code_base/evaluation

The fourth python file that is called by the main.py is the Named_Entitiy_recognition.py that is used to extract named entitties from the cleaned data for each media outlet and the resulted named entities will be stored in the folllwoing folder: ./code_base/evaluation/{medua_outlet}/NER 
 


