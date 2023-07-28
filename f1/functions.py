import requests


def get_driver_standings(year: int) -> list[tuple[int, str]]:
    """Get the driver standings.

    The input parameter year is used to specify the year in
    which to fetch the standings
    """
    url = f"http://ergast.com/api/f1/{year}/driverStandings.json"

    response = requests.get(url)
    data = response.json()
    drivers = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

    drivers_family_name = [
        (i + 1, x["Driver"]["familyName"]) for i, x in enumerate(drivers)
    ]
    return drivers_family_name


f1_data = [get_driver_standings]
