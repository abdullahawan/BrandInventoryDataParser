#!/usr/bin/env python3
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
from GeneralMethods import alert_msg

BRAND_LIST = ["Ksubi", "Psycho Bunny"]
LOCATIONS = ["14469", "Fairlane", "Corp Registered"]


def cleanup_folder():
    print("Please choose one of the following folders to clean")
    folder_list = ["./Converted Inventory", "./Inventory to Convert"]
    counter = 0

    for folder in folder_list:
        print(f"{counter} - {folder}")
        counter += 1

    user_folder = int(input("Enter the index of the folder to cleanup:"))
    folder = folder_list[user_folder]
    while folder not in folder_list:
        print("[!] Incorrect index received... please enter the correct index of folder:")
        user_file = input()

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
    continue_program_flag = True

    while continue_program_flag:
        # Welcome Message + Warning
        alert_msg("Please ensure all Excel files are closed")
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

            user_file_to_convert_index = int(input("Enter the index of the file you choose to convert: "))
        else:
            alert_msg("No inventory files in folder")
            alert_msg("Exiting program...")
            exit(0)

        # Save file name in local variable
        file = list_of_inventory_to_convert[user_file_to_convert_index]

        # # Get Brand from User
        # counter = 0
        # for brand in BRAND_LIST:
        #     print(f"{counter} - {brand}")
        #     counter += 1
        #
        # # Get the index of the brand user wants to convert
        # user_brand_index = int(input("Enter the index of the brand you want to convert: "))

        # Output current task to user:
        alert_msg("Parsing file name")

        # Parse the file name string and get the brand_name and order_id as a tuple
        brand_name, order_id = parse_file_name(file=file)

        # clean up brand_name string
        brand_name = brand_name.strip().title()

        # Output current task to user:
        alert_msg("Retrieved brand name and order id from file")
        alert_msg(f"Brand: {brand_name} \nOrder_ID: {order_id}")

        # Outer scoped Brand class variable
        # Output current task to user:
        alert_msg("Creating Brand Object...")
        brand = None
        match brand_name:
            case "Ksubi":
                # brand = Ksubi()
                pass
            case "Psycho Bunny":
                brand = PsychoBunny(order_id=order_id)
            case _:
                print("Brand did not exist")
                exit(1)

        # Output current task to user:
        alert_msg("Created Brand Object")

        alert_msg("Parsing File...")
        brand.parse_file(list_of_inventory_to_convert[user_file_to_convert_index])

        alert_msg("Retrieving location from User...")
        brand.get_location_from_user(LOCATIONS)

        alert_msg("Converting file data to Shopify data frame...")
        brand.convert_to_dataframe()

        alert_msg("Exporting to CSV file...")
        brand.convert_to_shopify_csv()

        # Ask user if they want to clean up any folder
        print("Would you like to cleanup either of the folders?")
        user_cleanup_choice = input("y/n: ")
        user_cleanup_choice = user_cleanup_choice.lower().strip()

        # if choice does not start with 'y' or 'n' then loop since input is incorrect
        # while user_cleanup_choice != 'y' or user_cleanup_choice != 'n':
        #     print("Incorrect value received, please input either 'y' or 'n':")
        #     user_cleanup_choice = input("y/n: ").lower().strip()

        if user_cleanup_choice.startswith('y'):
            cleanup_folder()

        # Ask user if they want to execute the program again
        print("Would you like to run the program again? y/n: ")
        user_program_choice = input()
        user_program_choice = user_program_choice.lower().strip()

        if user_program_choice.startswith('n'):
            continue_program_flag = False

    # Program has completed and is exiting
    alert_msg("Completed program execution... program exiting...")