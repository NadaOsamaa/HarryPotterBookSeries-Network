#!/usr/bin/env python
# coding: utf-8

"""
Created on Sun July 14 2023

@author: Nada Osama
"""

# ![header%20%281%29.jpg](attachment:header%20%281%29.jpg)

# In[1]:


import pandas as pd
import numpy as np
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
import spacy
from spacy import displacy
import networkx as nx
from pyvis.network import Network


# ***

# # Load links & get all character names

# In[2]:


# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

# Silent download of drivers
logging.getLogger('WDM').setLevel(logging.NOTSET)
os.environ['WDM_LOG'] = 'False'

# Create service
webdriver_service = Service(ChromeDriverManager().install())

# Create driver
driver = webdriver.Chrome(service = webdriver_service, options = chrome_options)

# Go to the categories page
page_url = 'https://harrypotter.fandom.com/wiki/Category:Individuals_by_eye_colour'
driver.get(page_url)

# Find categories
categories = driver.find_elements(by=By.CLASS_NAME, value='category-page__member-link')

# all 8 category links in one list
categories_list = []
for category in categories:
    category_url = category.get_attribute('href')
    category_name = category.text
    categories_list.append({'category_name': category_name, 'url': category_url})


# In[3]:


categories_list


# In[4]:


# Find characters in each category link
character_list = []

for category in categories_list:
    # go to categories page
    driver.get(category['url'])
    
    character_elems = driver.find_elements(by=By.CLASS_NAME, value = 'category-page__member-link')
    
    for elem in character_elems:
        character_list.append({'category': category['category_name'],'character': elem.text})
        
# Creating a dataframe for the characters      
characters = pd.DataFrame(character_list)


# In[5]:


print('We have {x} characters.'.format(x = len(characters)))
characters


# ### desplaying number of characters in eace category 

# In[6]:


characters['category'].value_counts().plot(kind="bar");


# ### Cleaning

# In[7]:


# Remove brackets and text within brackets

characters['character'] = characters['character'].apply(lambda x: re.sub("[\(].*?[\)]", "", x)) 
characters['character_firstname'] = characters['character'].apply(lambda x: x.split(' ', 1)[0])
characters['character'] = characters['character'].replace('Ronald Weasley', 'Ron')


# In[8]:


characters[characters['character']=='Hermione Granger']


# In[9]:


characters


# In[10]:


# Load spacy English languague model
NER = spacy.load('en_core_web_sm')


# Maximum number of characters that could be processed by NER() are 1000000
# So we're going to slice and work on the first 1000000 characters only. (and maybe put the rest in a loop later)

# In[12]:


# reading the books text file
books = open('Harry_Potter_all_books_preprocessed.txt','r').read()
book_doc = NER(books[:1000000])


# In[13]:


len(books)


# ***

# # Named entity list per sentence

# In[14]:


sent_entity_df = []

# Loop through sentences, store named entity list for each sentence
for sent in book_doc.sents:
    entity_list = [ent.text for ent in sent.ents]
    sent_entity_df.append({"sentence": sent, "entities": entity_list})
    
sent_entity_df = pd.DataFrame(sent_entity_df)


# In[15]:


sent_entity_df


# In[16]:


# Filtering out non-character entities
def filtering(entity_list, characters):
    return [entity for entity in entity_list 
            if entity in list(characters.character) 
            or entity in list(characters.character_firstname)]


# In[17]:


sent_entity_df['character_entities'] = sent_entity_df['entities'].apply(lambda x: filtering(x, characters))

# Filter out sentences that don't have any character entities
sent_entity_df_filtered = sent_entity_df[sent_entity_df['character_entities'].map(len) > 0]
sent_entity_df_filtered['character_entities'] = sent_entity_df_filtered['character_entities'].apply(lambda x: [item.split()[0] for item in x])
sent_entity_df_filtered


# ***

# # Getting the relationships

# In[18]:


window_size = 5
relationships = []

for i in range(sent_entity_df_filtered.index[-1]):
    end_i = min(i+5, sent_entity_df_filtered.index[-1])
    char_list = sum((sent_entity_df_filtered.loc[i: end_i].character_entities), [])
    
    # Remove duplicated characters that are next to each other
    char_unique = [char_list[i] for i in range(len(char_list)) 
                   if (i==0) or char_list[i] != char_list[i-1]]
    
    if len(char_unique) > 1:
        for idx, a in enumerate(char_unique[:-1]):
            b = char_unique[idx + 1]
            relationships.append({'source': a, 'target': b})
            
relationship_df = pd.DataFrame(relationships)    
relationship_df


# In[19]:


# Sorting
relationship_df = pd.DataFrame(np.sort(relationship_df.values, axis = 1), columns = relationship_df.columns)
relationship_df["value"] = 1
relationship_df = relationship_df.groupby(['source','target'], sort = False, as_index = False).sum()
relationship_df


# ***

# # The Visualization Part

# In[20]:


graph = nx.from_pandas_edgelist(relationship_df, source = 'source', 
                            target = 'target', edge_attr = 'value', 
                            create_using = nx.Graph())


# ### Using Networkx

# In[21]:


fig = plt.figure(figsize=(13,10))
p = nx.kamada_kawai_layout(graph)
nx.draw(graph, with_labels=True, node_color='#5e919e', font_color='white', 
        edge_color='#000000', edge_cmap=plt.cm.Blues, pos = p)
fig.set_facecolor("#333333")
plt.show()


# ### Using Pyvis

# In[22]:


net = Network(notebook = True, width="1000px", height="700px", bgcolor='#222222', font_color='white')

node_degree = dict(graph.degree)
nx.set_node_attributes(graph, node_degree, 'size')

net.from_nx(graph)
net.show("graph.html")


# In[23]:


# recreating the graph but coloring each group
group_net = Network(notebook = True, width="1000px", height="700px", bgcolor='#222222', font_color='white')

node_degree = dict(graph.degree)
nx.set_node_attributes(graph, node_degree, 'group')

group_net.from_nx(graph)
group_net.show("group_graph.html")


# ***

# # The most mentioned characters in Harry Potter

# In[24]:


degree_dict = nx.degree_centrality(graph)
sorted(degree_dict.items(), key=lambda p: p[1], reverse=True)


# ![header%20%281%29.jpg](attachment:header%20%281%29.jpg)
