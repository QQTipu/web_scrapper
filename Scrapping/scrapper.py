from matplotlib.pyplot import text
import requests
from bs4 import BeautifulSoup

import nltk
import json
import os
from nltk.stem.snowball import FrenchStemmer
from nltk.probability import FreqDist
from nltk.util import ngrams

from unidecode import unidecode
import plotly.express as px
import pandas as pd
import numpy as np
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer

nom = "stopwords-fr.json"
chemin = os.path.dirname(__file__)
path_fichier = os.path.join(chemin, nom)
f = open(path_fichier,'r', encoding='utf-8')                # On ouvre le fichier de stopwords
stopwords = f.read()
f.close()
stopwords = json.loads(stopwords)

tokener = nltk.RegexpTokenizer(r"\w+")                      # Instanciation de l'objet tokener
stemmer = FrenchStemmer()                                   # Instanciation de l'objet stemmer
lemmatizer = FrenchLefffLemmatizer()                        # Instanciation de l'objet lemmatizer

url_txt = "data\\urls.txt"
path_url = os.path.join(chemin, url_txt)
f = open(path_url, 'r', encoding='utf-8')
urls = f.read().splitlines()
f.close()

def flatten_list(_2d_list):
    flat_list = []

    for element in _2d_list:
        if type(element) is list:
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

def clean_text(data_web, tag):
    list_fin = []
    index = 0

    for url in data_web['url']:
        list_fin.append(data_web.loc[index][tag].split(", "))
        list_fin = flatten_list(list_fin)
        index = index + 1
    
    return list_fin

def show_ngrams(data_web, tag, nb_item, n):
    txt_clean = clean_text(data_web, tag)
    ngram = list(ngrams(txt_clean, n))
    freq_ngram = FreqDist(ngram)
    top = dict(freq_ngram.most_common(nb_item))

    id = []
    for k in top.keys():
        key = ' '.join(k)
        id.append(key)
    
    freq_ngram = pd.DataFrame(id, columns=['ngram'])
    freq_ngram['value'] = top.values()
    
    fig = px.bar(x=freq_ngram['ngram'], y=freq_ngram['value'])
    fig.show()

def scrapper(urls, tags):
    df = pd.DataFrame()
    df['url'] = urls
    index = 0

    for url in df['url'] :
        print(url, requests.get(url))
        data = requests.get(url)                                        # On va charger le HTML de la page "url"
        soup = BeautifulSoup(data.text, 'html.parser')                  # On instancie l'objet soup, à partir de la classe BeautifulSoup, pour parser le HTML

        for tag in tags :

            txt_clean = []
            
            print('For tags :', tag)     
            for balise in soup.find_all(tag):                           # Pour chaque balise dans le code 
                txt_brut = balise.text.strip()                          # On récupère le txt
                txt_brut = txt_brut.lower()                             # On passe le txt en minuscules
                txt_brut = unidecode(txt_brut)                          # On decode les accents et caractères spéciaux
                token = tokener.tokenize(txt_brut)                      # On tokenise le txt

                for word in token:
                    if word not in stopwords and not word.isdigit():    # Si word n'est ni stopword ni un nombre
                        lem = lemmatizer.lemmatize(word, 'v')           # On met le sverbes à l'infinitif
                        stem = stemmer.stem(lem)                        # Garde uniquement la racine du mot
                        txt_clean.append(stem)
            
            df.loc[[index],[tag]] = ", ".join(txt_clean)
        
        index = index + 1

    df.to_excel('web_semantique.xlsx')
    return df

balises = ["h1", "h2", "h3", "p", "meta", "alt"]
show_ngrams(scrapper(urls, balises), "p", 50, 2)