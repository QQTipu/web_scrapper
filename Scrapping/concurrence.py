from multiprocessing.sharedctypes import Value
from ntpath import join
from operator import index
from optparse import Values
from turtle import color, width
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
# from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer

nom = "stopwords-fr.json"
chemin = os.path.dirname(__file__)
path_fichier = os.path.join(chemin, nom)
f = open(path_fichier,'r', encoding='utf-8')                # On ouvre le fichier de stopwords
stopwords = f.read()
f.close()
stopwords = json.loads(stopwords)

tokener = nltk.RegexpTokenizer(r"\w+")                      # Instanciation de l'objet tokener
stemmer = FrenchStemmer()                                   # Instanciation de l'objet stemmer
# lemmatizer = FrenchLefffLemmatizer()

url_txt = "data\\concurrence_short.txt"
path_url = os.path.join(chemin, url_txt)
f = open(path_url, 'r', encoding='utf-8')
urls = f.read().splitlines()
f.close()

def show_ngrams(txt_clean, nb_item, n):
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

txt_clean = []

for url in urls :
    print(url, requests.get(url))
    data = requests.get(url)                                    # On va charger le HTML de la page "url"
    soup = BeautifulSoup(data.text, 'html.parser')              # On instancie l'objet soup, à partir de la classe BeautifulSoup, pour parser le HTML

    for balise in soup.find_all("p"):                           # Pour chaque balise dans le code 
        txt_brut = balise.text.strip()                          # On récupère le txt
        txt_brut = txt_brut.lower()                             # On passe le txt en minuscules
        txt_brut = unidecode(txt_brut)                          # On decode les accents et caractères spéciaux
        token = tokener.tokenize(txt_brut)                      # On tokenise le txt
        # print(token)

        for word in token:
            if word not in stopwords and not word.isdigit():    # Si word n'est ni stopword ni un nombre
                stem = stemmer.stem(word)                       # Garde uniquement la racine du mot
                # word = lemmatizer.lemmatize(word, 'v')                # Passe les verbes à l'infinitf
                txt_clean.append(stem)

show_ngrams(txt_clean, 25, 4)


txt_final = " ".join(txt_clean)
nom_sem = "web-semantique.txt"
path_sem = os.path.join(chemin, nom_sem)

f = open(path_sem,'w', encoding='utf-8')                     # On ouvre le fichier de rendu
f.write(txt_final)
f.close()