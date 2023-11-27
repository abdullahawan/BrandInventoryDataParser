
"""
This program is meant to convert NuOrder and BrandBoom Order sheets to Shopify Inventory
Templates

Larger purposes of the application
1) Check if the relevant folders/files exist
2) Let the user choose the file that they want to convert
    2a) The output folder should exist, if it doesn't create it
3) Let the user choose the output file name (automate this)
    3a) Output the list of files with names and indexes, user should be able to choose the index
        of the file they want
    3a) Automate by doing the following format BRAND_YYYY_MMM_DD_Shopify
4) Automatically determine the brand and parse based off the brand's specific output format

Brand Parsing:
Brand Class:
    - Each brand has its own parsing ability inherited from a general parent
    - Should have a method to convert to shopify format


File Methods

os.mkdir(path) - create the file
os.listdir(path=".") - Returns List contianing the names of entries in the directory given by path argument



"""
import os

from PsychoBunny import PsychoBunny

BRAND_LIST = ["Ksubi", "Psycho Bunny"]
LOCATIONS = ["14469", "Fairlane", "Corp Registered"]

if __name__ == '__main__':
    # Welcome Message + Warning
    print("[!] Please ensure all Excel files are closed")

    # Get list of files/folders in directory
    list_of_dir = os.listdir()

    # Check if output folder exists
    if "Converted Inventory" not in list_of_dir:
        os.mkdir(path="./Converted Inventory")

    # Check if Input folder exists
    if "Inventory to Convert" not in list_of_dir:
        os.mkdir(path="./Inventory to Convert")

    # Get list of files in "Inventory to Convert"
    list_of_inventory_to_convert = os.listdir(path="./Inventory to Convert")

    if list_of_inventory_to_convert:
        counter = 0
        for list_of_inventory in list_of_inventory_to_convert:
            print(f"{counter} - {list_of_inventory}")
            counter += 1

        user_file_to_convert_index = int(input("Enter the index of the file you choose to convert:"))
    else:
        print("[!] No inventory files in folder")
        print("[!] Exiting program...")
        exit(0)

    # Get Brand from User
    counter = 0
    for brand in BRAND_LIST:
        print(f"{counter} - {brand}")
        counter += 1

    # delete counter?
    # del counter

    # Get the index of the brand user wants to convert
    user_brand_index = int(input("Enter the index of the brand you want to convert: "))

    # Outer scoped Brand class variable
    brand = None
    match BRAND_LIST[user_brand_index]:
        case "Ksubi":
            # brand = Ksubi()
            pass
        case "Psycho Bunny":
            brand = PsychoBunny()
        case _:
            print("Brand did not exist")
            exit(1)

    brand.parse_file(list_of_inventory_to_convert[user_file_to_convert_index])
    brand.get_location_from_user(LOCATIONS)
    brand.convert_to_dataframe()
    brand.convert_to_shopify_csv()
