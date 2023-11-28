
# Class for general brands
import pandas

from GeneralMethods import alert_msg


class Brands:
    def __init__(self, order_id):
        self.order_id = order_id
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
            alert_msg("Index is incorrect, please input another index for the location...")
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
        # create empty list for dictionaries
        list_of_product_rows = []
        for _, product in self.products.items():
            for product_data in product:
                for product_with_sizes in product_data["Sizes and Quantities"]:
                    # get the size and quantity data from the dict contained within the list
                    size = self.get_size_from_product_dict(product_dict=product_with_sizes)
                    quantity = self.get_quantity_from_product_dict(product_dict=product_with_sizes)

                    # create and get product object
                    product_row_data = self.create_get_product_data_object(
                                                                             product_data=product_data,
                                                                             size=size,
                                                                             quantity=quantity
                                                                             )

                    # Get the dictionary from the class and overwrite the variable and
                    # add the product row data to data frame
                    list_of_product_rows.append(product_row_data.get_product_data_dict())

        df = pandas.DataFrame(list_of_product_rows)
        self.cleaned_df = df

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

    def create_get_product_data_object(self, product_data, size, quantity):
        pass