#!/usr/bin/env python3
"""
This program is meant to convert NuOrder and BrandBoom Order sheets to Shopify Inventory
Templates

Larger purposes of the application
1) Check if the relevant folders/files exist
2) If the input and output folders don't exist, create them
3) Automatically scrape the brand and order id information from the file name
    3a) file name should be in format BRAND_ORDERID.xlsx or BRAND_ORDERID.csv
4) Automatically determine the brand and parse based off the brand's specific output format
5) Convert to data frame
6) Export to Shopify csv format

Brand Parsing:
Brand Class:
    - Each brand has its own parsing ability inherited from a general parent
    - Should have a method to convert to shopify format

File Methods

os.mkdir(path) - create the file
os.listdir(path=".") - Returns List containing the names of entries in the directory given by path argument
"""

import os

from Brand_Classes.CityLab import CityLab
from Brand_Classes.Cult import Cult
from Brand_Classes.Ksubi import Ksubi
from Brand_Classes.PsychoBunny import PsychoBunny
from Brand_Classes.RobertVinoMilano import RobertVinoMilano
from GeneralMethods import alert_msg

# BRAND_LIST = ["Ksubi", "Psycho Bunny"]
LOCATIONS = ["14469", "Fairlane", "Corp Registered"]


def cleanup_folder():
    print("Please choose one of the following folders to clean")
    folder_list = ["Converted Inventory", "Inventory to Convert"]
    counter = 0

    for folder in folder_list:
        print(f"{counter} - {folder}")
        counter += 1

    user_folder = int(input("Enter the index of the folder to cleanup:"))
    folder = folder_list[user_folder]
    while folder not in folder_list:
        print("[!] Incorrect index received... please enter the correct index of folder:")
        user_folder = input()

    print(f"Removing the following files:")
    for file in os.listdir(folder):
        print(f"-- {file}")

    for file in os.listdir(folder):
        os.remove(f"./{folder}/{file}")

    print(f"[!] Completed folder {folder} cleanup...")


def parse_file_name(file):
    file_string = file.split("_") # file should be in BRAND_ORDERID.xlsx format
    brand_name = file_string[0]

    order_id = file_string[1]
    order_id = order_id.split(".")
    order_id = order_id[0]

    return brand_name, order_id


if __name__ == '__main__':
    # Welcome Message + Warning
    alert_msg("Please ensure all Excel files are closed")

    # Get list of files/folders in directory
    list_of_dir = os.listdir()

    # Check if output folder exists
    if "Converted Inventory" not in list_of_dir:
        # create if it doesn't exist
        os.mkdir(path="./Converted Inventory")

    # Check if Input folder exists
    if "Inventory to Convert" not in list_of_dir:
        # create if it doesn't exist
        os.mkdir(path="./Inventory to Convert")

    # Get list of files in "Inventory to Convert"
    list_of_inventory_to_convert = os.listdir(path="./Inventory to Convert")

    # List of output file names
    created_files = []

    # Loop through all files in the inventory to convert folder
    for inv_file in list_of_inventory_to_convert:
        # Parse the file name string and get the brand_name and order_id as a tuple
        brand_name, order_id = parse_file_name(file=inv_file)

        # clean up brand_name string
        brand_name = brand_name.strip().title()

        # Output current task to user:
        alert_msg("Retrieved brand name and order id from file")
        print(f"Brand: {brand_name} \nOrder_ID: {order_id}")

        # Outer scoped Brand class variable
        brand = None
        match brand_name:
            case "City Lab":
                brand = CityLab(order_id=order_id)
            case "Cult" | "Cult of Individuality":
                brand = Cult(order_id=order_id)
            case "Ksubi":
                brand = Ksubi(order_id=order_id)
                pass
            case "Psycho Bunny":
                brand = PsychoBunny(order_id=order_id)
            case "Milano":
                brand = RobertVinoMilano(order_id=order_id)
            case _: # default case, brand does not exist
                print("Brand did not exist")
                exit(1)

        alert_msg("Parsing File...")
        match brand.brand_parse_type:
            case "NuOrder":
                brand.parse_file(file_name=inv_file)
            case "Brand Boom":
                brand.parse_csv_file(file_name=inv_file)

        alert_msg("Retrieving location from User...")
        brand.set_location_from_user(LOCATIONS)
        brand.convert_to_dataframe()

        alert_msg("Exporting to CSV file...")
        brand.convert_to_shopify_csv()

        brand.print_file_output()

        # append brand output file name to list of created files
        created_files.append(brand.output_file_name)

    # Ask user if they want to clean up any folder
    print("Would you like to cleanup either of the folders?")
    user_cleanup_choice = input("y/n: ")
    user_cleanup_choice = user_cleanup_choice.lower().strip()

    if user_cleanup_choice.startswith('y'):
        cleanup_folder()

    # Output list all files created
    print("="*50)
    print("Successfully created the following files:")
    for file in created_files:
        print(file)
    print("="*50)

    # Program has completed and is exiting
    alert_msg("Completed program execution... program exiting...")
