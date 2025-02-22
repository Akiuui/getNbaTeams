teamCodes = ["BOS", "BKN", "NYK", "PHI", "TOR", "CHI", "CLE", "DET", "IND", "MIL", "ATL", "CHA", "MIA", "ORL", "WAS", "DEN", "MIN", "OKC", "POR", "UTA", "GSW", "LAC", "LAL", "PHX", "SAC", "DAL", "HOU", "MEM", "NOP", "SAS"]
teamTowns = ["Boston", "Brooklyn", "New York", "Philadelphia", "Toronto", "Chicago", "Cleveland", "Detroit", "Indiana", "Milwaukee", "Atlanta", "Charlotte", "Miami", "Orlando", "Washington", "Denver", "Minnesota", "Oklahoma City", "Portland", "Utah", "Golden State", "Los Angeles", "Los Angeles", "Phoenix", "Sacramento", "Dallas", "Houston", "Memphis", "New Orleans", "San Antonio", "LA"]

def formatTeams(teams):

    formattedTeams = []

    for team in teams:

        if team["code"] not in teamCodes or team["city"] not in teamTowns:
            print(team)
            continue

        if team["city"] == "LA":
            team["city"] = "Los Angeles"

        team.pop("allStar", None)
        team.pop("logo", None)
        team.pop("nbaFranchise", None)
        team["leagues"] = team["leagues"]["standard"]
        team["_id"] = team["id"]
        team.pop("id", None)

        formattedTeams.append(team)

    return formattedTeams

