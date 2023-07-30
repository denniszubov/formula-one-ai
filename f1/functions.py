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


# Driver Information functions
def get_driver_information(season: int = 0, round: int = 0) -> pd.DataFrame:
    """Get driver information for the whole history of F1, for a season,
    or for a specific round in a season.

    The driver information contains a driver_id which is used to identify
    drivers in other functions. You can use this function to get a list of all
    drivers info to find the driver_id of a specific driver.

    If you want to get all driver info, do not specify season or round. To
    get info for a season, specify season only. If you want driver info for a
    specific round, specify season and round.

    Args:
        season (int): used to specify the year in which
            to fetch the driver info. Not required
        round (int): used to specify the round in which
            to fetch the driver info. Not required

    Return:
        pd.DataFrame: a dataframe representing the driver info. It contains
        driver_id, first name, last name, date of birth, and nationality.
    """
    url = BASE_URL
    if season:
        url += f"/{season}"
        if round:
            url += f"/{round}"

    # We are adding the `limit` arg to ensure we get all the drivers in one call.
    # Otherwise, the limit default is 30

    url += "/drivers.json?limit=10000"

    response = requests.get(url)
    data = response.json()

    drivers = data["MRData"]["DriverTable"]["Drivers"]

    driver_ids = [x["driverId"] for x in drivers]
    first_names = [x["givenName"] for x in drivers]
    last_names = [x["familyName"] for x in drivers]
    date_of_births = [x["dateOfBirth"] for x in drivers]
    nationalities = [x["nationality"] for x in drivers]
    driver_info = pd.DataFrame(
        {
            "driver_id": driver_ids,
            "first_name": first_names,
            "last_name": last_names,
            "date_of_birth": date_of_births,
            "nationality": nationalities,
        }
    )

    return driver_info


f1_data = [get_driver_standings, get_constructors_standings, get_season_info]
