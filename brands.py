
# Class for general brands
import pandas


class Brands:
    def __init__(self):
        self.brand = ""
        self.product_type_clothing = "Apparel & Accessories > Clothing"
        self.product_type_shoes = "Apparel & Accessories > Shoes"
        self.season = ""
        self.product_name = ""
        self.description = ""
        self.sku = ""
        self.cost_price = ""
        self.msrp_price = ""
        self.products = {}
        self.output_file_name = ""
        self.location = ""
        self.cleaned_df = None

    def get_location_from_user(self, location_list):
        print("What location are you updating inventory for?")
        idx = 0
        for location in location_list:
            print(f"{idx} - {location}")
            idx += 1

        user_location_idx = int(input("Enter the index of the location: "))
        while location_list[user_location_idx] not in location_list:
            print("[!] Index is incorrect, please input another index for the location...")
            user_location_idx = int(input("Enter the index of the location: "))

        self.location = location_list[user_location_idx]

    """
    Visual representation of the below Size and Quantities data structure
    Used in the get_size_from_product_dict and get_quantity_from_product_dict 
    methods below
    
        [
            {size: quantity},
            {size: quantity},
            ...
        ]
    """
    def get_size_from_product_dict(self, product_dict):
        size = list(product_dict)
        size = str(size[0])
        return size

    def get_quantity_from_product_dict(self, product_dict):
        quantity = list(product_dict.values())
        quantity = quantity[0]
        return quantity

    def convert_to_dataframe(self):
        pass

    def convert_to_shopify_csv(self):
        self.cleaned_df.to_csv(path_or_buf=f"./Converted Inventory/{self.output_file_name}.csv",
                               index=False)

    def parse_file(self, file_name):
        pass

    def parse_to_dictionary(self, content):
        pass

    def save_file(self, file_path):
        # !!! Implement this logic here
        pass