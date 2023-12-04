# Hudson Outerwear class file
import math

from Product import Product
from Brand_Classes.brands import Brands


class HudsonOuterwear(Brands):

    def __init__(self, order_id):
        super().__init__(order_id=order_id)
        self.brand = "Hudson Outerwear"
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
                            var_barcode=product_data["Barcode"]
                        )
        return product

    def parse_to_dictionary(self, content):
        # set all Nan cells (blank cells) to ""
        if ")" in content["Product Name"]:
            prd_name = content["Product Name"].split(")")
            prd_name = prd_name[1].strip()
            content["Product Name"] = prd_name

        if type(content["Season"]) is float:
            if math.isnan(content["Season"]):
                content["Season"] = ""

        if type(content["Description"]) is float:
            if math.isnan(content["Description"]):
                content["Description"] = ""

        if type(content["Type"]) is float:
            if math.isnan(content["Type"]):
                content["Type"] = ""

        if type(content["UPC"]) is float:
            if math.isnan(content["UPC"]):
                content["UPC"] = ""

        product_info = {
            "sku": content["Style Number"],
            "Tag": content["Season"].title(),
            "Type": content["Type"].title(),
            "Name": content["Product Name"].replace("-"," ").title().strip().replace("xh", "XH"),
            "Description": content["Description"].capitalize().replace("*", ""),
            "Color": content["Option Name"].title(),
            "Cost Price": content["Sale Price"],
            "Retail Price": content["MSRP"],
            "Barcode": content["UPC"],
            "Sizes and Quantities": [{content["Size"]: content["QTY"]}]
            # size (string) : quantity (integer), Odd Sox sizes are only One Size "O/S"
        }

        # append finalized product_info dictionary to master dictionary
        return product_info
