import pandas as pd
import requests


def get_driver_standings(year: int) -> pd.DataFrame:
    """Get the driver standings at the end of a specific season.
    If the season hasn't ended you will get the current standings.

    Args:
        year (int): used to specify the year in which
        to fetch the standings
    Returns:
        pd.DataFrame: a dataframe representing the driver positions
        and the driver last names.
    """
    url = f"http://ergast.com/api/f1/{year}/driverStandings.json"

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


def get_constructors_standings(year: int) -> pd.DataFrame:
    """Get the constructor standings at the end of a specific season.
    If the season hasn't ended you will get the current standings.

    Args:
        year (int): used to specify the year in which
        to fetch the standings
    Returns:
        pd.DataFrame: a dataframe representing the constructor position
        and the constructor name.
    """
    url = f"http://ergast.com/api/f1/{year}/constructorStandings.json"

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


f1_data = [get_driver_standings, get_constructors_standings]
