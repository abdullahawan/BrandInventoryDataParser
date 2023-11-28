# Ksubi class file
import math

from Product import Product
from Brand_Classes.brands import Brands


class Ksubi(Brands):

    def __init__(self, order_id):
        super().__init__(order_id=order_id)
        self.brand = "Ksubi"
        self.brand_parse_type = "NuOrder"

    def create_get_product_data_object(self, product_data, size, quantity):
        product = Product(
                            handle=product_data["Name"],
                            title=product_data["Name"],
                            description=product_data["Description"],
                            product_type=product_data["Type"],
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
        return product

    def parse_to_dictionary(self, content):
        product_info = {
            "Tag": content["Season"].title(),
            "sku": content["Style Number"],
            "Type": content["Subcategory"].title(),
            "Name": content["Name"].title(),
            "Description": content["Description"].capitalize(),
            "Color": content["Color"].title(),
            "Cost Price": content["Wholesale (USD)"],
            "Retail Price": round(content["Wholesale (USD)"] * 1.5, 2),  # confirm this
            "Sizes and Quantities": []  # size (string) : quantity (integer)
        }

        # Assume size and quantity range is 1-8 (inclusive) for all exported templates
        bottom_size_list = list(range(28, 43))  # 28 - 42 (inclusive)
        top_size_list = ["XS", "S", "M", "L", "XL", "2XL"]
        size_list = bottom_size_list + top_size_list

        for size in size_list:
            # append list of size and quantity to product info dictionary
            current_quantity = None
            try:
                # if Key exists then assign it to a variable
                current_quantity = content[f"{size}"]

                if math.isnan(current_quantity):
                    # check if the quantity cell is empty
                    pass
                else:
                    # if cell is not empty (existing quantity) then add to size and quantities list
                    product_info["Sizes and Quantities"].append({size: current_quantity})
            except KeyError:
                # If key doesn't exist then skip this iteration
                pass

        # append finalized product_info dictionary to master dictionary
        return product_info
