from typing import Tuple

import requests


def get_driver_standings() -> list[Tuple[int, str]]:
    """Get the driver standings"""
    url = "http://ergast.com/api/f1/current/driverStandings.json"

    response = requests.get(url)
    data = response.json()
    drivers = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

    drivers_family_name = [
        (i + 1, x["Driver"]["familyName"]) for i, x in enumerate(drivers)
    ]
    return drivers_family_name


f1_data = [get_driver_standings]
