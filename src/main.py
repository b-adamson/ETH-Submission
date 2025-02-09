import subprocess
import os
import sys
from analytics import *
from financial import *
from price_model import *
# by Billy Adamson
# run TS metadata extractor and parser and grab token symbol
def getTokenSymbol(mint_address):
    symbol = None
    try:
        result = subprocess.run(
            ["npx", "esrun", "src/dec.ts", mint_address], capture_output=True, text=True, check=True, shell=True)
        symbol = result.stdout
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the TypeScript file:")
        print(e.stderr)
    print(symbol)

    return symbol

def generateCSV(google_trends_data, crypto_price_data):
    if not google_trends_data.empty and crypto_price_data is not None:
        combined_data = pd.merge(
            google_trends_data, 
            crypto_price_data, 
            left_index=True, 
            right_index=True,
            how='inner'
        )

        combined_data.to_csv("src/data/coin.csv", header=False)
    else:
        raise Exception("One or both datasets are empty, skipping CSV export.")


def main():

    # find most recent search and add to mint address
    with open('frontend/data/searches.json', 'r') as file:
        data = json.load(file)
    mint_address = data[-1]['name'] 

    # check for valid token, and write a metadata.json if exists, else no file
    symbol = getTokenSymbol(mint_address)
    if not symbol:
        raise Exception("Coin not found")
    
    # get google trends data
    google_trends_data = get_analytics(symbol)

    # get price of coin data
    geckoID = get_coin_id_from_mint(mint_address)
    crypto_price_data = fetch_crypto_data(geckoID, days=365)

    # make csv
    generateCSV(google_trends_data, crypto_price_data)

    # add the trust score to metadata from analysis of csv
    with open('src/data/metadata.json', 'r') as file:
        data = json.load(file)
    data[0]['trustScore'] = predict_crash('src/data/coin.csv') 
    with open('src/data/metadata.json', 'w') as file:
        json.dump(data, file, indent=5)

    os._exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_data = {
            "name": str(e),
            "symbol": "none",
            "image": "data/default.png",
            "trustScore": 0
        }
        file_path = os.path.join("src", "data", "metadata.json")
        os.makedirs(os.path.dirname(file_path), exist_ok=True) 
        
        with open(file_path, "w") as error_file:
            json.dump([error_data], error_file, indent=4)
        
        print(f"Error logged to {file_path}")
        os._exit(0)
        


