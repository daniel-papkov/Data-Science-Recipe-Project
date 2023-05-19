import collections
from statistics import correlation
import time      # for testing use only
import os         # for testing use only
import matplotlib.pyplot as plt
import scipy.stats as stats
import time
from selenium import webdriver
from bs4 import BeautifulSoup  
import pandas as pd
import bs4

from bs4 import BeautifulSoup  
import pandas as pd
import scipy as sc
import numpy as np

import seaborn as sns

import requests
from bs4 import BeautifulSoup
import pandas as pd

import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
import scraping_functions
import re

import csv


from sklearn.feature_extraction.text import CountVectorizer



import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_loaded_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for the page to load
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 
    "comp mntl-article--two-column-right-rail right-rail sc-ad-container article--structured-project lifestyle-food-article mntl-article")))

    # Get the page source and parse it with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    return soup


def load_soup_object(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        else:
            print(f"Error: {response.status_code} - {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e} - {url}")
        return None

def get_info1_thespruceeats(url):#this give us a df [prep,cook,total,servings]
    #url = "https://www.thespruceeats.com/easy-and-fast-funfetti-birthday-cake-recipe-5114476"
    #this was the demo site we tried to scrape from :) 
    
    lines=[] # despites being called lines be get only 1 line 99% of the time
    soup = scraping_functions.load_soup_object(url)
    results_items = soup.find_all(class_='comp article__decision-block mntl-block')
    if(results_items==[]):
        soup = scraping_functions.load_soup_object(url)
        results_items = soup.find_all(class_='comp project-meta')
        print('nigga')

    for item in results_items:
        item.find_all(class_='meta-text__data')
        for sub_item in item:
            if bool(sub_item.text.strip()):
                clean_text = sub_item.text.strip().replace('\n', '')
                lines.append(clean_text)

    if(len(lines)>1):
        new_string = lines[0] + lines[1]
        lines[0]= new_string

    #use regex expressions to clean up the line we get it looks something like this
    #['Prep: 15 minsCook: 20 minsTotal: 35 minsServings: 6 servingsYield: 1 cake', 'ratingsAdd a comment']
    #prep = re.findall(r'Prep:\s*(\d+)\s*mins', lines[0])[0]
    cook_time_str = re.findall(r'Cook:\s*(?:(\d+)\s*(?:hrs?|hours?)\s*)?(?:(\d+)\s*mins?)?', lines[0])[0]
    prep_time_str = re.findall(r'Prep:\s*(?:(\d+)\s*(?:hrs?|hours?)\s*)?(?:(\d+)\s*mins?)?', lines[0])[0]    
    total_time_str = re.findall(r'Total:\s*(?:(\d+)\s*(?:hrs?|hours?)\s*)?(?:(\d+)\s*mins?)?', lines[0])[0]
# Convert cook time to minutes


    hours = int(cook_time_str[0]) if cook_time_str[0] else 0
    minutes = int(cook_time_str[1]) if cook_time_str[1] else 0
    cook_time_minutes = hours * 60 + minutes

    hours = int(prep_time_str[0]) if prep_time_str[0] else 0
    minutes = int(prep_time_str[1]) if prep_time_str[1] else 0
    prep_time_minutes = hours * 60 + minutes


    hours = int(total_time_str[0]) if total_time_str[0] else 0
    minutes = int(total_time_str[1]) if total_time_str[1] else 0
    total_minutes = hours * 60 + minutes
    #total = re.findall(r'Total:\s*(\d+)\s*mins', lines[0])[0]
    #servings = re.findall(r'Servings?:\s*(\d+?)\s*(?:to\s*\d+)?\s*(?:servings|ratings)', lines[0])[0] # sometimes instead of saying servings 6 they say servings 6 to 8 in this case we make it servings 6
    #servings = re.findall(r'servings?:\s*(\d+?)\s*(?:to\s*\d+)?\s*(?:servings?|ratings)', lines[0], re.IGNORECASE)[0]
    #text = "The serving size is 3 servings per container."
    
    if(lines[0].count('serv')):
        match = re.search(r'serv\w*:\D*(\d+)', lines[0], re.IGNORECASE)
        if match:
            servings=(match.group(1))
    else:
        servings=1

    

    # Create a pandas DataFrame from the extracted data
    df = pd.DataFrame({
        'Prep': [prep_time_minutes],
        'Cook': [cook_time_minutes],
        'Total': [total_minutes],
        'Servings': [servings]
    })
    df = df.astype(int)
    return df

def get_info2_thespruceeats(url):#this gives us the rating of the dish
    soup = scraping_functions.load_soup_object(url)
    results_items = soup.find_all(class_='comp js-feedback-trigger aggregate-star-rating mntl-block')
    final_links=[]
    #print(results_items.prettify())
    for item in results_items:##result items size is 1
        text=item.prettify()
        full_stars=text.count('class="active"')
        half_stars=text.count('class="half"')
        return(full_stars+0.5*half_stars)
    
def get_info3_thespruceeats(url):#this extract the nutritional values
    soup = scraping_functions.load_soup_object(url)
    results_items = soup.find_all(class_='nutrition-info__table--row')

    nutritional_vals=[]    


    for item in results_items:
        nutritional_vals.append(item.text.strip())
    new_list = []
    for s in nutritional_vals:
        # Split the string by the \n character and add the two parts to a new list
        parts = s.split('\n')
        # Add the new strings to the new list in the desired format
        #[caleories:934,fat:134g,carbs:999]
        new_list.extend([parts[1], parts[0]])
    #[calories,934,far,134g,carbs,1123,]
    df = pd.DataFrame({'nutrient': new_list[::2], 'value': new_list[1::2]})

    # Set 'nutrient' column as index and transpose DataFrame
    df = df.set_index('nutrient').T
    if df.empty:

        df = pd.DataFrame(columns=['nutrient', 'Calories', 'Fat', 'Carbs', 'Protein'])

        # add a row filled with zeros
        df.loc[0] = ['value', 0, '0g', '0g', '0g']
        df['Calories'] = df['Calories'].astype(np.int32)
        return df

        # df = pd.DataFrame(0, index=[], columns=['Calories', 'Fat', 'Carbs', 'Protein'], dtype=float)
        # df.iloc[0] = {'Calories': 0, 'Fat': 0, 'Carbs': 0, 'Protein': 0}
        # return df
        # df = pd.DataFrame({'Calories': [0], 'Fat': ['0g'], 'Carbs': ['0g'], 'Protein': ['0g']})
        # # Set all the values in the first row to zero
        # df.iloc[0] = {'Calories': 0, 'Fat': 0, 'Carbs': 0, 'Protein': 0}
        # return df
        #return pd.DataFrame({'Calories': 0, 'Fat': 0, 'Carbs': 0, 'Protein': 0}) ##cocktails dont have nutritional values apperently ...
    df['Calories'] = df['Calories'].astype(int)

    return df

def get_info4_thespruceeats(url):#this gives us a list of ingridient(amounts are still in and not removed)
    cond=0
    soup = scraping_functions.load_soup_object(url)
    results_items = soup.find_all(class_='structured-ingredients__list text-passage')
                                        #comp ingredient-list simple-list simple-list--bulleted 

    if(results_items==[]): #sometimes they like to change the class name
        soup = scraping_functions.load_soup_object(url)
        results_items = soup.find_all(class_='simple-list__item js-checkbox-trigger ingredient text-passage')
        cond=1
    nutritional_vals=[]
    if(results_items==[]):
        return []
    for item in results_items:
        temp=item.text.strip()
        nutritional_vals.append(item.text.strip())
        #print(item.text.strip())
    if(cond==1):
        return nutritional_vals
    else:
        my_list = [s.strip() for s in nutritional_vals[0].split('\n\n\n')]
        return(my_list)

def analyze_recipe(ingredients):
    dairy_keywords = ["milk", "cheese", "yogurt", "cream", "butter", "whey", "casein", "curds"]
    meat_keywords = ["beef", "chicken", "pork", "lamb", "turkey", "venison", "duck", "bacon", "sausage",
                     "ham", "prosciutto", "pepperoni", "salami", "chorizo", "bresaola", "pastrami",
                     "corned beef", "veal", "goose", "game", "elk", "bison", "rabbit", "boar", "guinea fowl", "quail"]
    
    categories = {'Dairy': False, 'Meat': False, 'Fur': True}
    
    for ingredient in ingredients:
        ingredient = ingredient.lower()
        if any(keyword in ingredient for keyword in dairy_keywords):
            categories['Dairy'] = True
            categories['Fur'] = False
        elif any(keyword in ingredient for keyword in meat_keywords):
            categories['Meat'] = True
            categories['Fur'] = False
            
    df = pd.DataFrame(categories, index=[0])
    return df

def get_full_page_thespruceeats():#this returns a list of all the links to receipies on the page:
    # URL to scrape
    url = "https://www.thespruceeats.com/search?q=&searchType=recipe"

    # Configure the Selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)

    # Get the page source and parse it with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    results_div = soup.find("div", attrs={"class": "results-list__container"})
    recipe_names = []
    recipe_links = []

    # Scrape the first page
    for li in results_div.find_all("li", class_="results__item"):
        if li.find("a") is not None:
            link = li.find("a").get("href")
        else:
            link = ''

        if li.find("h4", class_="card__title") is not None:
            name = li.find("h4", class_="card__title").text.strip()
        else:
            name = ''
        
        recipe_names.append(name)
        recipe_links.append(link)

    # Scrape subsequent pages if the "Next" button exists
    while True:
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".pagination__item-link--next")))
            next_button.click()
            time.sleep(5)

            # Get the page source and parse it with BeautifulSoup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            results_div = soup.find("div", attrs={"class": "results-list__container"})

            # Scrape recipe names and links
            for li in results_div.find_all("li", class_="results__item"):
                if li.find("a") is not None:
                    link = li.find("a").get("href")
                else:
                    link = ''

                if li.find("h4", class_="card__title") is not None:
                    name = li.find("h4", class_="card__title").text.strip()
                else:
                    name = ''
                print(f"{name} added")
                recipe_names.append(name)
                recipe_links.append(link)

        except:
            break

    # Create a DataFrame with the recipe names and links
    df = pd.DataFrame({"Recipe_name": recipe_names, "Recipe_link": recipe_links})

    # Write DataFrame to a CSV file
    df.to_csv("Recipe_Links_and_Names.csv", index=False)

    # Close the driver
    driver.quit()

    print("Done!")

def merge_data_into_single_df_thespruceeats(url,recepie_name):
    
    df = pd.DataFrame(columns=['Link','Name','Prep', 'Cook', 'Total', 'Servings', 'Rating', 'Calories', 'Fat', 'Carbs', 'Protein', 'Ingredients'])

    recipe_df = scraping_functions.get_info1_thespruceeats(url)

    ratings_list=(scraping_functions.get_info2_thespruceeats(url))

    nutrition_df = scraping_functions.get_info3_thespruceeats(url)

    ingredients = scraping_functions.get_info4_thespruceeats(url)


    if(ingredients==[]):
        ingredients=['','','','']
        print(type(nutrition_df['Calories'][0]))
    new_row = {
        'Link':url,
        'Name':recepie_name,
        'Prep': recipe_df['Prep'][0],
        'Cook': recipe_df['Cook'][0],
        'Total': recipe_df['Total'][0],
        'Servings': recipe_df['Servings'][0],
        'Rating': ratings_list,
        #'Calories': nutrition_df['Calories']['value'],
        'Calories': nutrition_df['Calories'][0],
        'Fat': nutrition_df['Fat'][0],
        'Carbs': nutrition_df['Carbs'][0],
        'Protein': nutrition_df['Protein'][0],
        'Ingredients': [ingredients]
    }
    print(new_row)

    # add the new row to the DataFrame
    #df = df.append(new_row, ignore_index=True)
    df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)
    #pd.concat([df, new_row], ignore_index=True)

    df['Prep'] = df['Prep'].astype(float)
    df['Cook'] = df['Cook'].astype(float)
    df['Total'] = df['Total'].astype(float)
    df['Servings'] = df['Servings'].astype(float)
    df['Rating'] = df['Rating'].astype(float)
    df['Calories'] = df['Calories'].astype(float)

    # display the updated DataFrame
    print("another line added")
    return(df)

def bigloopsover_receipies_thespruceeats(csv_file_name):#this is done with the csv to save time it takes a solid 15 mins to scrape all recepies    
    recipe_names = []
    recipe_links = []
    count=0
    with open(csv_file_name, encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            recipe = ','.join(row).strip().replace('\x9c', '')  # Join recipe name and link with a comma, remove problematic characters
            last_comma = recipe.rfind(',')  # Find the index of the last comma in the recipe string
            if last_comma != -1:
                recipe_name = recipe[:last_comma].strip()  # Get the recipe name before the last comma
                recipe_link = recipe[last_comma+1:].strip()  # Get the recipe link after the last comma
                recipe_names.append(recipe_name)
                recipe_links.append(recipe_link)
            else:
                print(f"Invalid row: {row}")

    final_df=pd.DataFrame()
    for name, link in zip(recipe_names, recipe_links):
        # print(f"Recipe name: {name}")
        # print(f"Recipe link: {link}")
        temp_df=merge_fast(link,name)
        if(final_df.empty):
            final_df=temp_df
        else:
            final_df = pd.concat([final_df,temp_df])
        print(final_df)
    

    print(final_df)

def get_info1_fast(soup_obj):
    lines=[]
    results_items = soup_obj
    results_items = soup_obj.find_all(class_='comp article__decision-block mntl-block')
    if(results_items==[]):
        soup = soup_obj
        results_items = soup.find_all(class_='comp project-meta')        

    for item in results_items:
        item.find_all(class_='meta-text__data')
        for sub_item in item:
            if bool(sub_item.text.strip()):
                clean_text = sub_item.text.strip().replace('\n', '')
                lines.append(clean_text)

    if(len(lines)>1):
        new_string = lines[0] + lines[1]
        lines[0]= new_string

    #use regex expressions to clean up the line we get it looks something like this
    #['Prep: 15 minsCook: 20 minsTotal: 35 minsServings: 6 servingsYield: 1 cake', 'ratingsAdd a comment']
    #prep = re.findall(r'Prep:\s*(\d+)\s*mins', lines[0])[0]
    cook_time_str = re.findall(r'Cook:\s*(?:(\d+)\s*(?:hrs?|hours?)\s*)?(?:(\d+)\s*mins?)?', lines[0])[0]
    prep_time_str = re.findall(r'Prep:\s*(?:(\d+)\s*(?:hrs?|hours?)\s*)?(?:(\d+)\s*mins?)?', lines[0])[0]    
    total_time_str = re.findall(r'Total:\s*(?:(\d+)\s*(?:hrs?|hours?)\s*)?(?:(\d+)\s*mins?)?', lines[0])[0]
# Convert cook time to minutes


    hours = int(cook_time_str[0]) if cook_time_str[0] else 0
    minutes = int(cook_time_str[1]) if cook_time_str[1] else 0
    cook_time_minutes = hours * 60 + minutes

    hours = int(prep_time_str[0]) if prep_time_str[0] else 0
    minutes = int(prep_time_str[1]) if prep_time_str[1] else 0
    prep_time_minutes = hours * 60 + minutes


    hours = int(total_time_str[0]) if total_time_str[0] else 0
    minutes = int(total_time_str[1]) if total_time_str[1] else 0
    total_minutes = hours * 60 + minutes
    #total = re.findall(r'Total:\s*(\d+)\s*mins', lines[0])[0]
    #servings = re.findall(r'Servings?:\s*(\d+?)\s*(?:to\s*\d+)?\s*(?:servings|ratings)', lines[0])[0] # sometimes instead of saying servings 6 they say servings 6 to 8 in this case we make it servings 6
    #servings = re.findall(r'servings?:\s*(\d+?)\s*(?:to\s*\d+)?\s*(?:servings?|ratings)', lines[0], re.IGNORECASE)[0]
    #text = "The serving size is 3 servings per container."
    
    if(lines[0].count('serv')):
        match = re.search(r'serv\w*:\D*(\d+)', lines[0], re.IGNORECASE)
        if match:
            servings=(match.group(1))
    else:
        servings=1

    

    # Create a pandas DataFrame from the extracted data
    df = pd.DataFrame({
        'Prep': [prep_time_minutes],
        'Cook': [cook_time_minutes],
        'Total': [total_minutes],
        'Servings': [servings]
    })
    df = df.astype(int)
    return df    

def get_info2_fast(soup_obj):    
    soup = soup_obj
    results_items = soup.find_all(class_='comp js-feedback-trigger aggregate-star-rating mntl-block')    
    #print(results_items.prettify())
    for item in results_items:##result items size is 1
        text=item.prettify()
        full_stars=text.count('class="active"')
        half_stars=text.count('class="half"')
        return(full_stars+0.5*half_stars)

def get_rating_count(soup_obj):
    soup = soup_obj
    rating_elements = soup.find_all("div", attrs={'class': "comp aggregate-star-rating__count mntl-aggregate-rating mntl-text-block"})
    for rating_element in rating_elements:
        rating_text = rating_element.text.strip()
        try:
            num_ratings = int(rating_text.split()[0])
            return num_ratings
        except ValueError:
            pass
    return 0

def get_info3_fast(soup_obj):
    soup = soup_obj
    results_items = soup.find_all(class_='nutrition-info__table--row')

    nutritional_vals=[]    


    for item in results_items:
        nutritional_vals.append(item.text.strip())
    new_list = []
    for s in nutritional_vals:
        # Split the string by the \n character and add the two parts to a new list
        parts = s.split('\n')
        # Add the new strings to the new list in the desired format
        #[caleories:934,fat:134g,carbs:999]
        new_list.extend([parts[1], parts[0]])
    #[calories,934,far,134g,carbs,1123,]
    df = pd.DataFrame({'nutrient': new_list[::2], 'value': new_list[1::2]})

    # Set 'nutrient' column as index and transpose DataFrame
    df = df.set_index('nutrient').T
    if df.empty: #recepies like cocktails have no calories

        df = pd.DataFrame(columns=['nutrient', 'Calories', 'Fat', 'Carbs', 'Protein'])

        # add a row filled with zeros
        df.loc[0] = ['value', 0, '0g', '0g', '0g']
        df['Calories'] = df['Calories'].astype(np.int32)
        return df 

    df['Calories'] = df['Calories'].astype(int)

    return df

def get_info4_fast(soup_obj):
    cond=0
    soup = soup_obj
    span_elements = soup.find_all('span', {'data-ingredient-name': 'true'})

    # create an empty list to store the ingredient names
    ingredient_names = []

    # loop over the span elements and extract their text content
    for span in span_elements:
        ingredient_names.append(span.text)
    #print(ingredient_names)
    if(len(ingredient_names)>0):
        return(ingredient_names)
    else:
        cond=0
        soup = soup_obj
        results_items = soup.find_all(class_='structured-ingredients__list text-passage')
                                            #comp ingredient-list simple-list simple-list--bulleted  
        #print(results_items)                                           
        if(results_items==[]): #sometimes they like to change the class name
            soup = soup_obj
            results_items = soup.find_all(class_='simple-list__item js-checkbox-trigger ingredient text-passage')
            cond=1
        nutritional_vals=[]
        if(results_items==[]):
            return []
        
        final_lst=[]

        for item in results_items:    
            nutritional_vals.append(item.text.strip())
            #print(item.text.strip())
        if(cond==1):
            return nutritional_vals
        else:        
            for i in nutritional_vals:
                my_list = [s.strip() for s in i.split('\n\n\n')]
                final_lst.extend(my_list)
                #print(final_lst)
            
            return(final_lst)

def get_steps_to_cook(soup_obj):
    class_name = "comp mntl-sc-block-group--LI mntl-sc-block mntl-sc-block-startgroup"
    elements = soup_obj.find_all(class_=class_name)

    # Print the number of elements found
    #print(f"Number of instances of {class_name}: {len(elements)}")
    return len(elements)

def get_number_of_comments(soup_obj):
    li_tag = soup_obj.find('li', {'class': 'nav-tab nav-tab--primary tab-conversation tab-conversation--refresh active'})
    if li_tag is not None:
        comment_count_span = li_tag.find('span', {'class': 'comment-count'})
        if comment_count_span is not None:
            comment_count_text = comment_count_span.text
            print(comment_count_text)
        else:
            print("No comment count found on the page.")
    else:
        print("The li tag with the specified class name was not found on the page.")

def get_number_of_favorites(soup_obj):
    #
    soup = soup_obj
    results_items = soup.find_all(class_='thread-likes')    
    #print(results_items.prettify())
    for item in results_items:##result items size is 1
        text=item.prettify()
        print(text)
        
def merge_fast(url,recepie_name):
    df = pd.DataFrame(columns=['Name','Prep', 'Cook', 'Total', 'Servings', 'Rating','Rating_Count','Dairy','Meat','Fur', 'Calories', 'Fat', 'Carbs', 'Protein','Num_ing','Steps', 'Ingredients'])
    #Dairy
    #Meat
    #Fur
    
    soup_obj = load_soup_object(url)

    if soup_obj is not None:
        soup_obj=soup = scraping_functions.load_soup_object(url)

        recipe_df = scraping_functions.get_info1_fast(soup_obj)

        ratings_list=(scraping_functions.get_info2_fast(soup_obj))

        nutrition_df = scraping_functions.get_info3_fast(soup_obj)

        ingredients = scraping_functions.get_info4_fast(soup_obj)

        rating_num = scraping_functions.get_rating_count(soup_obj)

        meatdaity_df =scraping_functions.analyze_recipe(ingredients)

        num_ing = len(ingredients)

        steps = get_steps_to_cook(soup_obj)



        if(ingredients==[]):
            ingredients=['','','','']
            print(type(nutrition_df['Calories'][0]))
        new_row = {
            'Name':recepie_name,
            'Prep': recipe_df['Prep'][0],
            'Cook': recipe_df['Cook'][0],
            'Total': recipe_df['Total'][0],
            'Servings': recipe_df['Servings'][0],
            'Rating': ratings_list,
            'Rating_Count':rating_num,
            'Dairy':meatdaity_df['Dairy'][0],
            'Meat':meatdaity_df['Meat'][0],
            'Fur':meatdaity_df['Fur'][0],
            'Calories': nutrition_df['Calories'][0],
            'Fat': nutrition_df['Fat'][0],
            'Carbs': nutrition_df['Carbs'][0],        
            'Protein': nutrition_df['Protein'][0],
            'Num_ing' : num_ing,
            'Steps' : steps,      
            'Ingredients': [ingredients]
        }
        #print(new_row)

        # add the new row to the DataFrame
        df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)
        #df_concat = pd.concat([df1, df2], keys=['df2'])
        df['Prep'] = df['Prep'].astype(float)
        df['Cook'] = df['Cook'].astype(float)
        df['Total'] = df['Total'].astype(float)
        df['Servings'] = df['Servings'].astype(float)
        df['Rating'] = df['Rating'    ].astype(float)
        df['Calories'] = df['Calories'].astype(float)

        # display the updated DataFrame
        #print("another line added")
    return(df)

def fast_scrape(csv_file_name):
    recipe_names = []
    recipe_links = []
    count=0

    with open(csv_file_name, encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            recipe = ','.join(row).strip().replace('\x9c', '')  # Join recipe name and link with a comma, remove problematic characters
            last_comma = recipe.rfind(',')  # Find the index of the last comma in the recipe string
            if last_comma != -1:
                recipe_name = recipe[:last_comma].strip()  # Get the recipe name before the last comma
                recipe_link = recipe[last_comma+1:].strip()  # Get the recipe link after the last comma
                recipe_names.append(recipe_name)
                recipe_links.append(recipe_link)
            else:
                print(f"Invalid row: {row}")

    final_df=pd.DataFrame()
    for name, link in zip(recipe_names, recipe_links):
        # print(f"Recipe name: {name}")
        # print(f"Recipe link: {link}")
        temp_df=merge_fast(link,name)
        temp_df.set_index('Name', inplace=True)  # set the index of temp_df to the recipe name
        if(final_df.empty):
            final_df=temp_df
        else:
            final_df = pd.concat([final_df,temp_df])
        print(final_df)

    #final_df.to_pickle('dataframe.pkl')
    #final_df.to_pickle('dataframe.pkl', protocol=4, encoding='utf-8')
    final_df.to_csv('my_data.csv', index=True, encoding='utf-8')
    print(final_df)

def read_csv_file(file_name):
    #df = pd.read_pickle('dataframe.pkl')
    new_df = pd.read_csv('my_data.csv', encoding='utf-8')
    print(new_df)

def initial_data_review():
    df=pd.read_csv('Original-Scraping.csv')
    all_ingredients = []
    for i in df['Ingredients']:
        all_ingredients += eval(i)

    # Count the frequency of each ingredient
    ingredient_counts = pd.Series(all_ingredients).value_counts()

    # Create a pie chart for the top 10 ingredients
    top_10_ingredients = ingredient_counts.head(10)
    plt.pie(top_10_ingredients, labels=top_10_ingredients.index, autopct='%1.1f%%')
    plt.title('Top 10 Ingredients in Recipes')
    plt.show()

def initial_data_review2():
    #Create a list of all the ingredients
    df=pd.read_csv('Original-Scraping.csv')
    all_ingredients = []

    for i in df['Ingredients']:
        all_ingredients += eval(i)
    # Define a list of terms to exclude from the ingredients list
    exclude_terms = ['salt', 'pepper', 'garlic', 'onion', 'paprika', 'cumin', 'chili', 'oregano', 'basil', 'thyme', 'rosemary']
    # Create a list of all the ingredients
    clean_ingredients = []
    for ingredient in all_ingredients:
        ingredient = re.sub(r'\d+(\.\d+)?', '', ingredient) # Remove any quantity
        ingredient = re.sub(r'(\s+\d+)?\s*(large|medium|small)?\s*(cup|teaspoon|tablespoon)s?', '', ingredient, flags=re.IGNORECASE) # Remove any volume/capacity description
        ingredient = ingredient.strip()
        if ingredient and not any(term in ingredient.lower() for term in exclude_terms):
            clean_ingredients.append(ingredient)

    # Count the frequency of each ingredient
    ingredient_counts = pd.Series(clean_ingredients).value_counts()

    # Create a pie chart for the top 10 ingredients
    top_10_ingredients = ingredient_counts.head(10)
    plt.pie(top_10_ingredients, labels=top_10_ingredients.index, autopct='%1.1f%%')
    plt.title('Top 10 Ingredients in Recipes (Excluding Spices)')
    plt.show()

def clean(df,column_name):
    
    print(df[column_name].describe())
    # Calculate the IQR of the Prep column
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1

    # Determine the upper and lower bounds for the Prep column
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 10 * IQR

    # Replace any values outside of the bounds with NaN
    df.loc[(df[column_name] < lower_bound) | (df[column_name] > upper_bound), column_name] = float('NaN')
    #df = df.dropna(subset=[column_name])
    df.dropna(inplace=True)
    print(df[column_name].describe())
    return df

def clean2(df,column_name):
    print(f'results before cleaning {df[column_name].describe()}')
    # Compute the z-scores for the "Prep" column
    z_scores = np.abs((df[column_name] - df[column_name].mean()) / df[column_name].std())

    # Define a threshold for outlier removal (e.g., anything more than 3 standard deviations from the mean)
    threshold = 3

    print(f'results after cleaning {df[column_name].describe()}')
    df = df[z_scores < threshold]
    return df
    # Print the cleaned DataFrame
    # plt.hist(df[column_name], bins=20)
    # plt.xlabel(column_name)
    # plt.ylabel('Frequency')
    # plt.title(f'Distribution of {column_name} Times')
    # plt.xticks(rotation=90)  # Rotate x-axis labels by 90 degrees
    # print(df[column_name].describe())
    # plt.show()

def manual_clean_up(df):
    print(0)

def get_ingridients_dict():
    ingredients = []

    with open('ingridients.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            ingredients.extend(row)

    df= pd.read_csv('clean_modified.csv')


    ingredients_dict = {}

    # loop through the ingredients in the DataFrame
    for line in df['Ingredients']:
        for single_item in line.split(','): # split the ingredients by comma if they're in a single string
            for ing_in_lst in ingredients: # loop through the ingredients in the ingredients list
                if ing_in_lst in single_item.strip(): # check if the ingredient in the list is a substring of the ingredient in the dataset
                    # if the ingredient exists in the dictionary, increment its count
                    if ing_in_lst in ingredients_dict:
                        ingredients_dict[ing_in_lst] += 1
                    # otherwise, add the ingredient to the dictionary with a count of 1
                    else:
                        ingredients_dict[ing_in_lst] = 1

    # sort the dictionary by value in descending order
    sorted_dict = dict(sorted(ingredients_dict.items(), key=lambda x: x[1], reverse=True))

    # print the dictionary of ingredients and their counts
    # print("Ingredient Counts:")
    # for ing, count in sorted_dict.items():
    #     print(f'{ing}: {count}')   
    return sorted_dict

def show_rating_vs_calories():
    
    df =pd.read_csv('my_data.csv')
    fig, ax = plt.subplots()
    ax.plot(df["rating"], df["calories"], linewidth=2)

    # Adding x and y labels
    ax.set_xlabel("Rating")
    ax.set_ylabel("Calories")

    # Adding a title
    ax.set_title("Rating vs Calories")

    # Setting the figure size
    fig.set_size_inches(8, 6)

    # Displaying the plot
    plt.show()
  
def draw_scatter_2_params(df,col_name_1,col_name_2):    
    df['Fat'] = df['Fat'].str.replace('g', '').str.replace(',', '').astype(int)
    df['Carbs'] = df['Carbs'].str.replace('g', '').str.replace(',', '').astype(int)
    df['Protein'] = df['Protein'].str.replace('g', '').str.replace(',', '').astype(int)
    df.plot.scatter(x=col_name_1, y=col_name_2)
    
    plt.show()

def draw_histo_1_params(df,col_name):
    # read in your dataframe from a csv file
    # choose the column you want to use for the histogram

    # sort the column values into bins
    bin_values, bin_edges = np.histogram(df[col_name].dropna(), bins='auto')

    # create the histogram using the sorted bins
    plt.hist(df[col_name], bins=bin_edges)

    # add labels and title to the histogram
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Histogram of ' + col_name)

    # display the histogram
    plt.show()

def draw_pie_1_params(df,col_name):
    # get the count of unique values in the column
    value_counts = df[col_name].value_counts()

    # create the pie chart
    plt.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')

    # add title to the pie chart
    plt.title('Pie Chart of ' + col_name)

    # display the pie chart
    plt.show()

def draw_pie_meat_dairy_fur(df):

    #df = pd.read_csv('my_data.csv')
    
    # Calculate the number of recipes in each category
    meat_count = len(df[df['Meat'] == True])
    dairy_count = len(df[df['Dairy'] == True])
    fur_count = len(df[df['Fur'] == True])
    dairy_meat_count = len(df[(df['Dairy'] == True) & (df['Meat'] == True)])

    # Create a list of category counts and labels
    counts = [meat_count, dairy_count, fur_count, dairy_meat_count]
    labels = ['Meat', 'Dairy', 'Fur', 'Dairy&Meat']

    # Create the pie chart
    plt.pie(counts, labels=labels, autopct='%1.1f%%')

    # Add a title to the chart
    plt.title('Recipe Categories')

    # Show the chart
    plt.show()

def draw_ingridient_pie_chart(top_n,total_receipe_count):
    # print()
    ingredient_counts = get_ingridients_dict()

    # Extract the top N ingredients by frequency
    ingredient_names = collections.Counter(ingredient_counts).most_common(top_n)
    ingredient_names = [x[0] for x in ingredient_names]
    ingredient_frequencies = [ingredient_counts[name] for name in ingredient_names]
    total_receipe_count = sum(ingredient_frequencies)
    ingredient_percentages = [(count/total_receipe_count)*100 for count in ingredient_frequencies]
    ingredient_labels = ['{} ({:.1f}%)'.format(name, percentage) for name, percentage in zip(ingredient_names, ingredient_percentages)]

    # Create the pie chart
    plt.pie(ingredient_percentages, labels=ingredient_labels)
    plt.title('Top {} Ingredients'.format(top_n))
    plt.show()

def save_df(df,name):
    df.to_csv(name, index=True, encoding='utf-8')

def remove_g_fron_col(df,col_name):
    df[col_name] = df[col_name].str.replace('g', '').str.replace(',', '').astype(int)
    return df

def clean_data_time(df):
    #df = pd.read_csv('clean_df.csv')

    # Replace Prep, Cook, and Total values with median if Prep + Cook != Total
    for index, row in df.iterrows():
        if row['Prep'] + row['Cook'] != row['Total']:
            if row['Prep'] != 0:
                df.at[index, 'Cook'] = df.at[index, 'Total'] - df.at[index, 'Prep']
            elif row['Cook'] != 0:
                df.at[index, 'Prep'] = df.at[index, 'Total'] - df.at[index, 'Cook']
            else:
                df.drop(index, inplace=True)

    # Fill missing Total values with Prep + Cook
    df['Total'].fillna(df['Prep'] + df['Cook'], inplace=True)

    # Fill missing Prep or Cook values if only one is missing
    for index, row in df.iterrows():
        if pd.isna(row['Prep']):
            if pd.notna(row['Cook']) and pd.notna(row['Total']):
                df.at[index, 'Prep'] = df.at[index, 'Total'] - df.at[index, 'Cook']
            else:
                df.drop(index, inplace=True)
        elif pd.isna(row['Cook']):
            if pd.notna(row['Prep']) and pd.notna(row['Total']):
                df.at[index, 'Cook'] = df.at[index, 'Total'] - df.at[index, 'Prep']
            else:
                df.drop(index, inplace=True)
        elif pd.isna(row['Total']):
            if pd.notna(row['Prep']) and pd.notna(row['Cook']):
                df.at[index, 'Total'] = df.at[index, 'Prep'] + df.at[index, 'Cook']
            else:
                df.drop(index, inplace=True)

    # Save cleaned dataframe to new csv file
    #df = df.drop(columns='Unnamed')
    #df = df.drop(df.columns[0], axis=1)
    #print(df.columns)
    #df.to_csv('Cleaned_df_updated.csv', index=False)
    return df

def clean_df(df):
    #df=pd.read_csv(filename)
    #df=clean_data_time(df)
    df=remove_g_fron_col(df,'Fat')
    df=remove_g_fron_col(df,'Carbs')
    df=remove_g_fron_col(df,'Protein')

    
    #print(df)
    numeric_cols = df.select_dtypes(include=['int', 'float']).columns
    #print(numeric_cols)
    # # loop over the selected columns
    for col in numeric_cols:
        clean(df,col)

    return df

def remove_teaspoon(df, column):
    df=delete_index_columns(df)
    df[column] = df[column].str.replace('teaspoon', '')
    df=delete_index_columns(df)
    return df

def get_correlation(df, col1, col2):
    return df[col1].corr(df[col2])

def draw_all_histo(df):
    df = delete_index_columns(df)
    numeric_cols = df.select_dtypes(include=['int', 'float']).columns.to_list()
    #print(numeric_cols)
    #numeric_cols.remove("Unnamed: 0")
    #print(numeric_cols)
    #print(numeric_cols)
    # # loop over the selected columns
    #print(df.describe())
    for col in numeric_cols:
        scraping_functions.draw_histo_1_params(df,col)

def find_most_common_ingridients():
    final_lst = []
    df = pd.read_csv('Original-Scraping.csv')
    ingredients = df['Ingredients'].tolist()

    for item in ingredients:
        temp = item.replace("'", "")   
        temp = item.replace("\\\\xa0", " ")
        temp = item.replace("\\\\u200b", " ")
        temp = temp.strip("[]").split(", ")
        temp_tokens = []
        for item in temp:
            temp_tokens.extend(item.split())
        final_lst.extend(temp_tokens)

    #print(final_lst)
    word_count = collections.Counter(final_lst)

    # Filter out items that start with a digit
    sorted_dict = {k: v for k, v in word_count.items() if not k[0].isdigit()}
    sorted_dict = dict(sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True))
    
    # Create a DataFrame from the sorted dictionary and save it as a CSV file
    df = pd.DataFrame.from_dict(sorted_dict, orient='index', columns=['count'])
    df.to_csv('Ingredients.csv')

    # Print the top 100 items
    for i, (key, value) in enumerate(sorted_dict.items()):
        if i == 300:
            break
        print(f"{key}: {value}")

def read_ingridients():
    with open('ingridients.csv', 'r') as file:
    # Initialize an empty list to store the data
        data = []
        for line in file:
            line = line.strip()
            values = line.split(',')
            return values
    return data

def delete_index_columns(df):
    # Get a list of all column names that start with 'Unnamed'
    index_cols = [col for col in df.columns if col.startswith('Unnamed')]
    
    # Drop the columns from the dataframe
    df.drop(columns=index_cols, inplace=True)
    
    return df
    
def clean_ingridients(df):
    df=delete_index_columns(df)
    df2=df.copy()
    pure_ingredients=read_ingridients()
    print("starting ingridient cleanup this might take a minute")
    #df=pd.read_csv(filename)
    for i, ingredient in enumerate(df2['Ingredients']):
        line = ingredient.split(",")
        for j, item in enumerate(line):
            for single_ingredient in pure_ingredients:
                if single_ingredient.lower() in item.lower():
                    #print(f'found {single_ingredient} in {item}')
                    line[j] = single_ingredient.lower()
        df2.loc[i, 'Ingredients'] = ",".join(line)
        #print(line)
        #print('\n\n')
    #print(df['Ingredients'])
    # save the modified dataframe to a new CSV file
    df2=delete_index_columns(df)
    df2.to_csv('clean_modified.csv', index=False)
    print("done!")
   
    return df2

def corr_ingridients_rating_1():
    df = pd.read_csv('clean_modified.csv')

    # extract the ingredients column

    # define a list of ingredients you care about
    #important_ingredients = ['salt', 'pepper', 'sugar', 'flour']
    important_ingredients = []

    with open('ingridients.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            important_ingredients.extend(row)

    # create a CountVectorizer object and fit it to the important ingredients
    vectorizer = CountVectorizer(vocabulary=important_ingredients)
    X = vectorizer.fit_transform(df['Ingredients'])

    # convert the vectorized ingredients to a DataFrame
    ingredients_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())

    # concatenate the original DataFrame with the new ingredients DataFrame
    df = pd.concat([df, ingredients_df], axis=1)

    # group the DataFrame by each important ingredient and calculate the mean rating
    ingredient_ratings = df.groupby(important_ingredients)['Rating'].mean()

    # print the ingredient ratings
    #print(ingredient_ratings)
    corr = df[important_ingredients + ['Rating']].corrwith(df['Rating'])

    # sort the correlation values in descending order
    corr_sorted = corr.sort_values(ascending=False)

    # print the top 10 positively correlated ingredients
    print(corr_sorted.head(30))

def corr_ingridients_rating_2(df):#this function expands the dataframe to each ingridient and tries to find a correlation
    #df = pd.read_csv('clean_modified.csv')

    # extract the ingredients column
    df_ing = df['Ingredients']

    # define a list of ingredients you care about
    important_ingredients = []

    with open('ingridients.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            important_ingredients.extend(row)

    # loop through the ingredients you care about
    for ingredient in important_ingredients:
        # create a new column with a value of 1 if the recipe contains the ingredient and 0 otherwise
        df[ingredient] = df_ing.str.contains(ingredient).astype(int)

    correlations = df[['Rating'] + [ingredient for ingredient in important_ingredients]].corr()

    # print the correlation coefficients for each ingredient
    # print(correlations.loc['Rating'])
    top_20 = correlations.loc['Rating'].sort_values(ascending=False)[1:21]
    print("Top 20 ingredients with the highest correlation with the 'Rating' column:")
    print(top_20)
    return df

def explode_df_with_ingridients(df):

    df=delete_index_columns(df)
    df_ing = df['Ingredients']

    # define a list of ingredients you care about
    important_ingredients = []
    with open('ingridients.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            important_ingredients.extend(row)

    # loop through the ingredients you care about
    for ingredient in important_ingredients:
        # create a new column with a value of 1 if the recipe contains the ingredient and 0 otherwise
        df[ingredient] = df_ing.str.contains(ingredient).astype(int)
    df=delete_index_columns(df)
    return df

def get_corr_all_columns(df):
    df = pd.read_csv('clean_modified.csv')
    numeric_cols = df.select_dtypes(include=['int', 'float'])
    if 'Unnamed' in numeric_cols.columns:
        numeric_cols = numeric_cols.drop('Unnamed', axis=1)

    correlation = {}
    for col1 in numeric_cols:
        for col2 in numeric_cols:
            if col1 != col2:
                corr_value = scraping_functions.get_correlation(df, col1, col2)
                if corr_value > 0.5 or corr_value < -0.5:
                    correlation[(col1, col2)] = corr_value

    # Sort the correlations by their absolute value, in descending order
    sorted_correlations = sorted(correlation.items(), key=lambda x: abs(x[1]), reverse=True)

    # Print the correlations above 0.5 or below -0.5
    for corr, value in sorted_correlations:
        if abs(value) > 0.5:
            print(f"{corr[0]} and {corr[1]}: {value}")

def draw_heatmap_view(df):
    heat_map_view = df[['Prep', 'Cook', 'Total', 'Servings', 'Rating', 'Rating_Count', 'Dairy', 'Meat', 'Fur', 'Calories','Fat','Carbs','Protein','Num_ing','Steps','Z_score','Difficulty']]
    sns.heatmap(heat_map_view.corr(), annot=True)
    plt.show()

def draw_heatmap_view_important(df):
    heat_map_view = df[['Prep', 'Cook', 'Total', 'Servings', 'Rating', 'Rating_Count', 'Dairy', 'Meat', 'Fur', 'Calories','Fat','Carbs','Protein','Num_ing','Steps','Z_score','Difficulty']]
    corr = heat_map_view.corr()
    mask = (corr > 0.5) | (corr < -0.5)  # set the threshold for correlation values
    sns.heatmap(corr, annot=True, mask=~mask, cmap='coolwarm')
    
    # print the correlations above 0.5 or below -0.5
    print("Correlations above 0.5 or below -0.5:")
    for i in range(len(corr.columns)):
        for j in range(i):
            if mask.iloc[i, j]:
                print(f"{corr.index[i]} - {corr.columns[j]}: {corr.iloc[i, j]}")

    plt.show()

def build_perceptron_model(df):
    #df = pd.read_csv('test123.csv')

    # Save the 'Rating' column separately
    ratings = df['Rating']

    # Drop the 'Rating' column from the dataframe
    df = df.drop(['Rating'], axis=1)
    df = df.select_dtypes(include=['int', 'float'])
    # Get the column names of the dataframe
    col_names = df.columns

    # Convert the dataframe to a numpy array
    X = df.select_dtypes(include=['int', 'float']).values

    # Define the target variable
    y = (ratings > 4.5).astype(int).values

    # Verify that X and y have the same length
    assert len(X) == len(y), "X and y must have the same length"

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit the Perceptron model to the training data
    model = Perceptron()
    model.fit(X_train, y_train)

    # Compute the predictions on the test data
    y_pred = model.predict(X_test)

    # Compute the accuracy of the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Get the weights learned by the perceptron
    weights = model.coef_[0]

    # Create a new dataframe with the column names and weights
    weights_df = pd.DataFrame({'column': col_names, 'weight': weights})

    # Print the weights dataframe
    print(weights_df)

    scraping_functions.save_df(weights_df,'FML.csv')
    return weights_df

def add_difficulty_column(df):
    # Read the CSV file into a pandas dataframe
    # df = pd.read_csv(csv_file_path)
    
    # Calculate the combined score for each recipe
    df['Combined'] = df['Num_ing'] + df['Steps'] + df['Total']
    
    # Calculate the mean and standard deviation of the combined score
    mean = df['Combined'].mean()
    std_dev = df['Combined'].std()
    
    # Calculate the z-score for each recipe
    df['Z_score'] = (df['Combined'] - mean) / std_dev
    
    # Divide the z-scores into 5 equal-sized groups
    df['Difficulty'] = pd.qcut(df['Z_score'], q=5, labels=[1, 2, 3, 4, 5])
    
    # Write the updated dataframe to a new CSV file
    # new_csv_file_path = csv_file_path.split('.csv')[0] + '_with_difficulty.csv'
    # df.to_csv(new_csv_file_path, index=False)
    save_df(df,'csv_with_diff.csv')
    
    # Print the number of recipes in each difficulty level
    for i in range(1, 6):
        count = df['Difficulty'][df['Difficulty'] == i].count()
        print(f"Difficulty level {i}: {count}")
    
    return df

def add_popularity_score_to_df(df):
    binary_columns = [col for col in df.columns if col not in ['Name', 'Prep', 'Cook', 'Total', 'Servings', 'Rating', 'Rating_Count', 'Dairy', 'Meat', 'Fur', 'Calories', 'Fat', 'Carbs', 'Protein', 'Num_ing', 'Steps', 'Ingredients','Num_ing','Steps','Z_score','Difficulty']]

    # Calculate the frequencies of each binary value
    ingredient_frequencies = df[binary_columns].sum() / len(df) * 30

    # Calculate the popularity score for each recipe
    popularity_scores = []
    for _, row in df.iterrows():
        score = 0
        for column in binary_columns:
            if row[column] == 1:
                score += ingredient_frequencies[column]
        popularity_scores.append(score)

    # Add the popularity scores as a new column to the DataFrame
    df['Popularity Score'] = popularity_scores

    # Print the updated DataFrame
    #print(df)
    scraping_functions.draw_histo_1_params(df,'Popularity Score')
    return df

def predict_rating_linear(df):
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split

    # Prepare X and y
    X = df.drop(['Ingredients', 'Name', 'Rating'], axis=1)
    y = df['Rating']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and fit the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Round predicted ratings to nearest half-integer value
    def round_half_up(x):
        # Clamp ratings to 0-5 range
        x = np.clip(x, 0, 5)
        # Round to nearest half-integer value
        return np.floor(x * 2 + 0.5) / 2

    # Make predictions on the training set
    y_train_pred = model.predict(X_train)
    y_train_pred_rounded = round_half_up(y_train_pred)

    # Count correct and incorrect predictions in the training set
    num_train_correct = np.sum(np.abs(y_train_pred_rounded - y_train) <= 0.25)
    num_train_incorrect = len(y_train) - num_train_correct
    percent_train_correct = num_train_correct / len(y_train) * 100

    # Make predictions on the testing set
    y_test_pred = model.predict(X_test)
    y_test_pred_rounded = round_half_up(y_test_pred)

    # Count correct and incorrect predictions in the testing set
    num_test_correct = np.sum(np.abs(y_test_pred_rounded - y_test) <= 0.25)
    num_test_incorrect = len(y_test) - num_test_correct
    percent_test_correct = num_test_correct / len(y_test) * 100

    # Print results
    print(f"Number of recipes in the dataset: {len(df)}")
    print(f"Number of recipes in the training set: {len(X_train)}")
    print(f"Number of recipes in the testing set: {len(X_test)}")
    print(f"Number of correctly predicted recipes in the training set: {num_train_correct}")
    print(f"Number of incorrectly predicted recipes in the training set: {num_train_incorrect}")
    print(f"Percent of correctly predicted recipes in the training set: {percent_train_correct}%")
    print(f"Number of correctly predicted recipes in the testing set: {num_test_correct}")
    print(f"Number of incorrectly predicted recipes in the testing set: {num_test_incorrect}")
    print(f"Percent of correctly predicted recipes in the testing set: {percent_test_correct}%")

    test_results = np.concatenate((y_test.to_numpy().reshape(-1, 1), y_test_pred_rounded.reshape(-1, 1)), axis=1)
    plt.scatter(range(len(test_results)), test_results[:, 0], label='Actual Ratings')
    plt.scatter(range(len(test_results)), test_results[:, 1], label='Predicted Ratings')
    plt.xlabel('Recipe Number')
    plt.ylabel('Rating')
    plt.ylim(0, 5)  # Set y-axis limits
    plt.title('Actual vs. Predicted Ratings')
    plt.legend()
    plt.show()

    return model, num_train_correct, num_train_incorrect, percent_train_correct, num_test_correct, num_test_incorrect, percent_test_correct

def predict_rating_knn(df):
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.model_selection import train_test_split
    
    # Prepare X and y
    X = df.drop(['Ingredients', 'Name', 'Rating'], axis=1)
    y = df['Rating']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and fit the model
    best_k = 0
    best_accuracy = 0
    for k in range(1, 31):
        model = KNeighborsRegressor(n_neighbors=k)
        model.fit(X_train, y_train)
    
        # Make predictions on the training set
        y_train_pred = model.predict(X_train)
        y_train_pred_rounded = np.round(np.clip(y_train_pred, 0, 5) * 2) / 2
    
        # Count correct and incorrect predictions in the training set
        num_train_correct = np.sum(np.abs(y_train_pred_rounded - y_train) <= 0.25)
        percent_train_correct = num_train_correct / len(y_train) * 100
    
        # Make predictions on the testing set
        y_test_pred = model.predict(X_test)
        y_test_pred_rounded = np.round(np.clip(y_test_pred, 0, 5) * 2) / 2
    
        # Count correct and incorrect predictions in the testing set
        num_test_correct = np.sum(np.abs(y_test_pred_rounded - y_test) <= 0.25)
        percent_test_correct = num_test_correct / len(y_test) * 100
        
        # Print results
        print(f"For k={k}:")
        print(f"Number of correctly predicted recipes in the training set: {num_train_correct}")
        print(f"Percent of correctly predicted recipes in the training set: {percent_train_correct}%")
        print(f"Number of correctly predicted recipes in the testing set: {num_test_correct}")
        print(f"Percent of correctly predicted recipes in the testing set: {percent_test_correct}%")
        
        # Check if the current model is better than the previous best model
        if percent_test_correct > best_accuracy:
            best_k = k
            best_accuracy = percent_test_correct
    
    print(f"\nBest k: {best_k}")
    print(f"Best percent of correctly predicted recipes in the testing set: {best_accuracy}%")
    
    # Train the best model
    model = KNeighborsRegressor(n_neighbors=best_k)
    model.fit(X_train, y_train)
    
    # Make predictions on the testing set
    y_test_pred = model.predict(X_test)
    y_test_pred_rounded = np.round(np.clip(y_test_pred, 0, 5) * 2) / 2
    
    # Count correct and incorrect predictions in the testing set
    num_test_correct = np.sum(np.abs(y_test_pred_rounded - y_test) <= 0.25)
    num_test_incorrect = len(y_test) - num_test_correct
    percent_test_correct = num_test_correct / len(y_test) * 100
    
    # Print final results
    print("\nFinal results:")
    print(f"Number of recipes in the dataset: {len(df)}")
    print(f"Number of recipes in the training set: {len(X_train)}")


def predict_rating_mlp(df):
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from tensorflow import keras
    from keras import layers
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.metrics import r2_score

    print("Preprocessing data...")
    # select features and target variable
    X = df.drop(['Ingredients', 'Name', 'Rating'], axis=1)
    y = df['Rating']

    # scale data
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    X_scraped = scaler.transform(df.drop(['Ingredients', 'Rating', 'Name'], axis=1))
    # split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # build model
    print("Building model...")
    model = keras.Sequential()
    model.add(layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(1))

    # compile model
    model.compile(loss='mse', optimizer='adam')

    # fit model
    model.fit(X_train, y_train, epochs=50, verbose=0)

    # Evaluate the model
    mse = model.evaluate(X_test, y_test, verbose=0)
    rmse = np.sqrt(mse)
    print(f'Root Mean Squared Error: {rmse:.3f}')

    # Predict the ratings for the scraped data
    y_pred = model.predict(X_scraped)

    # Round the predicted ratings to the nearest 0.5
    y_pred_rounded = (np.round(y_pred * 2) / 2)

    # Print the predicted ratings and their accuracy compared to the actual ratings
    print('Predicted Ratings:')
    print(y_pred_rounded.flatten())
    accuracy = r2_score(y_test, model.predict(X_test))
    print(f'Accuracy compared to test data: {accuracy:.3f}')
    
    return y_pred_rounded.flatten()


def scatter_3d(df):

    ax = plt.axes(projection='3d')

    xdata = df['Rating']
    ydata = df['Calories']
    zdata = df['Total']

    ax.set_xlabel('Rating')
    ax.set_ylabel('Calories')
    ax.set_zlabel('Total time')

    ax.scatter3D(xdata, ydata, zdata, c=zdata, depthshade=False)
    plt.show()