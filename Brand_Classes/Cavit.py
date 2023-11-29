# Cavit class file
import math

from Product import Product
from Brand_Classes.brands import Brands


class Cavit(Brands):

    def __init__(self, order_id):
        super().__init__(order_id=order_id)
        self.brand = "Cavit"
        self.brand_parse_type = "Brand Boom"

    def create_get_product_data_object(self, product_data, size, quantity):
        product = Product(
                            handle=product_data["Name"],
                            title=product_data["Name"],
                            description=product_data["Description"],
                            location=self.location,
                            vendor=self.brand,
                            product_type=product_data["Type"],
                            tags=product_data["Tag"],
                            product_category=self.product_type_clothing,
                            option1_value=size,  # option 1 is Size by default,
                            option2_value=product_data["Color"],  # there is no color or color value for Odd Sox
                            variant_sku=product_data["sku"],
                            var_inv_qty=quantity,
                            var_price=product_data["Retail Price"],
                            var_cost=product_data["Cost Price"],
                        )
        return product

    def parse_to_dictionary(self, content):
        product_info = {
            "sku": content["Style Number"],
            "Tag": content["Season"].title(),
            "Type": content["Category"].title(),
            "Name": content["Product Name"].title(),
            "Description": content["Description"].capitalize().replace("*", ""),
            "Color": content["Option Name"].title(),
            "Cost Price": content["Sale Price"],
            "Retail Price": content["MSRP"],
            "Sizes and Quantities": [{content["Size"]: content["QTY"]}]
            # size (string) : quantity (integer), Odd Sox sizes are only One Size "O/S"
        }

        # append finalized product_info dictionary to master dictionary
        return product_info
