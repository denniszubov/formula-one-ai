from typing import Any, Callable

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
def get_season_info(season: int, cols: list[str]) -> pd.DataFrame:
    """Get information about a specific F1 season. This will return
    all the races in the season, with information about round number,
    race name, date, circuit name, and country.

    Args:
        season (int): used to specify the year in which
            to fetch the season info
        cols (list[str]): list of strings representing which columns
            to return. The columns that are available to return are
            ("round_number", "race_name", "date", "circuit_name", "country").
            Only ask for the columns that you need, the less, the better.

    Return:
        pd.DataFrame: a dataframe representing the season inf
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

    list_mapping = {
        "round_number": round_numbers,
        "race_name": race_names,
        "date": dates,
        "circuit_name": circuit_names,
        "country": countries,
    }
    season_info_dict = {}
    for col in cols:
        season_info_dict[col] = list_mapping[col]
    season_info = pd.DataFrame(season_info_dict)
    return season_info


# Driver Information functions
def get_driver_information(
    cols: list[str], season: int = 0, round: int = 0
) -> pd.DataFrame:
    """Get driver information for the whole history of F1, for a season,
    or for a specific round in a season.

    You can use this function to get a list of all
    drivers info to find the driver_id of a specific driver.

    If you want to get all driver info, do not specify season or round. To
    get info for a season, specify season only. If you want driver info for a
    specific round, specify season and round.

    Args:
        cols (list[str]): list of strings representing which columns
            to return. The columns that are available to return are
            ("driver_id", "first_name", "last_name", "date_of_birth", "nationality").
            Only ask for the columns that you need, the less, the better.
        season (int): used to specify the year. Not required
        round (int): used to specify the round. Not required

    Return:
        pd.DataFrame: a dataframe representing the driver info.
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

    list_mapping = {
        "driver_id": driver_ids,
        "first_name": first_names,
        "last_name": last_names,
        "date_of_birth": date_of_births,
        "nationality": nationalities,
    }
    driver_info_dict = {}
    for col in cols:
        driver_info_dict[col] = list_mapping[col]

    driver_info = pd.DataFrame(driver_info_dict)

    return driver_info


# Race Results functions
def get_race_result(season: int, round: int) -> pd.DataFrame:
    """Get the results of a specific race. It will show the finishing order
    of all the drivers. It will show position, first name, and last name

    Args:
        season (int): used to specify the year. Not required
        round (int): used to specify the round. Not required
    Return:
        pd.DataFrame: a dataframe representing the race result
    """
    url = f"{BASE_URL}/{season}/{round}/results.json"

    response = requests.get(url)
    data = response.json()
    race_result = data["MRData"]["RaceTable"]["Races"][0]["Results"]

    positions = [x["position"] for x in race_result]
    first_names = [x["Driver"]["givenName"] for x in race_result]
    last_names = [x["Driver"]["familyName"] for x in race_result]

    race_result = pd.DataFrame(
        {"position": positions, "first_name": first_names, "last_names": last_names}
    )

    return race_result


# Qualifying Results functions
def get_race_qualifying(season: int, round: int) -> pd.DataFrame:
    """Get the results of a specific qualifying session. It will show the finishing order
    of all the drivers. It will show position, first name, and last name, constructor, q1 time, q2 time, q3 time.
    q2 and q3 times will not be shown if the driver did not qualify for these sessions

    Args:
        season (int): used to specify the year.
        round (int): used to specify the round.
    Return:
        pd.DataFrame: a dataframe representing the qualifying result
    """
    url = f"{BASE_URL}/{season}/{round}/qualifying.json"

    response = requests.get(url)
    data = response.json()
    qualifying_result = data["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"]

    positions = [x["position"] for x in qualifying_result]
    first_names = [x["Driver"]["givenName"] for x in qualifying_result]
    last_names = [x["Driver"]["familyName"] for x in qualifying_result]
    constructors = [x["Constructor"]["name"] for x in qualifying_result]
    q1_times = [x["Q1"] for x in qualifying_result]
    q2_times = [x.get("Q2") for x in qualifying_result]
    q3_times = [x.get("Q3") for x in qualifying_result]

    qualifying_result = pd.DataFrame(
        {
            "position": positions,
            "first_name": first_names,
            "last_names": last_names,
            "constructors": constructors,
            "q1_times": q1_times,
            "q2_times": q2_times,
            "q3_times": q3_times,
        }
    )

    return qualifying_result


f1_data: list[Callable[..., Any]] = [
    get_driver_standings,
    get_constructors_standings,
    get_season_info,
    get_driver_information,
    get_race_result,
    get_race_qualifying,
]
