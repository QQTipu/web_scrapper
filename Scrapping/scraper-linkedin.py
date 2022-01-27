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

url = "https://www.linkedin.com/search/results/content/?keywords=on-x%20groupe&mentionsOrganization=%5B%2224634%22%5D&origin=FACETED_SEARCH&sid=Dd)&sortBy=%22date_posted%22"

posts = []

print(url, requests.get(url))
data = requests.get(url)                                    # On va charger le HTML de la page "url"
soup = BeautifulSoup(data.text, 'html.parser')              # On instancie l'objet soup, à partir de la classe BeautifulSoup, pour parser le HTML

for balise in soup.find_all("h2"):                           # Pour chaque balise dans le code 
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

print(posts)


# txt_final = " ".join(txt_clean)
# nom_sem = "web-semantique.txt"
# path_sem = os.path.join(chemin, nom_sem)

# f = open(path_sem,'w', encoding='utf-8')                     # On ouvre le fichier de rendu
# f.write(txt_final)
# f.close()