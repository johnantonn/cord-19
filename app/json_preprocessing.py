""" This module contains code to provide the preprocessing of raw json files. """

import sys
import argparse
from preprocessing.JSONProcessor import JSONProcessor
from util.util_functions import *


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder", type=str, help="the folder of raw json files")
    parser.add_argument("output_folder", type=str, help="the folder of converted json files")
    args = parser.parse_args()

    if len(vars(args)) != 2:
        print("Wrong number of given arguments")
        sys.exit(1)

    json_files = get_subfolders_and_files(args.input_folder, "json")
    json_processor_obj = JSONProcessor()
    for json_file in json_files:
        output_file = str(json_file).replace(args.input_folder, args.output_folder)
        json_data = read_json_file(json_file)
        json_data_converted = json_processor_obj\
            .convert_dictionaries_to_list(json_data,
                                          [{"external_key": "bib_entries", "internal_key": "id"},
                                           {"external_key": "ref_entries", "internal_key": "id"}])
        write_json_to_file(json_data_converted, output_file)
