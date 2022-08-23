# Web Scrapping for french websites

Here is a python script for scraping any web tags from the website URLs marked down in the .txt file in data directory.

## Initialization

The first part from line 18 to line 34 is for the initialization of the objects/intsances/files needed.
 - lines 18-24 : load the stopwords.json file (you can change that file to get teh stopwords from the language you want).
 - lines 26-28 : instantiation for : the tokener with the regular expression you want, the french stemmer and the french lemmatizer.
 - lines 30-34 : open the urls.txt and read it line by line.

## Scrapping

The **scrapper** function needs two arguments :
 - the urls, gotten from urls.txt.
 - the tags you want to get.

It will return you a pandas DataFrame for every urls with the tags chosen.
You also have an excel file exported as "web_semantique.xlsx" to share the data with your team.

## Plot ngrams

The **show_ngrams** function needs 4 arguments :
 - the web DataFrame you want to use to analyse the ngrams.
 - the web tags on the one you want to do the analysis.
 - the number of ngrams you want to plot.
 - the n of the ngrams you want (E.g. 2 for bigrams).

It will plot you an interactive bar chart on your web browser using a local ip. More info about the bar plot from plotly : [HERE](https://plotly.com/python/bar-charts/).
