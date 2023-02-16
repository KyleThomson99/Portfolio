import pandas as pd
import requests
import urllib.request
from bs4 import BeautifulSoup
import re

def scrape_wiki(wiki_url):
    html = urllib.request.urlopen(wiki_url)
    soup = BeautifulSoup(html, 'html.parser')


    tables = soup.find_all('table', class_ = 'wikitable plainrowheaders')

    list_of_dfs = []

    for table in tables:
        if 'albums' in table.find('caption').text.lower():
            html_table = pd.read_html(str(table))
            df_table = pd.DataFrame(html_table[0])

            list_of_dfs.append(df_table)
        elif 'mixtape' in table.find('caption').text.lower():
            html_table = pd.read_html(str(table))
            df_table = pd.DataFrame(html_table[0])

            list_of_dfs.append(df_table)
    
    df = pd.concat(list_of_dfs)
    df.columns = df.columns.droplevel()
    df = df.reset_index()
    df.drop('index', axis = 1, inplace = True)
    df = df[[col for col in df.columns if 'Unnamed' not in col]]

    df = df[df['Title'].str.contains('denotes') == False]

    return df