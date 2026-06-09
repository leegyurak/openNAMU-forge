from __future__ import annotations


class flask_data_or_variable:
    def __init__(self, flask_data, var_dict):
        if var_dict == {}:
            self.data = flask_data
            self.selected_flask = True
        else:
            self.data = var_dict
            self.selected_flask = False

    def get(self, dict_name, replace_data):
        if self.selected_flask:
            return self.data.get(dict_name, replace_data)

        if dict_name in self.data:
            return self.data[dict_name]

        return replace_data
