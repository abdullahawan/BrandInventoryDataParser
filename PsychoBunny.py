# Psycho Bunny class file
import math
import time

import pandas

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
                cleaned_handle = (product_data["Name"].replace(".", "")
                                  .replace("+", "")
                                  .replace("-", "")
                                  .replace("\'", "")
                                  .replace(" ", "-")
                                  .strip()
                                  .lower()
                                  )

                for product_with_sizes in product_data["Sizes and Quantities"]:
                    """
                        [
                            {size: quantity},
                            {size: quantity},
                            ...
                        ]
                    """
                    size = list(product_with_sizes)
                    size = str(size[0])
                    quantity = list(product_with_sizes.values())
                    quantity = quantity[0]

                    product_row_data = {
                        "Handle": cleaned_handle,
                        "Title": product_data["Name"],
                        "Body (HTML)": "",
                        "Description": product_data["Description"],
                        "Location": self.location,
                        "Vendor": self.brand,
                        "Tags": product_data["Tag"],
                        "Type": "",
                        "Product Category": self.product_type_clothing,
                        "Published": "false",
                        "status": "active",
                        "Option1 Name": "Size",
                        "Option1 Value": size,
                        "Option2 Name": "Color",
                        "Option2 Value": product_data["Color"],
                        "Option3 Name": "",
                        "Option3 Value": "",
                        "Variant SKU": product_data["sku"],
                        "Variant Grams": "0.0",
                        "HS Code": "",
                        "COO": "US",
                        "Variant Inventory Qty": quantity,
                        "Variant Inventory Policy": "deny",
                        "Variant Price": product_data["Retail Price"],
                        "Cost Per Item": product_data["Cost Price"],
                        "Variant Inventory Tracker": "shopify",
                        "Variant Fulfillment Service": "manual",
                        "Variant Requires Shipping": "false",
                        "Variant Taxable": "true",
                        "Variant Weight Unit": "lbs",
                        "Gift Card": "false",
                        "Status": "active"
                    }

                    # add the product row data to data frame
                    list_of_product_rows.append(product_row_data)

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
