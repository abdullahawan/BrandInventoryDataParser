# SIW class file

from Product import Product
from Brand_Classes.brands import Brands


class SIW(Brands):

    def __init__(self, order_id):
        super().__init__(order_id=order_id)
        self.brand = "SIW"
        self.brand_parse_type = "Brand Boom"

    def create_get_product_data_object(self, product_data, size, quantity):
        product = Product(
                            handle=product_data["Name"],
                            title=product_data["Name"],
                            description=product_data["Description"],
                            location=self.location,
                            vendor=self.brand,
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
            "Type": str(content["Category"]).title(),
            "sku": content["Style Number"],
            "Name": content["Product Name"].title(),
            "Description": content["Product Name"].capitalize(),
            "Color": content["Option Name"].title(),
            "Cost Price": content["Sale Price"],
            "Retail Price": content["MSRP"],
            "Sizes and Quantities": [{content["Size"]: content["QTY"]}]  # size (string) : quantity (integer)
        }

        # append finalized product_info dictionary to master dictionary
        return product_info
