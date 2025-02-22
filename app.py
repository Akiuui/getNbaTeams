from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
from fetchers import fetchTeam
from formatters import formatTeams
import os
import logging

load_dotenv()
app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    client = MongoClient(os.environ.get("MONGO_KEY"))
    logging.info("Connected to MongoDB")
except Exception as e:
    logging.critical({f"Exception":"MongoDb could not connect: {e}"})

@app.route("/populate")
def populateTeamDB():
# """Fetches NBA teams from API and stores them in MongoDB."""
    authKey = request.headers.get("Authorization")
    
    if authKey==None or authKey != authKey:
         return jsonify({"AuthError": "Unauthorized access"}), 400
    
    logging.info("Auth key is valid")

    db = client["NbaGames"]
    collection = db["NbaTeams"]

    logging.info("Started with deleting the collection")
    collection.delete_many({})
    logging.info("Deleted the contents of NbaTeams collection")

    resWest = fetchTeam("West")
    resWest = formatTeams(resWest["response"])
    
    resEast = fetchTeam("East")
    resEast = formatTeams(resEast["response"])

    teams = [*resWest, *resEast]

    result = collection.insert_many(teams)

    if result.acknowledged:
        logging.info("Successfuly saved data!")
        return jsonify({"success": "Successfuly saved data"}), 200
    else:
        logging.error("Not saved successfully")
        return jsonify({"error": "Not saved successfully!"}), 400


@app.route("/getIdByCode")
def getIdByCode():
    teamCode = request.args.get('teamCode')
    
    if not teamCode:
        logging.error(f"Args is None")
        return jsonify({"Error": "Missing 'teamCode' parameter"}), 400
    else:
        logging.info(f"Args is teamCode: {teamCode}")

    db = client["NbaGames"]
    collection = db["NbaTeams"]

    logging.info("Trying to find an element via teamCode")
    team = collection.find_one({"code": teamCode})
    logging.info("Found something")

    if team == None or team == []:
        logging.info("Team not found")
    else:
        logging.info("Team found")
        return jsonify(team["_id"]), 200


@app.route("/getTeamById")
def getTeamById():

    teamId = int(request.args.get('teamId'))

    if not teamId:
        logging.error(f"Args is None")
        return jsonify({"Error": "Missing 'teamId' parameter"}), 400
    else:
        logging.info(f"Args is teamId: {teamId}")

    db = client["NbaGames"]
    collection = db["NbaTeams"]

    team = collection.find_one({"_id": teamId})

    if team == None or team == []:
        logging.info("Team not found")
        return jsonify({"Error": "Team not found"}), 400
    else:
        logging.info("Team found")
        return jsonify(team), 200

if __name__ == "__main__":
    from waitress import serve
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 8007))
    serve(app, host="0.0.0.0", port=port)
