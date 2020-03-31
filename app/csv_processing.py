""" This module contains code to provide the preprocessing of raw csv files. """

import sys
import os
import argparse
from pathlib import Path
CURRENT_DIR = os.path.dirname(__file__)
sys.path.append(str(Path(Path(CURRENT_DIR).parents[0])))
from preprocessing.CSVProcessor import CSVProcessor
from util.util_functions import *


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=str, help="the raw csv file")
    parser.add_argument("output_csv", type=str, help="the converted csv file")
    args = parser.parse_args()

    if len(vars(args)) != 2:
        print("Wrong number of given arguments")
        sys.exit(1)

    df = read_csv_file(args.input_csv)
    csv_processor = CSVProcessor()
    df["publish_time"] = df.apply(lambda row: csv_processor.fix_date(row['publish_time']), axis=1)
    write_csv_to_file(df, args.output_csv)