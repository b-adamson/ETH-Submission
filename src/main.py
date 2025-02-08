import subprocess
import os
import sys
from analytics import *
from financial import *

mint_address = "6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN"

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
        # Save the combined data to a CSV file
        combined_data.to_csv('combined_data.csv', header=False)
        print("Combined data has been saved to combined_data.csv")
    else:
        raise Exception("One or both datasets are empty, skipping CSV export.")


def main():
    symbol = getTokenSymbol(mint_address)
    if not symbol:
        raise Exception("Coin not found")
    google_trends_data = get_analytics(symbol)
    geckoID = get_coin_id_from_mint(mint_address)
    crypto_price_data = fetch_crypto_data(geckoID, days=60)
    generateCSV(google_trends_data, crypto_price_data)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_data = {
            "error": str(e),
        }
        file_path = os.path.join("src", "data", "error.json")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create directory if it doesn't exist
        
        with open(file_path, "w") as error_file:
            json.dump(error_data, error_file, indent=4)
        
        print(f"Error logged to {file_path}")


