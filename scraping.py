import collections
import pickle
import re
from statistics import LinearRegression
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

df = pd.read_csv('Most-updated-scrape.csv')
scraping_functions.scatter_3d(df)