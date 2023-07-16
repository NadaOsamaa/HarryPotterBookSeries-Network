# Harry Potter Book Series Network

## Introduction
This Python script aims to extract character relationships from Harry Potter Book Series using Named Entity Recognition (NER) and create a graph visualization of the relationships between the characters. The graph is created using the NetworkX and Pyvis libraries.

## Requirements
- pandas
- selenium
- webdriver_manager
- matplotlib
- os
- logging
- re
- numpy
- spacy
- networkx
- pyvis

You can install these libraries using pip:

```
pip install pandas selenium webdriver_manager matplotlib os logging re numpy spacy networkx pyvis
```

## Explanation
The script first extracts the character names from the [Harry Potter Wiki page](https://harrypotter.fandom.com/wiki/Category:Individuals_by_eye_colour) based on their eye color. Then, it reads [the preprocessed Harry Potter books text file](https://www.kaggle.com/datasets/moxxis/harry-potter-lstm?select=Harry_Potter_all_books_preprocessed.txt) and extracts the named entities using the spaCy library. It filters out the named entities that are not characters and creates a dataframe with sentences and the characters mentioned in each sentence.

Next, the script creates relationships between the characters based on the co-occurrence of their names in a window of **five sentences**. It creates a pandas dataframe with the edges of the graph, where each row represents an edge between two characters.

Finally, the script creates a graph visualization of the relationships between the characters using NetworkX and Pyvis libraries. The resulting Pyvis graph shows the characters as nodes and the relationships between them as edges. The size of the nodes represents the degree of the character, and the width of the edges represents the strength of the relationship. and in the colored Pyvis graph, nodes are colored according to groups.

## Visualization Output
![download (2)](https://github.com/NadaOsamaa/HarryPotterBookSeries-Network/assets/88216343/a668db42-498b-4437-88c4-72113d9dd846)

## Credits
- This code was created by [Nada Osama](https://github.com/NadaOsamaa)
- [Harry Potter Book Series](https://www.kaggle.com/datasets/moxxis/harry-potter-lstm?select=Harry_Potter_all_books_preprocessed.txt) text file was obtained from Kaggle
