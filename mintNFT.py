import os
from dotenv import load_dotenv
import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.requests import AccountNFTs
from xrpl.utils import str_to_hex
import sys
import json

# The first element in sys.argv is the name of the script itself
script_name = sys.argv[0]
# The second element is the JSON string
json_string = sys.argv[1]
# Deserialize JSON string to a Python object
json_data = json.loads(json_string)
# Now you can access the JSON data
# print("JSON data:", json_data)

# Load environment variables
with open('.env', 'r') as file:
    for line in file:
        key, value = line.strip().split('=', 1)
        os.environ[key] = value

# Access environment variables
WALLET_SECRET = os.environ.get('WALLET_SECRET')
XRPL_WS_URL = os.environ.get('XRPL_WS_URL')

print(f"Using XRPL WebSocket URL: {XRPL_WS_URL}")

def optimize_and_encode_report_data(report_data):
    optimized_data = {
        "fid": report_data["farmerId"],
        "loc": report_data["location"],
        "lc": report_data["livestockCount"],
        "mp": report_data["milkProduction"],
        "fc": report_data["feedConsumption"],
        "me": report_data["methaneEmissions"]
    }

    json_data = str(optimized_data) # convert to string
    base64_data = json_data.encode("utf-8").hex() # base64 encode
    data_uri = f"data:application/json;base64,{base64_data}" # data URI
    return str_to_hex(data_uri)

def mint_token(seed, uri, flags, transfer_fee, taxon=0):
    """mint_token"""
    print("Connecting to XRPL...")
    client = JsonRpcClient(XRPL_WS_URL)
    # print('the uri is ---', uri)
    minter_wallet = Wallet.from_seed(seed)
    print(f"Wallet address: {minter_wallet.classic_address}")

    print("Preparing to mint NFT...")
    mint_tx=xrpl.models.transactions.NFTokenMint(
        account=minter_wallet.classic_address,
        uri=uri,
        flags=int(flags),
        transfer_fee=int(transfer_fee),
        nftoken_taxon=int(taxon)
    )
    # print('mint_tx is ---', mint_tx)
    reply=""
    try:
        response=xrpl.transaction.submit_and_wait(mint_tx,client,minter_wallet)
        reply=response.result
        print("NFT Minted Successfully!")
        print(f"Transaction Hash: {response.result['hash']}")
        print(f"Account: {response.result['Account']}")
        print(f"Fee (in drops): {response.result['Fee']}")
        print(f"Transaction Result: {response.result['meta']['TransactionResult']}")
        print(f"NFT Token ID: {response.result['meta']['nftoken_id']}")
        print(f"URI: {response.result['URI']}")
        print(f"Ledger Index: {response.result['ledger_index']}")
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply

def get_tokens(account):
    """get_tokens"""
    client = JsonRpcClient(XRPL_WS_URL)
    account_nfts = AccountNFTs(account=account)
    response=client.request(account_nfts)
    return response.result

def burn_token(seed, nftoken_id):
    """burn_token"""
    owner_wallet=Wallet.from_seed(seed)
    client=JsonRpcClient(XRPL_WS_URL)
    burn_tx=xrpl.models.transactions.NFTokenBurn(
        account=owner_wallet.classic_address,
        nftoken_id=nftoken_id
    )
    reply=""
    try:
        response=xrpl.transaction.submit_and_wait(burn_tx,client,owner_wallet)
        reply=response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply

def main():
    # Example report data
    # example_report_data = {
    #     "farmerId": "FARM12345",
    #     "location": "Location A",
    #     "livestockCount": 100,
    #     "milkProduction": 5000,
    #     "feedConsumption": {"corn": 1000, "soybean": 500},
    #     "methaneEmissions": 200
    # }
    
    uri = optimize_and_encode_report_data(json_data)
    mint_token(WALLET_SECRET, uri, 11, 0)

if __name__ == "__main__":
    main()