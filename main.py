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
import time
import shutil
import pandas

from Brand_Classes.AfflictionClothing import AfflictionClothing
from Brand_Classes.Cavit import Cavit
from Brand_Classes.CityLab import CityLab
from Brand_Classes.Cult import Cult
from Brand_Classes.DoctrineDenim import DoctrineDenim
from Brand_Classes.EmbellishNYC import EmbellishNYC
from Brand_Classes.HVMan import HVMan
from Brand_Classes.HudsonOuterwear import HudsonOuterwear
from Brand_Classes.Ksubi import Ksubi
from Brand_Classes.MVDadHats import MVDadHats
from Brand_Classes.OddSox import OddSox
from Brand_Classes.PRPS import PRPS
from Brand_Classes.PrivilegeSociety import PrivilegeSociety
from Brand_Classes.ProStandard import ProStandard
from Brand_Classes.PsychoBunny import PsychoBunny
from Brand_Classes.RobertVinoMilano import RobertVinoMilano
from Brand_Classes.SIW import SIW
from Brand_Classes.XHostile import XHostile
from GeneralMethods import *
from Inventory import Inventory

# BRAND_LIST = ["Ksubi", "Psycho Bunny"]
LOCATIONS = ["14469", "Fairlane", "Corp Registered"]


def convert_product_to_inventory_file(merged_inv_list):
    # for each shopify product template create/export an updated inventory file
    for file in os.listdir(path=CONVERTED_PRODUCTS_PATH):
        inventory = Inventory(file)

        # parse csv
        inventory.parse_product_csv()

        # convert to Data Frame
        inventory.convert_to_inv_dataframe()

        # export to shopify
        inventory.convert_to_shopify_csv()

        # Get the cleaned list of product inventory date
        inv_list = inventory.get_product_inventory_list()

        # extend the passed in merged_inv_list
        merged_inv_list.extend(inv_list)


def create_master_csv_file(merged_product_list, merged_inv_list):
    border(space_before=2)
    print("Do you want to combine all of the updated inventory and/or products into one file? (Default is yes)")
    user_inv_join_choice = input("y/n: ").lower().strip()

    if user_inv_join_choice.startswith('n'):
        alert_msg("You've chosen not to join any file")
        return

    print("""
    Would you like to combine (default is Both (2)): 
    0) Products 
    1) Inventory
    2) Both
    
    """)
    user_folder_choice = input()

    folder = ""
    if user_folder_choice == '0':
        folder = "Converted Products"
        export_merged_list_to_csv(merged_product_list, folder)
    elif user_folder_choice == '1':
        folder = "Converted Inventory"
        export_merged_list_to_csv(merged_inv_list, folder)
    else:
        folder = "Converted Products"
        export_merged_list_to_csv(merged_product_list, folder)

        folder = "Converted Inventory"
        export_merged_list_to_csv(merged_inv_list, folder)

    border()


def export_merged_list_to_csv(data_list, folder):
    # create data frame
    merged_df = pandas.DataFrame(data_list)

    # set file string
    file_end_string = ""
    if "Inventory" in folder:
        file_end_string = "_Inventory"

    local_time = time.localtime()

    # export data frame to csv
    merged_df.to_csv(path_or_buf=f"./{folder}/"
                                 f"{local_time.tm_year}_{local_time.tm_mon}_{local_time.tm_mday}"
                                 f"_Shopify{file_end_string}.csv",
                     index=False)


def cleanup_folders():
    alert_msg("Force cleaning all files within 'Converted Inventory' and 'Converted Products'...")
    folder_list = ["Converted Products", "Converted Inventory"]

    for folder in folder_list:
        alert_msg(f"Removing the following files from folder {folder}:")
        for file in os.listdir(folder):
            print(f"-- {file}")

        for file in os.listdir(folder):
            if "Product" in folder:
                # If product folder then move files to product archive
                shutil.move(src=f"{CONVERTED_PRODUCTS_PATH}/{file}", dst=f"{ARCHIVED_PRODUCTS_PATH}/{file}")
            elif "Inventory" in folder:
                # Else if it's the Inventory folder, move files to inventory archive
                shutil.move(src=f"{CONVERTED_INVENTORY_PATH}/{file}", dst=f"{ARCHIVED_INVENTORY_PATH}/{file}")

        alert_msg(f"Completed folder {folder} cleanup... Files moved to archive")


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

    # Check if Input folder exists
    if "Products to Convert" not in list_of_dir:
        # create if it doesn't exist
        os.mkdir(path=PRODUCTS_TO_CONVERT_PATH)

    # Check if output folder exists
    if "Converted Products" not in list_of_dir:
        # create if it doesn't exist
        os.mkdir(path=CONVERTED_PRODUCTS_PATH)

    # check if inventory output folder exists
    if "Converted Inventory" not in list_of_dir:
        # create if it doesn't exist
        os.mkdir(path=CONVERTED_INVENTORY_PATH)

    # check if archive folder exists
    if "Archive" not in list_of_dir:
        # create
        os.mkdir(path=ARCHIVE_PATH)

    # check if archived Converted Products exists at the deeper archive level
    archive_dir = os.listdir(path=ARCHIVE_PATH)

    if "Converted Products" not in archive_dir:
        # create
        os.mkdir(path=ARCHIVED_PRODUCTS_PATH)

    if "Converted Inventory" not in archive_dir:
        # create
        os.mkdir(path=ARCHIVED_INVENTORY_PATH)

    # Ask user if they want to clean up any folder
    border(space_before=2)
    print("Would you like to cleanup the output folders?")
    user_cleanup_choice = input("y/n: ")
    user_cleanup_choice = user_cleanup_choice.lower().strip()

    if user_cleanup_choice.startswith('y'):
        cleanup_folders()
    border()

    # Get list of files in "Inventory to Convert"
    list_of_inventory_to_convert = os.listdir(path=PRODUCTS_TO_CONVERT_PATH)

    # List of output file names
    created_files = []

    # Create empty list for merged product data
    merged_product_list = []

    border(space_before=2)
    # Loop through all files in the inventory to convert folder
    for inv_file in list_of_inventory_to_convert:
        # Parse the file name string and get the brand_name and order_id as a tuple
        brand_name, order_id = parse_file_name(file=inv_file)

        # clean up brand_name string
        brand_name = brand_name.strip()

        # Output current task to user:
        alert_msg("Retrieved brand name and order id from file")
        print(f"Brand: {brand_name} \nOrder_ID: {order_id}")

        # Outer scoped Brand class variable
        brand = None
        match brand_name:
            case "Affliction Clothing":
                brand = AfflictionClothing(order_id=order_id)
            case "City Lab":
                brand = CityLab(order_id=order_id)
            case "Cavit":
                brand = Cavit(order_id=order_id)
            case "Cult" | "Cult Of Individuality":
                brand = Cult(order_id=order_id)
            case "Doctrine Denim":
                brand = DoctrineDenim(order_id=order_id)
            case "Embellish" | "Embellish NYC":
                brand = EmbellishNYC(order_id=order_id)
            case "Hudson" | "Hudson Outerwear":
                brand = HudsonOuterwear(order_id=order_id)
            case "HVMan":
                brand = HVMan(order_id=order_id)
            case "Ksubi":
                brand = Ksubi(order_id=order_id)
            case "MV Dad Hats":
                brand = MVDadHats(order_id=order_id)
            case "Odd Sox":
                brand = OddSox(order_id=order_id)
            case "Privilege Society":
                brand = PrivilegeSociety(order_id=order_id)
            case "Pro Standard":
                brand = ProStandard(order_id=order_id)
            case "PRPS":
                brand = PRPS(order_id=order_id)
            case "Psycho Bunny":
                brand = PsychoBunny(order_id=order_id)
            case "Milano":
                brand = RobertVinoMilano(order_id=order_id)
            case "SIW":
                brand = SIW(order_id=order_id)
            case "XHostile":
                brand = XHostile(order_id=order_id)
            case _:  # default case, brand does not exist
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

        # append product data to merged product data list
        merged_product_list.extend(brand.get_product_row_list())

        # append brand output file name to list of created files
        created_files.append(brand.output_file_name)

    # Output list all files created
    border()
    print("Successfully created the following files:")
    for file in created_files:
        print(file + ".csv")
    border()

    merged_inv_list = []

    border(space_before=2)
    print("Converting created product files to inventory files")
    convert_product_to_inventory_file(merged_inv_list)

    alert_msg("Created inventory files...")
    for file in created_files:
        print(file + "_Inventory.csv")
    border()

    # Ask user if they want a master Inventory file and convert to master file
    create_master_csv_file(merged_product_list=merged_product_list, merged_inv_list=merged_inv_list)

    # Program has completed and is exiting
    alert_msg("Completed program execution... program exiting...")
