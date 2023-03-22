# data_loader.py

import pandas as pd
import logging
import os

import chardet


def load_csv_data(input_dir):
    filepath, filename = os.path.split(input_dir)

    logging.info(f"Loading file: {filename}")
    filepath = os.path.join(filepath, filename)

    # detect encoding of CSV file
    with open(filepath, 'rb') as f:
        result = chardet.detect(f.read())

    return pd.read_csv(filepath, encoding=result['encoding'])


