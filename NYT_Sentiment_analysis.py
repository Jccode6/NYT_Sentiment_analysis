import requests 
import json
import pandas as pd
from textblob import TextBlob

file = '/Users/josephcrawford/NYT_API_Key.txt'

def get_api_key(file):
    try:
        with open(file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" %file)



#Make API call and load json by month
my_api_key = get_api_key(file)

api_data = []

month_endpoints = ['2023/1','2023/2','2023/3','2023/4','2023/5']
#month_endpoints = ['2023/6','2023/7','2023/8','2023/9','2023/10','2023/11']
                #    '2023/12']


for month in month_endpoints:
    
    base_url = 'https://api.nytimes.com/svc/archive/v1/' + month + '.json?api-key=' + my_api_key
    try:
        article_response = requests.get(base_url)
        articles = article_response.json()
        api_data.append({month: articles})
       
        #api_data.update({month:article_json})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {month}: {e}")
api_data


#Create dictionary of dataframes from json
dfs = {}


for months_data in api_data:
    for month, month_info in months_data.items():
        df = pd.DataFrame(month_info['response']['docs']) 
        dfs[month] = df 
        #print(months_data)
        #print(month_info)


#Combine dataframes into one
final_df = pd.concat([dfs['2023/1'],dfs['2023/2'],dfs['2023/3'],dfs['2023/4'],dfs['2023/5']])

#Convert headline column to string data type

final_df_str = final_df.astype({'abstract':'string'})
print(final_df_str.dtypes)

#Run sentiment analysis on headline column and create new column with result

sentiment_results = []
for index, row in final_df_str.loc[:,['web_url','abstract']].iterrows():
    blob = TextBlob(row[1])
    sentiment = blob.sentiment.polarity
    print(row['abstract'])
    print(sentiment)
    sentiment_results.append(sentiment)

final_df_str['sentiment'] = sentiment_results

#Export to csv
final_df_str.to_csv('/Users/josephcrawford/headlines.csv',mode='a')