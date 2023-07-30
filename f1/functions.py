import pandas as pd
import requests

BASE_URL = "http://ergast.com/api/f1"


# Standings functions
def get_driver_standings(season: int, round: int = 0) -> pd.DataFrame:
    """Get the driver standings at the end of a specific season or
    after a specific round in a season. If the round parameter is not
    specified then it will fetch the standings at the end of the
    specific season. If the season hasn't ended you will get the
    current standings.

    Args:
        season (int): used to specify the year in which
            to fetch the standings
        round (int): used to specify the round in which
            to fetch the standings. Not required
    Returns:
        pd.DataFrame: a dataframe representing the driver positions
        and the driver last names.
    """
    if round:
        url = f"{BASE_URL}/{season}/{round}/driverStandings.json"
    else:
        url = f"{BASE_URL}/{season}/driverStandings.json"

    response = requests.get(url)
    data = response.json()
    drivers = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

    positions = [x["position"] for x in drivers]
    last_names = [x["Driver"]["familyName"] for x in drivers]
    driver_standings = pd.DataFrame(
        {
            "position": positions,
            "last_name": last_names,
        }
    )
    return driver_standings


def get_constructors_standings(season: int, round: int = 0) -> pd.DataFrame:
    """Get the constructor standings at the end of a specific season or
    after a specific round in a season. If the round parameter is not
    specified then it will fetch the standings at the end of the
    specific season. If the season hasn't ended you will get the
    current standings.

    Args:
        season (int): used to specify the year in which
            to fetch the standings
        round (int): used to specify the round in which
            to fetch the standings. Not required
    Returns:
        pd.DataFrame: a dataframe representing the constructor position
        and the constructor name.
    """
    if round:
        url = f"{BASE_URL}/{season}/{round}/constructorStandings.json"
    else:
        url = f"{BASE_URL}/{season}/constructorStandings.json"

    response = requests.get(url)
    data = response.json()
    constructors = data["MRData"]["StandingsTable"]["StandingsLists"][0][
        "ConstructorStandings"
    ]

    positions = [x["position"] for x in constructors]
    constructor_names = [x["Constructor"]["name"] for x in constructors]
    constructors_standings = pd.DataFrame(
        {
            "position": positions,
            "constructor name": constructor_names,
        }
    )
    return constructors_standings


# Season List functions
def get_season_info(season: int) -> pd.DataFrame:
    """Get information about a specific F1 season. This will return
    all the races in the season, with information about round number,
    race name, date, circuit name, and country.

    Args:
        season (int): used to specify the year in which
            to fetch the season info

    Return:
        pd.DataFrame: a dataframe representing the season info with
        info about the races. It has the race round, race name, date,
        circuit name, and country.
    """
    url = f"{BASE_URL}/{season}.json"

    response = requests.get(url)
    data = response.json()

    races = data["MRData"]["RaceTable"]["Races"]

    round_numbers = [x["round"] for x in races]
    race_names = [x["raceName"] for x in races]
    dates = [x["date"] for x in races]
    circuit_names = [x["Circuit"]["circuitName"] for x in races]
    countries = [x["Circuit"]["Location"]["country"] for x in races]
    season_info = pd.DataFrame(
        {
            "round_number": round_numbers,
            "race_name": race_names,
            "date": dates,
            "circuit_name": circuit_names,
            "country": countries,
        }
    )

    return season_info


f1_data = [get_driver_standings, get_constructors_standings, get_season_info]
