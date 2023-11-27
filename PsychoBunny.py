# Psycho Bunny class file
import math
import time
import pandas

from Product import Product
from brands import Brands


class PsychoBunny(Brands):

    def __init__(self):
        super().__init__()
        self.brand = "Psycho Bunny"
        # BRAND_YYYY_MMM_DD_Shopify
        local_time = time.localtime()
        capitalized_brand_name = self.brand.strip().upper()
        local_time_year = local_time.tm_year
        local_time_month = local_time.tm_mon
        local_time_day = local_time.tm_mday
        self.output_file_name = (f"{capitalized_brand_name}_{local_time_year}_{local_time_month}"
                                 f"_{local_time_day}_Shopify")

    def convert_to_dataframe(self):
        # create empty list for dictionaries
        list_of_product_rows = []
        for _, product in self.products.items():
            for product_data in product:
                for product_with_sizes in product_data["Sizes and Quantities"]:
                    # get the size and quantity data from the dict contained within the list
                    size = self.get_size_from_product_dict(product_dict=product_with_sizes)
                    quantity = self.get_quantity_from_product_dict(product_dict=product_with_sizes)

                    product_row_data = Product(
                        handle=product_data["Name"],
                        title=product_data["Name"],
                        description=product_data["Description"],
                        location=self.location,
                        vendor=self.brand,
                        tags=product_data["Tag"],
                        product_category=self.product_type_clothing,
                        option1_value=size,  # option 1 is Size by default
                        option2_value=product_data["Color"],  # option 2 is Color by default
                        variant_sku=product_data["sku"],
                        var_inv_qty=quantity,
                        var_price=product_data["Retail Price"],
                        var_cost=product_data["Cost Price"]
                    )

                    # Get the dictionary from the class and overwrite the variable and
                    # add the product row data to data frame
                    list_of_product_rows.append(product_row_data.get_product_data_dict())

        df = pandas.DataFrame(list_of_product_rows)
        self.cleaned_df = df

    def parse_to_dictionary(self, content):
        # Build Value dictionary
        if "REPLENISHMENT" in content["Season"]:
            content["Season"] = ""

        product_info = {
            "Tag": content["Season"],
            "sku": content["Style Number"],
            "Name": content["Description"],
            "Description": content["Description"],
            "Color": content["Color"],
            "Cost Price": content["Wholesale (USD)"],
            "Retail Price": content["M.S.R.P (USD)"],
            "Sizes and Quantities": []  # size (string) : quantity (integer)
        }

        # Assume size and quantity range is 1-8 (inclusive) for all exported templates
        size_list = range(1, 9)  # 1 - 8 (inclusive)

        for size in size_list:
            # append list of size and quantity to product info dictionary
            current_quantity = content[f"Qty {size}"]
            if math.isnan(current_quantity):
                pass
            else:
                product_info["Sizes and Quantities"].append({content[f"Size {size}"]: current_quantity})

        # append finalized product_info dictionary to master dictionary
        return product_info

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
