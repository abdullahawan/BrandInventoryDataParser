# PrivilegeSociety class file
import math

from Product import Product
from Brand_Classes.brands import Brands


class PrivilegeSociety(Brands):

    def __init__(self, order_id):
        super().__init__(order_id=order_id)
        self.brand = "Privilege Society"
        self.brand_parse_type = "Brand Boom"

    def create_get_product_data_object(self, product_data, size, quantity):
        product = Product(
                            handle=product_data["Name"],
                            title=product_data["Name"],
                            description=product_data["Description"],
                            location=self.location,
                            vendor=self.brand,
                            product_category=self.product_type_clothing,
                            option1_value=size,  # option 1 is Size by default,
                            option2_name=product_data["Color Heading"],
                            option2_value=product_data["Color"],  # there is no color or color value for Odd Sox
                            variant_sku=product_data["sku"],
                            var_inv_qty=quantity,
                            var_price=product_data["Retail Price"],
                            var_cost=product_data["Cost Price"],
                        )
        return product

    def parse_to_dictionary(self, content):
        # set all Nan cells (blank cells) to ""
        if type(content["Option Name"]) is float:
            if math.isnan(content["Option Name"]):
                content["Option Name"] = ""
                # if color value is "" then set color name to "" too
                content["Color Heading"] = ""
        else:
            content["Color Heading"] = "Color"

        if type(content["Description"]) is float:
            if math.isnan(content["Description"]):
                content["Description"] = ""

        product_info = {
            "sku": content["Style Number"],
            "Name": content["Product Name"].title(),
            "Description": content["Description"].capitalize().replace("*", ""),
            "Color": content["Option Name"].title(),
            "Color Heading": content["Color Heading"].title(),
            "Cost Price": content["Sale Price"],
            "Retail Price": content["MSRP"],
            "Sizes and Quantities": [{content["Size"]: content["QTY"]}]
            # size (string) : quantity (integer), Odd Sox sizes are only One Size "O/S"
        }

        # append finalized product_info dictionary to master dictionary
        return product_info
