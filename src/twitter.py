import json  # To read the JSON file
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

pytrends = TrendReq(hl='en-US', tz=360)

with open('data/metadata.json', 'r') as file:
    metadata = json.load(file) 

keyword = metadata.get("symbol", "DefaultSymbol")
pytrends.build_payload([keyword], cat=0, timeframe='all', geo='', gprop='')

data = pytrends.interest_over_time()

if not data.empty:
    data = data.drop(columns=['isPartial']) 

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data[keyword], label=f'Search Interest for "{keyword}"')
    plt.xlabel('Date')
    plt.ylabel('Search Interest')
    plt.title(f'Google Search Interest Over Time for "{keyword}"')
    plt.legend()
    plt.grid(True)
    plt.show()

else:
    print("No data found for the specified keyword.")
