# Odd Sox class file

from Product import Product
from Brand_Classes.brands import Brands


class OddSox(Brands):

    def __init__(self, order_id):
        super().__init__(order_id=order_id)
        self.brand = "Odd Sox"
        self.brand_parse_type = "Brand Boom"

    def create_get_product_data_object(self, product_data, size, quantity):
        product = Product(
                            handle=product_data["Name"],
                            title=product_data["Name"],
                            description=product_data["Description"],
                            location=self.location,
                            vendor=self.brand,
                            tags=product_data["Tag"],
                            product_category=self.product_type_clothing,
                            option1_value=size,  # option 1 is Size by default,
                            option2_name="",  # there is no color or color value for Odd Sox
                            variant_sku=product_data["sku"],
                            var_inv_qty=quantity,
                            var_price=product_data["Retail Price"],
                            var_cost=product_data["Cost Price"],
                            var_barcode=product_data["Barcode"]
                        )
        return product

    def parse_to_dictionary(self, content):
        product_info = {
            "Type": str(content["Type"]).title(),
            "Tag": content["Season"],
            "sku": content["Style Number"],
            "Name": content["Product Name"].title(),
            "Description": content["Product Name"].capitalize(),
            "Cost Price": content["Sale Price"],
            "Retail Price": round(content["Sale Price"] * 2.165, 2),  # retail price / cost = 2.165 x,
            "Barcode": content["UPC"],
            "Sizes and Quantities": [{"O/S": content["QTY"]}]
            # size (string) : quantity (integer), Odd Sox sizes are only One Size "O/S"
        }

        # append finalized product_info dictionary to master dictionary
        return product_info
