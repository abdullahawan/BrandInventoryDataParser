
PRODUCTS_TO_CONVERT_PATH = "./Products to Convert"
CONVERTED_PRODUCTS_PATH = "./Converted Products"
CONVERTED_INVENTORY_PATH = "./Converted Inventory"
ARCHIVE_PATH = "./Archive"
ARCHIVED_PRODUCTS_PATH = "./Archive/Converted Products"
ARCHIVED_INVENTORY_PATH = "./Archive/Converted Inventory"

def alert_msg(msg):
    print(f"[!] {msg}")


def border(space_before=0):
    print(("\n"*space_before) + ("="*50))