import requests
import os
import logging

def fetchTeam(conference):

    url = f"https://v2.nba.api-sports.io/teams?conference={conference}"

    headers = {
        'x-rapidapi-host': "v2.nba.api-sports.io",
        'x-rapidapi-key': os.environ.get("SPORT_KEY")
    }

    try:
        res = requests.get(url, headers=headers)
    except Exception as e:
        logging.info({"Exception":f"While fetching we have an erorr: {e}"})

    if res == None:
        logging.info({"Error":"Result is None"})
        return None
    
    return res.json()
