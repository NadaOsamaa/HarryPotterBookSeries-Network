#!/usr/bin/env python
# coding: utf-8

# In[31]:


import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
import os
import logging
import re 

import numpy as np
import spacy
from spacy import displacy
import networkx as nx


# In[33]:


## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Silent download of drivers
logging.getLogger('WDM').setLevel(logging.NOTSET)
os.environ['WDM_LOG'] = 'False'

# Create service
webdriver_service = Service(ChromeDriverManager().install())

# Create driver
driver = webdriver.Chrome(service = webdriver_service, options = chrome_options)

# Go to the characters in categories page
page_url = 'https://harrypotter.fandom.com/wiki/Category:Individuals_by_eye_colour'
driver.get(page_url)

# Find categories
categories = driver.find_elements(by=By.CLASS_NAME, value='category-page__member-link')

categories_list = []
for category in categories:
    category_url = category.get_attribute('href')
    category_name = category.text
    categories_list.append({'category_name': category_name, 'url': category_url})


# In[34]:


categories_list


# In[35]:


character_list = []

for category in categories_list:
    # go to categories page
    driver.get(category['url'])
    
    character_elems = driver.find_elements(by=By.CLASS_NAME, value = 'category-page__member-link')
    
    for elem in character_elems:
        character_list.append({'category': category['category_name'],'character': elem.text})
        
        
characters = pd.DataFrame(character_list)


# In[36]:


characters[characters['character']=='Harry Potter']


# In[37]:


characters['category'].value_counts().plot(kind="bar");


# In[38]:


# Remove brackets and text within brackets

characters['character'] = characters['character'].apply(lambda x: re.sub("[\(].*?[\)]", "", x)) 
characters['character_firstname'] = characters['character'].apply(lambda x: x.split(' ', 1)[0])


# In[41]:


characters


# In[43]:


# reading the books text file
books = open('Harry_Potter_all_books_preprocessed.txt','r').read()


# In[44]:


books[:1000]


# In[45]:


sent_entity_df = []

# Loop through sentences, store named entity list for each sentence
for sent in books.sents:
    entity_list = [ent.text for ent in sent.ents]
    sent_entity_df.append({"sentence": sent, "entities": entity_list})
    
sent_entity_df = pd.DataFrame(sent_entity_df)


# In[ ]:




