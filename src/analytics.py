import json 
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
# by Billy Adamson
pytrends = TrendReq(hl='en-US', tz=360)
pd.set_option('future.no_silent_downcasting', True)

def get_analytics(SYMBOL):
    pytrends.build_payload([SYMBOL], cat=0, timeframe='today 12-m', geo='', gprop='')

    data = pytrends.interest_over_time()
    return data
