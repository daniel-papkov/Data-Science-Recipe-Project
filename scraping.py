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



df = pd.read_csv('clean_modified.csv')
# print("Correlations:\n")
# scraping_functions.get_corr_all_columns(df)
# print("Original Model")
# scraping_functions.predict_rating_linear(df)
# scraping_functions.predict_rating_nn(df)
scraping_functions.predict_rating_mlp(df)

#scraping_functions.draw_heatmap_view(df)
#scraping_functions.draw_heatmap_view_important(df)
# print("\nModel with Normalized Data")
# scraping_functions.improve_model_linear_with_normalize(df)