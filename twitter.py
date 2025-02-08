import base58
import requests
from solders.pubkey import Pubkey
from solana.rpc.api import Client

# Solana RPC client (mainnet-beta endpoint)
client = Client("https://api.mainnet-beta.solana.com")

# Correct Metaplex Token Metadata Program ID
METADATA_PROGRAM_ID = Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")

def get_metadata_account(mint_address: str) -> Pubkey:
    """Derives the metadata account address from the mint address using a Program Derived Address (PDA)."""
    mint_pubkey = Pubkey.from_string(mint_address)
    metadata_seed = [
        b"metadata",  # Seed prefix for Metaplex metadata
        METADATA_PROGRAM_ID.as_bytes(),  # Correct method to get bytes from Pubkey
        mint_pubkey.as_bytes()  # Correct method for mint_pubkey as well
    ]
    metadata_pubkey, _ = Pubkey.find_program_address(metadata_seed, METADATA_PROGRAM_ID)
    return metadata_pubkey

def fetch_metadata(mint_address: str):
    """Fetch and parse token metadata from a given mint address."""
    try:
        metadata_account = get_metadata_account(mint_address)
        print(f"Derived Metadata Account: {metadata_account}")

        # Fetch account information for the metadata account
        response = client.get_account_info(metadata_account)
        account_info = response.get('result', {}).get('value', {})

        if not account_info:
            print(f"No metadata found for mint address: {mint_address}")
            return None

        # Decode the data (it's base58-encoded)
        data = base58.b58decode(account_info['data'][0])

        # The URI is typically stored starting at byte 115 (Metaplex Metadata format)
        uri_offset = 115
        uri = data[uri_offset:].split(b'\x00', 1)[0].decode("utf-8")
        print(f"Metadata URI: {uri}")

        # Fetch and parse the metadata from the URI (usually JSON hosted on Arweave or IPFS)
        metadata_response = requests.get(uri)
        if metadata_response.status_code == 200:
            metadata_json = metadata_response.json()
            return metadata_json
        else:
            print(f"Failed to fetch metadata from URI: {uri}")
            return None

    except Exception as e:
        print(f"An error occurred while fetching metadata: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Replace with a valid Solana token mint address
    mint_address = "mntYaUoFdkQSrAYBQGngaBYiy2brkF2XwV1YoTPiv6Z"  # Ensure this is a valid Solana mint address
    metadata = fetch_metadata(mint_address)
    
    if metadata:
        print("Token Metadata:", metadata)
