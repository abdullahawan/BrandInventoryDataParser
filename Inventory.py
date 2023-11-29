# Inventory class

import os
import pathlib
import pandas


class Inventory:
    def __init__(self, inv_file):
        self.product_inv = []
        self.cleaned_inv_df = None
        self.inv_file = inv_file
        self.inv_output_file_name = inv_file.split(".")[0].strip() + "_Inventory.csv"

    def convert_to_shopify_csv(self):
        # convert cleaned data frame to csv
        self.cleaned_inv_df.to_csv(path_or_buf=f"./Converted Inventory/{self.inv_output_file_name}",
                               index=False)

    def convert_to_inv_dataframe(self):
        self.cleaned_inv_df = pandas.DataFrame(self.product_inv)

    def parse_product_csv(self):
        file_path = pathlib.Path(f"./Converted Products/{self.inv_file}")
        csv = pandas.read_csv(filepath_or_buffer=file_path)
        for label, content in csv.iterrows():
            # Create a deep copy of the content data frame in which the original
            # data frame is not mutated
            content = content.copy(deep=True)

            # Execute the method to parse content values to dictionary
            product_info = self.parse_to_inv_dictionary(content=content)

            # append product info to existing dictionary
            self.product_inv.append(product_info)

    def parse_to_inv_dictionary(self, content):
        product = {
            "Handle": content["Handle"],
            "Title": content["Title"],
            "Option1 Name": content["Option1 Name"],
            "Option1 Value": content["Option1 Value"],
            "Option2 Name": content["Option2 Name"],
            "Option2 Value": content["Option2 Value"],
            "Option3 Name": content["Option3 Name"],
            "Option3 Value": content["Option3 Value"],
            "SKU": content["Variant SKU"],
            "HS Code": content["HS Code"],
            "COO": content["COO"],
            "Location": content["Location"],
            "Incoming": 0,
            "Unavailable": 0,
            "Committed": 0,
            "Available": content["Variant Inventory Qty"],
            "On hand": content["Variant Inventory Qty"],
        }

        # append finalized product_info dictionary to master dictionary
        return product

    def get_product_inventory_list(self):
        return self.product_inv
