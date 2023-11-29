# Affliction Clothing class file
import math

from Product import Product
from Brand_Classes.brands import Brands


class AfflictionClothing(Brands):

    def __init__(self, order_id):
        super().__init__(order_id=order_id)
        self.brand = "Affliction Clothing"
        self.brand_parse_type = "Brand Boom"

    def create_get_product_data_object(self, product_data, size, quantity):
        product = Product(
                            handle=product_data["Name"],
                            title=product_data["Name"],
                            product_type=product_data["Type"],
                            description=product_data["Description"],
                            location=self.location,
                            vendor=self.brand,
                            tags=product_data["Tag"],
                            product_category=self.product_type_clothing,
                            option1_value=size,  # option 1 is Size by default,
                            option2_value=product_data["Color"],  # there is no color or color value for Odd Sox
                            variant_sku=product_data["sku"],
                            var_inv_qty=quantity,
                            var_price=product_data["Retail Price"],
                            var_cost=product_data["Cost Price"],
                            var_barcode=product_data["Barcode"]
                        )
        return product

    def parse_to_dictionary(self, content):
        product_info = {
            "Type": content["Type"].title(),
            "Tag": content["Season"].split("-")[0].title().strip(),
            "sku": content["Style Number"],
            "Name": content["Product Name"].title(),
            "Description": content["Description"].capitalize(),
            "Color": content["Option Name"].title(),
            "Cost Price": content["Sale Price"],
            "Retail Price": content["MSRP"],
            "Barcode": content["UPC"],
            "Sizes and Quantities": [{content["Size"]: content["QTY"]}]
            # size (string) : quantity (integer), Odd Sox sizes are only One Size "O/S"
        }

        # append finalized product_info dictionary to master dictionary
        return product_info
