import pandas as pd
import numpy as np
from os import read

def overview(df):
    print("\n---Nombre de lignes * Nombre de Colonnes---")
    print(df.shape)
    print("\n---Head de la BD---")
    print(df.head())
    print("\n---Info de la DF---")
    print(df.info())
    print("\n---Type de chacun des indexes---")
    print(df.dtypes)

def import_data(filepath):
    df_import = pd.read_csv(filepath, delimiter=',', dtype={"impressions":"int", "engagements":"int", "taux d'engagement":"float", "Retweets" : "int", "réponses":"int", "J'aime":"int", "clics sur le profil de l'utilisateur":"int", "clics sur l'URL":"int","clics sur le hashtag":"int", "ouvertures des détails":"int", "clics sur le permalien":"int"})
    df_import['heure'] = pd.to_datetime(df_import["heure"], format="%Y-%m-%d")
    return(df_import)

def create_df():
    df_list = []
    
    for year in range(2020, 2022):
        if year == 2020:
            for month in range(10, 13):
                filepath = f"./Twitter/data/tweet_activity_metrics_groupe_onx_{year}-{month}.csv"
                df = import_data(filepath)

                df_list.append(df)
        else :
            for month in range(1, 12):
                filepath = f"./Twitter/data/tweet_activity_metrics_groupe_onx_{year}-{month}.csv"
                df = import_data(filepath)

                df_list.append(df)

    df_all = pd.concat(df_list)

    return(df_all)

def main():
    twitter_df = create_df()
    print(twitter_df.dtypes)

    twitter_df.to_csv("./Twitter/data/tweet_activity_metrics_20201001_20211131.csv", sep=';')
    print('Exported successfully !')

main()