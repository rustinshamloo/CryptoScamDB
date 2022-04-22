
import pandas as pd
import json

with open('scams.json', 'r') as f:
    data = json.load(f)
    
# print(data)

iden_lst = []
name_lst = []
url_lst = []
coin_lst = []
cat_lst = []
sub_lst = []
desc_lst = []
rep_lst = []

for i in range(len(data)):
    
    try:
      iden = data[i]['id']
      iden_lst.append(iden)
      
    except:
      iden_lst.append(',')
    
    try:
      name = data[i]['name']
      name_lst.append(name)
      
    except:
      name_lst.append(',')
    
    try:
      url = data[i]['url']
      url_lst.append(url)
      
    except:
      url_lst.append(',')
    
    try:
      coin = data[i]['coin']
      coin_lst.append(coin)
      
    except:
      coin_lst.append(',')
    
    try:
      cat = data[i]['category']
      cat_lst.append(cat)
      
    except:
      cat_lst.append(',')
    
    try:
      sub = data[i]['subcategory']
      sub_lst.append(sub)
      
    except:
      sub_lst.append(',')
    
    try:
        desc = data[i]['description'] 
        desc_lst.append(desc)
        
    except:
        desc_lst.append(',')
    
    rep = data[i]['reporter']
    rep_lst.append(rep)
    
print(iden_lst[:10])    
print(name_lst[:10])
print(url_lst[:10])
print(coin_lst[:10])
print(cat_lst[:10])
print(sub_lst[:10])
print(desc_lst[:10])
print(rep_lst[:10])

# make df with cols = these lists above, then export to .csv for streamlit