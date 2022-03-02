import base64
import time

import requests
import pandas as pd


# api-endpoint
URL = "https://api.elrond.com"

# NFT url
NFT_URL = URL + "/nfts"
COLLECTION_NAME = "GNOGONS-73222b" # Example with the Gnogons
NB_NFT = 10000 # Update this number if necessary


# Useful function that adds 0 for even hexadecimals
def num_to_hex(num) : 
    hexa = format(num, "x")
    if len(hexa)%2==1 :  
        return "0" + hexa
    return hexa   



all_attributes = {}
id_NFT = 1
while id_NFT < (NB_NFT+1):
    
    print(id_NFT)

    id_hex_format = COLLECTION_NAME  + "-" + num_to_hex(id_NFT)

    params = {"collection" : COLLECTION_NAME, "identifiers" : id_hex_format}

    # sending get request and saving the response as response object
    try : 
        nft_requests = requests.get(url = NFT_URL, params=params)
        nft_data = nft_requests.json()
        
    except : 
        time.sleep(5)
        continue


    base64_string = nft_data[0]["attributes"]
    base64_bytes = base64_string.encode("ascii")

    attributes_bytes = base64.b64decode(base64_bytes)
    attributes_string = attributes_bytes.decode("ascii")

    attributes = {}
    for attr in attributes_string.split(";")[:-1] :
        attr_split = attr.split(":")
        attributes[attr_split[0]] = attr_split[1]
    
    all_attributes[id_NFT] = attributes
    
    id_NFT+=1
    time.sleep(0.2) # Pause before each request
    
    
# Save all attributes for every gnogon in a csv file
all_attributes_df = pd.DataFrame(all_attributes).T
all_attributes_df.to_csv("collection_attributes.csv")    