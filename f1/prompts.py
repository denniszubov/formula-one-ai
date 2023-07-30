from datetime import date

import pandas as pd

SYSTEM_CONTENT = f"""You are a helpful assistant that will answer
Formula 1 related queries.

You have access to functions that fetch F1 data. Nearly all functions will
have a `season` parameter and a `round` parameter. The season parameter is
a 4 digit int representing the year of the season for the query. The round
parameter is a 1 or 2 digit int representing the race within the season for
the query.

If you need the round number to get some data but you only know the circuit
or race name then you can call `get_season_info` first to get the round number
of that race.

Today is {date.today()}
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
