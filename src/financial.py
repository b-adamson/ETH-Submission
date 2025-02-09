import requests
import pandas as pd
# by Arthav Gupta
def fetch_crypto_data(crypto_id, vs_currency='usd', days=30):
    """
    Fetch historical data for a specific cryptocurrency from the CoinGecko API.
    
    Parameters:
    - crypto_id: The ID of the cryptocurrency (e.g., 'bitcoin', 'ethereum', etc.).
    - vs_currency: The currency to get prices in (e.g., 'usd', 'eur').
    - days: The number of days of historical data to fetch. E.g., '30' for the last 30 days.
    
    Returns:
    - DataFrame with timestamp and prices.
    """
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': vs_currency,
        'days': days,  
        'interval': 'daily'
    }
    
    response = requests.get(url, params=params)
    
    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        prices = data['prices']  
        
        # Convert to a DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        return df
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def fetch_sol_token_price(mint_address, days=30):
    """
    Fetch real-time price data for a Solana token using Jupiter Aggregator API.
    
    Parameters:
    - mint_address: The mint address of the Solana token.
    - days: The number of days to simulate historical data (approximate by sampling every 6 hours).
    
    Returns:
    - DataFrame with simulated historical prices (timestamp and price).
    """
    url = f"https://quote-api.jup.ag/v1/price?id={mint_address}"
    prices = []

    # Simulate historical data 
    for i in range(days * 4):  # 4 samples per day
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            price = data['data']['price']
            timestamp = datetime.utcnow() - timedelta(hours=i * 6)
            prices.append({"timestamp": timestamp, "price": price})
        else:
            print(f"Failed to fetch price at iteration {i}. Status code: {response.status_code}")
        
    # Convert to DataFrame
    df = pd.DataFrame(prices)
    df.set_index('timestamp', inplace=True)
    return df


def get_coin_id_from_mint(mint_address, platform='solana'):
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Failed to fetch data from CoinGecko API")
    
    coins = response.json()
    
    for coin in coins:
        if 'platforms' in coin and platform in coin['platforms']:
            if coin['platforms'][platform] == mint_address:
                return coin['id']
    
    return None
