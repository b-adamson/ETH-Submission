import json 
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

pytrends = TrendReq(hl='en-US', tz=360)
pd.set_option('future.no_silent_downcasting', True)

# with open('data/metadata.json', 'r') as file:
#     metadata = json.load(file) 

def get_analytics(SYMBOL):
    # keyword = metadata.get("symbol", "DefaultSymbol")
    pytrends.build_payload([SYMBOL], cat=0, timeframe='today 1-m', geo='', gprop='')

    data = pytrends.interest_over_time()
    data = data.drop(columns=['isPartial'])

    # if not data.empty:
    #     data = data.drop(columns=['isPartial']) 

    #     plt.figure(figsize=(12, 6))
    #     plt.plot(data.index, data[SYMBOL], label=f'Search Interest for "{SYMBOL}"')
    #     plt.xlabel('Date')
    #     plt.ylabel('Search Interest')
    #     plt.title(f'Google Search Interest Over Time for "{SYMBOL}"')
    #     plt.legend()
    #     plt.grid(True)
    #     plt.show()
    return data
    # else:
    #     print("No data found for the specified keyword.")
# get_analytics("eeee")