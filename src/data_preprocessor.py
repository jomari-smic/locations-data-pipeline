# data_preprocessor.py

import logging
import re

from pandas import DataFrame
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

# concatenate the barangay and city
concat_brgy_city = lambda row: row['barangay'] + ' ' + row['city']
# concatenate the barangay, city, province
concat_until_region = lambda row: row['barangay'] + ' ' + row['city'] + ' ' + row['province'] + ' ' + row['region']


def filter_df_columns(df: DataFrame, cols: list):
    return df[cols]


def normalize_selected_columns(df: DataFrame, cols: list):

    for col in cols:
        df[col] = df[col].apply(lambda x: x.lower())

    return df

def filter_masterlist_by_province_and_region(df, province, region):
    return df.loc[(df['province'] == province) & (df['region'] == region)]

# TODO: clearer function name and docs
# eto yung new column to know if barangay or city is found sa masterlist
# by comparing from our set of cities and barangays
def create_is_found_in_column(df, column, set):

    # the field will be set to None if not found but if found will set to the matched word
    df[column] = df["address_string_cleaned"].apply(lambda x: next((b.title() for b in set if b.lower() in x.lower()), None))

    return df

def make_column_title_case(df, col_name, inplace=False):

    title_case_col = df[col_name].str.title()
    if inplace:
        df[col_name] = title_case_col
    else:
        df[f"{col_name}_titlecase"] = title_case_col

def preprocess_address(df):
    # Step 1: Normalize spaces
    df['address_string_cleaned'] = df['address_string'].apply(lambda x: ' '.join(x.split()))

    # Step 2: Add spaces between numbers and letters
    df['address_string_cleaned'] = df['address_string_cleaned'].apply(lambda x: re.sub(r'(\d)([a-zA-Z])', r'\1 \2', x))

    # Step 3: Remove symbols
    df['address_string_cleaned'] = df['address_string_cleaned'].apply(lambda x: re.sub(r'[^\w\s]', '', x))

    # Step 4: Remove numbers except those with barangay or brgy before it
    df['address_string_cleaned'] = df['address_string_cleaned'].apply(lambda x: re.sub(r'(?<!barangay\s)(?<!brgy\s)\d+', '', x))

    # Step 5: Normalize to lowercase
    df['address_string_cleaned'] = df['address_string_cleaned'].apply(lambda x: x.lower())

    # Step 6: Remove words with length less than 3 except "fe" and "oy", (fe and oy are found in our master data list)
    # Since we're using barangay master list of Iloilo and Region VI, fe and oy are not present in the data
    df['address_string_cleaned'] = df['address_string_cleaned'].apply(lambda x: ' '.join(word for word in x.split() if len(word) >= 3 or word in ['fe', 'oy']))

    # Step 7: Remove keywords found from this set {'blk', 'block', 'lt', 'lot', 'street'}
    # we don't need the following details
    #cant remove 'street','subd', 'village' because it exist in barangays
    keywords_to_remove = {'blk', 'block', 'lt', 'lot', 'subdivision'}
    df['address_string_cleaned'] = df['address_string_cleaned'].apply(lambda x: ' '.join(word for word in x.split() if word not in keywords_to_remove))

    return df