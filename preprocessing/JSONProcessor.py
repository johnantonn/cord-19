""" This module contains closses that preprocess the data. """


class JSONProcessor:
    """ Class that contains methods to process json data. """

    def convert_dictionaries_to_list(self, json_input, dictionaries_to_convert):
        """ Function that converts dictionaries inside the given json to list of dictionaries.

        Args:
            json_input (dict): The input json
            dictionaries_to_convert (list): A list with all the dictionaries to convert along with
                                            the required information

        Returns:
            (dict): The converted json
        """

        for dictionary_to_convert in dictionaries_to_convert:
            dict_data = json_input[dictionary_to_convert["external_key"]]
            if type(dict_data) != dict:
                continue

            internal_key = dictionary_to_convert["internal_key"]
            list_of_dicts = list()
            for key, value in dict_data.items():
                value[internal_key] = key
                list_of_dicts.append(value)
            json_input[dictionary_to_convert["external_key"]] = list_of_dicts

        return json_input
