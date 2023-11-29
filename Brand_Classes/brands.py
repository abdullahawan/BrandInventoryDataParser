import pathlib
import time

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
        self.brand_parse_type = ""
        self.cleaned_df = None

    def print_file_output(self):
        alert_msg(f"File: {self.output_file_name}.csv successfully created.\n\n")

    def create_set_file_output_name(self, order_id):
        # BRAND_OrderID_YYYY_MMM_DD_Shopify
        local_time = time.localtime()
        capitalized_brand_name = self.brand.strip().title()
        local_time_year = local_time.tm_year
        local_time_month = local_time.tm_mon
        local_time_day = local_time.tm_mday
        self.output_file_name = (f"{capitalized_brand_name}_{order_id}_{local_time_year}_{local_time_month}"
                                 f"_{local_time_day}_Shopify")

    def set_location_from_user(self, location_list):
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

    def execute_df_conversion(self):
        self.convert_to_dataframe()

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

        # convert to Data Frame and set self.cleaned_df
        df = pandas.DataFrame(list_of_product_rows)
        self.cleaned_df = df

    def convert_to_shopify_csv(self):
        # Create and set the file output for the object
        self.create_set_file_output_name(order_id=self.order_id)

        # convert cleaned data frame to csv
        self.cleaned_df.to_csv(path_or_buf=f"./Converted Inventory/{self.output_file_name}.csv",
                               index=False)

    def parse_file(self, file_name):
        excel = pandas.read_excel(io=f"./Inventory to Convert/{file_name}")
        for label, content in excel.iterrows():
            # Create a deep copy of the content data frame in which the original
            # data frame is not mutated
            content = content.copy(deep=True)

            # Check if style number exists as key in Dictionary
            if content["Style Number"] not in self.products:
                # Create and initiate empty list for the dictionary
                self.products[content["Style Number"]] = []

            # Execute the method to parse content values to dictionary
            product_info = self.parse_to_dictionary(content=content)

            # append product info to existing dictionary
            self.products[content["Style Number"]].append(product_info)

    def parse_csv_file(self, file_name):
        file_path = pathlib.Path(f"./Inventory to Convert/{file_name}")
        csv = pandas.read_csv(filepath_or_buffer=file_path)
        for label, content in csv.iterrows():
            # Create a deep copy of the content data frame in which the original
            # data frame is not mutated
            content = content.copy(deep=True)
            # Check if style number exists as key in Dictionary
            if content["Style Number"] not in self.products:
                # Create and initiate empty list for the dictionary
                self.products[content["Style Number"]] = []

            # Execute the method to parse content values to dictionary
            product_info = self.parse_to_dictionary(content=content)

            # append product info to existing dictionary
            self.products[content["Style Number"]].append(product_info)

    def set_size_and_quantities(self, product_size_qty_list):
        pass

    def parse_to_dictionary(self, content):
        pass

    def create_get_product_data_object(self, product_data, size, quantity):
        pass
