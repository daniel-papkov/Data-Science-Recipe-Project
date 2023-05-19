import collections
import pickle
import re
from statistics import LinearRegression
#from statistics import LinearRegression, correlation
import time
from matplotlib.widgets import Lasso
from numpy import average, shape
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Perceptron
from sklearn.metrics  import r2_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import mean_squared_error
import scraping_functions
from mpl_toolkits.mplot3d import Axes3D

from sklearn.metrics import accuracy_score
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import itertools

import csv

# df = pd.read_csv('Most-updated-scrape.csv')
# df = scraping_functions.clean_df(df)
# df = scraping_functions.clean_data_time(df)
# df = scraping_functions.remove_teaspoon(df, 'Ingredients')
# df = scraping_functions.clean_ingridients(df)
# df = scraping_functions.add_difficulty_column(df)

# df = scraping_functions.explode_df_with_ingridients(df)
# df = scraping_functions.add_popularity_score_to_df(df)
# scraping_functions.save_df(df,'FinalCSV.csv')

# url = 'https://www.thespruceeats.com/hallullas-chilean-biscuits-3028924'

# value = scraping_functions.load_soup_object(url)
# print(value)



#scraping_functions.fast_scrape('short_link_list.csv')
df = pd.read_csv('my_data.csv')

df['Fat'] = df['Fat'].str.strip().str.rstrip('g').astype(int)
df['Carbs'] = df['Carbs'].str.strip().str.rstrip('g').astype(int)
df['Protein'] = df['Protein'].str.strip().str.rstrip('g').astype(int)

scraping_functions.save_df(df, 'with_no_grams.csv')

# df = pd.read_csv('clean_modified.csv')
# scraping_functions.draw_all_histo(df)

#scraping_functions.draw_heatmap_view(df)
#scraping_functions.draw_heatmap_view_important(df)
# print("\nModel with Normalized Data")
# scraping_functions.improve_model_linear_with_normalize(df)