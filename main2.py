import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup

all_prod_link_list2 = []
with open('/Users/sz742/Ai-core-Project-1-Web_Scraping/all_product_links_method2.csv', newline='') as file:
    for row in csv.reader(file):
        all_prod_link_list2.append(row[0])
print(all_prod_link_list2[:5])


nutri_df= pd.DataFrame()


for ur in all_prod_link_list2[1:]:
    r = requests.get(ur) # make a HTTP GET request to this website
    html_string = r.text 
    soup = BeautifulSoup(html_string, 'lxml')  
    try:
        table_nutrition = soup.find('table', {'class' : 'table table-striped'}).find('tbody')
    except: AttributeError
    pass
    #     table_nutrition = soup.find('table', {'class' : 'table table-striped'}).find('tbody')
    nutrition = {}
    try:
        product_name = soup.find('span', {'class' : 'name___30fwb'}).text
    except: AttributeError
    pass
    # print(product_name)
    for row in table_nutrition.find_all('tr'):
        key = row.find('th').text
        value = row.find('td').text
        nutrition[key] = value
    nutrition.update({'product_name': product_name})
    nutri_df = nutri_df.append(nutrition, ignore_index=True)
    # nutri_df['product_name'] = product_name
    
    print(ur)

with open('nutrition_typical_values.csv', 'a') as f:
    nutri_df.to_csv(f, mode='a', header=f.tell()==0) 
print(nutri_df.head())

