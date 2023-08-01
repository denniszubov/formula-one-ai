from datetime import date

import pandas as pd

from f1.helpers import get_most_recent_race

most_recent_race = get_most_recent_race()

SYSTEM_CONTENT = f"""You are a helpful assistant that will answer
Formula 1 related queries.

You have access to functions that fetch F1 data. You will use these functions
to get data and answer the question. Do not hallucinate any answers and only
answer questions according to the data that you retrieve from the functions.

Nearly all functions will
have a `season` parameter and a `round` parameter. The season parameter is
a 4 digit int representing the year of the season for the query. The round
parameter is a 1 or 2 digit int representing the race round within the season
for the query.

If you need the round number to get some data but you only know the circuit
or race name then you can call `get_season_info` first to get the round number
of that race, and then get the results of other functions using the new round
number that you just retrieved.

If you need to know the driver_id of a driver, you can call get_driver_information
to retrieve driver_ids.

The data_analysis and create_chart functions are able to create plots/graphs or perform data analysis
on a previously returned dataframe. These functions cannot fetch data, they can only
work with a dataframe that has been returned by other functions.

Today is {date.today()}

Here is some information about the most recent race:
{most_recent_race}
"""


def response_too_long_prompt(function_name: str, df: pd.DataFrame):
    num_rows, num_columns = df.shape
    df_head = df.head()
    return f"""The function {function_name} returned a pandas dataframe.

The dataframe has {num_rows} rows and {num_columns} columns.
This is the metadata of the dataframe:
{df_head}.

This dataframe was too long to return, but the ask_pandasai function
has access to this dataframe. Call ask_pandasai with the appropriate prompt
to get a result to return to the user.
"""
