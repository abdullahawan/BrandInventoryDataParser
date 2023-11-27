# Product row data class

class Product:
    def __init__(self,
                 handle="",
                 title="",
                 body_html="",
                 description="",
                 location="",
                 vendor="",
                 tags="",
                 product_type="",
                 product_category="",
                 published="false",
                 option1_name="Size",
                 option1_value="",
                 option2_name="Color",
                 option2_value="",
                 option3_name="",
                 option3_value="",
                 variant_sku="",
                 variant_grams=0.0,
                 hs_code="",
                 coo="US",
                 var_inv_qty=0,
                 var_inv_policy="deny",
                 var_price=0,
                 var_cost=0,
                 var_inv_tracker="shopify",
                 var_fulfillment_service="manual",
                 var_req_shipping="false",
                 var_taxable="true",
                 var_weight_unit="lbs",
                 gift_card="false",
                 status="active"
                 ):
        self.product_data = {
            "Handle": handle,
            "Title": title,
            "Body (HTML)": body_html,
            "Description": description,
            "Location": location,
            "Vendor": vendor,
            "Tags": tags,
            "Type": product_type,
            "Product Category": product_category,
            "Published": published,
            "Option1 Name": option1_name,
            "Option1 Value": option1_value,
            "Option2 Name": option2_name,
            "Option2 Value": option2_value,
            "Option3 Name": option3_name,
            "Option3 Value": option3_value,
            "Variant SKU": variant_sku,
            "Variant Grams": variant_grams,
            "HS Code": hs_code,
            "COO": coo,
            "Variant Inventory Qty": var_inv_qty,
            "Variant Inventory Policy": var_inv_policy,
            "Variant Price": var_price,
            "Cost Per Item": var_cost,
            "Variant Inventory Tracker": var_inv_tracker,
            "Variant Fulfillment Service": var_fulfillment_service,
            "Variant Requires Shipping": var_req_shipping,
            "Variant Taxable": var_taxable,
            "Variant Weight Unit": var_weight_unit,
            "Gift Card": gift_card,
            "Status": status
        }

        # Execute the creation, cleanup/modification of data method
        self.execute_product_creation_methods()

    def execute_product_creation_methods(self):
        self.update_product_handle()

    def update_product_handle(self):
        cleaned_handle = (self.product_data["Handle"].replace(".", "")
                          .replace("+", "")
                          .replace("-", "")
                          .replace("\'", "")
                          .replace(" ", "-")
                          .strip()
                          .lower()
                          )
        self.update_product_data(column="Handle", data=cleaned_handle)

    def update_product_data(self, column, data):
        self.product_data[column] = data

    def get_product_data_dict(self):
        return self.product_data
