#!/usr/bin/env python3

import os, csv, logging
# import json


#----------------------------------------------------------------------------------------
def fn_create_log_file_name(): 
    '''\n function fn_create_log_file_name() returns a log file name based on the name
 of the script. Example: script new_function.py returns log file name new_function.log\n'''
    # import os

    file_name = os.path.basename(__file__) # name of the current script without path -> new_function.py
    log_file_name = os.path.splitext(file_name)[0]  # os.path.splitext() is used to split the path name into a pair root and extension

    return log_file_name + '.log'
#----------------------------------------------------------------------------------------


#-------------------------------------------------------------------------
def fn_folder_exists_check(folder, f_path='.'):
    '''\n function checks if folder already exists, if not it is created\n'''
    from os import listdir, mkdir
    from os.path import isdir

    folder_content = listdir(f_path)
    folders = [item for item in folder_content if isdir(f_path+'\\'+item)]  #  list of folders in the specified directory

    if folder not in folders:
        mkdir(f_path + '\\' + folder)
#--------------------------------------------------------------------------------


#------------------------------------- logger setup -----------------------------------
fn_folder_exists_check('logs')  # 'logs' folder is created if it doesn't exist already
log_file_name = fn_create_log_file_name()
log_file_folder = '.\\logs\\'
log_file_path = log_file_folder + log_file_name

# logging setup 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(message)s')

# file handler saves log messages in the specified file
file_handler = logging.FileHandler(log_file_path, 'w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# stream handler sends log messages to the console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
#------------------------------------- end of logger setup -------------------------------------------


#----------------------------------------------------------------------------------------
def fn_list_of_files(path='.'):
    '''\nreturns a list of files in a folder (current folder if path isn't specified)\n'''
    # import os

    folder_content = os.listdir(path=path) # content of the folder including folders and files
    files = []

    for file in folder_content: # list of files only
        file_path = path + '\\' + file
        if os.path.isfile(file_path):
            files.append(file_path)

    return files
#----------------------------------------------------------------------------------------


#-------------------------------------------------------------------------
def fn_open_csv(file): 
    '''opens a csv file and returns the content as a list'''
    try:
        with open(file, 'r') as data_file:
            csv_object = csv.reader(data_file)
            csv_data = list(csv_object)
        return csv_data
    except FileNotFoundError as err:
        message1 = f'\n\n FILE NOT FOUND: {file}.'
        message2 = f' Press ENTER to exit.\n\n'
        logger.exception(err)
        logger.info(message1)
        input(message2)
        exit()
    except UnicodeDecodeError as err:
        message1 = f'\n WRONG FILE FORMAT (NOT CSV). FILE CAN\'T BE DECODED: {file}'
        message2 = f' Press ENTER to exit.\n\n'
        logger.exception(err)
        logger.info(message1)
        input(message2)
        exit()
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
def fn_save_csv(data, file): 
    '''\nsaves data from a list to a csv file\n'''
    try:
        with open (file, 'w', newline='') as outputfile:
            content = csv.writer(outputfile)
            for line in data:
                content.writerow(line)
    except:
        input(f'\n ERROR SAVING FILE: {file} ')
        exit()
#-------------------------------------------------------------------------


#--------------------------------------------------------------------------------
def fn_lowercase_strip(string):
    '''removes whitespace and converts the string to lowercase'''

    new_string = string.strip()
    new_string = new_string.lower()

    return new_string
#--------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------
def fn_remove_zeros(item_number):
    '''\n This function removes zeros at the beginning of a string. Examples:
    1. 00898708931x  ->  898708931x
    2. 000000000000385177097  ->  385177097\n'''

    while True:
        if item_number[0] != '0':
            break
        elif item_number[0] == '0':
            item_number = item_number[1:]

    return item_number
#----------------------------------------------------------------------------------------



# ----------- 1. we create a dictionary of items from a file exported from NAV -------------------------------------------
items_file = 'nav_items.csv'
items_data = fn_open_csv(items_file)[1:]  # we use [1:] to remove headers
items_dict = {}

for item in items_data:
    # No. - Description	- Blocked - Unit Cost   <-  column order
    item_number = item[0]
    item_number = fn_lowercase_strip(item_number) # all item numbers are converted to lowercase

    if not item_number:  # if item number is an empty cell we jump to the next item
        continue 

    title = item[1]
    blocked = item[2]
    unit_cost = item[3]
 
    items_dict[item_number] = {'title': title, 'blocked': blocked, 'unit_cost': unit_cost} # we add the item to items_dict, item_number is the key

    #  if item number start with zero we add it again with zeros removed from the beginning of the string:
    #  when csv file is opened in excel by double-clicking excel may convert item numbers to general type/number instead of text and remove zeros
    if item_number[0] == '0':
        item_number = fn_remove_zeros(item_number)
        items_dict[item_number] = {'title': title, 'blocked': blocked, 'unit_cost': unit_cost} # we add the item to items_dict, item_number is the key

del items_data

# with open('items.json', 'w') as file:
#     json.dump(items_dict, file, indent=2)
#-------------------------------------------------------------------------------------------------------------------------


# ----------- 2. we create a dictionary of barcodes from a file exported from NAV -------------------------------------------
barcodes_file = 'nav_barcodes.csv'
barcodes_data = fn_open_csv(barcodes_file)[1:]  # we use [1:] to remove headers
barcodes_dict = {}

for barcode in barcodes_data:
    # Item No. - Barcode No.   <-  column order
    item_number = barcode[0]
    item_number = fn_lowercase_strip(item_number) # all item numbers are converted to lowercase
    barcode_number = barcode[1]
    barcode_number = fn_lowercase_strip(barcode_number) # all barcode numbers are converted to lowercase

    if not barcode_number or not item_number:  # if barcode number or an item number is an empty cell we jump to the next line
        continue

    barcodes_dict[barcode_number] = item_number # we add the barcode to barcodes_dict

    #  if barcode number start with zero we add it again with zeros removed from the beginning of the string:
    #  when csv file is opened in excel by double-clicking excel may convert barcode numbers to general type/number instead of text and remove zeros
    if barcode_number[0] == '0':
        barcode_number = fn_remove_zeros(barcode_number)
        barcodes_dict[barcode_number] = item_number  # we add the barcode to barcodes_dict

del barcodes_data

# with open('barcodes.json', 'w') as file:
#     json.dump(barcodes_dict, file, indent=2)
#-------------------------------------------------------------------------------------------------------------------------


# ----------- 3. we match scannned item numbers to items exported from NAV -------------------------------------------
data_file = 'item_by_total_qty_by_location_merged.csv'
# data_file = 'item_by_total_qty_by_location_merged_test.csv'

# data = fn_open_csv(data_file)#[1:]
data_no_headers = fn_open_csv(data_file)[1:]

# data format:
# Item Number	Location	Total QTY in Location	  File Name
# 929650891	    33014	    34	                      scan01.csv

new_headers = ['Scanned No', 'Item No', 'Title', 'Location', 'Quantity', 'Blocked', 'Unit Cost', 'Filename']
identified_items = []
unidentified_items = []
unknowns = []
blocked_items = []
unknown = 'UNKNOWN'


for item in data_no_headers:

    continue_loop = True
    # logger.info(str(item))
    scanned_item_number = fn_lowercase_strip(item[0])
    item_number = fn_lowercase_strip(item[0])
    location = fn_lowercase_strip(item[1])
    quantity = fn_lowercase_strip(item[2])
    filename = fn_lowercase_strip(item[3])

    loop_check = 0

    while continue_loop:

        loop_check += 1

        if loop_check == 10: # check to avoid an infinite loop
            item_to_add = [scanned_item_number, unknown, unknown, location, quantity, unknown, unknown, filename]
            unknowns.append(item_to_add)
            break

        if loop_check <= 1:
            log_message = f'\n\n >>> searching for item: {item_number}\n'
            logger.info(log_message)
        elif loop_check > 1:
            log_message = f'     - searching for item: {item_number}'
            logger.info(log_message)


        # There only 2 options, item is either found or not found in items dict

        # -- STEP 1: CHECK IF SCANNED ITEM NUMBER CAN BE FOUND IN NAV ITEMS
        try: # item is found, if item doesn't exist then program will jump to except block
            items_dict[item_number]
            log_message = f'     - item {item_number} found in NAV items'
            logger.info(log_message)
            # format -> [scanned_item_number, item_number, title, location, quantity, blocked, unit_cost, filename]
            title = items_dict[item_number]['title']
            blocked = items_dict[item_number]['blocked']
            unit_cost = items_dict[item_number]['unit_cost']            

            item_to_add = [scanned_item_number, item_number, title, location, quantity, blocked, unit_cost, filename]

            if blocked.lower() == 'false' and 'blocked item' not in title.lower(): # item isn't blocked so it is saved to identified items
                identified_items.append(item_to_add)
                log_message = f'     - saving item {item_to_add[0:3]}'
                logger.info(log_message)
                continue_loop = False

            else: # item is blocked, we try to extract new item number from the description
                # descritption format -> 'BLOCKED ITEM USE  9781845962852'

                log_message = f'     - item {item_number} is BLOCKED'
                logger.info(log_message)

                # blocked_items.append(item)
                # continue_loop = False

                try: # we try to extract new item number for the blockd item and check if it is found in items
                    new_item_number = title.split()[-1]  # 'BLOCKED ITEM USE  9781845962852' -> '9781845962852' 
                    new_item_number = fn_lowercase_strip(new_item_number)
                    items_dict[new_item_number]  # if item doesn't exist we'll get a key error and jumt to except block

                    if new_item_number != item_number: # extracted number can't be the same, it will create an infinite loop
                        log_message = f'     - new item number found for the blocked item -> {new_item_number}'
                        logger.info(log_message)
                        item_number = new_item_number # we replace old item No with the new one and let the loop run again
                        continue # we jump back to the beginning of the while loop
                    else:
                        blocked_items.append(item_to_add)
                        continue_loop = False

                except: # we can't extract new item number or it doesn't exist, we save it to blocked items to be checked manually
                    blocked_items.append(item_to_add)
                    continue_loop = False
                    # log_message = f'  - new item number found for the blocked item -> {new_item_number}\n'
                    # logger.info(log_message)
         
        except: # item wasn't found in items dict

            log_message = f'     - item {item_number} NOT FOUND in NAV items'
            logger.info(log_message)

            try: # first we check if scanned number can be found in barcodes and if the barcode has assigned correct item number
                new_item_number = barcodes_dict[item_number] # we check if scanned number exists in barcodes

                log_message = f'     - item {item_number} found in NAV barcodes'
                logger.info(log_message)

                if new_item_number == item_number: # if barcode is the same as scanned number then item is unknown
                    
                    log_message = f'     - UNKNOWN ITEM. Item No: {item_number} the same as barcode No: {new_item_number} '
                    logger.info(log_message)
                   
                    item_to_add = [scanned_item_number, unknown, unknown, location, quantity, unknown, unknown, filename]
                    unknowns.append(item_to_add)
                    continue_loop = False

                else:
                    item_number = new_item_number

                    log_message = f'     - new item number found -> {new_item_number}'
                    logger.info(log_message)

                    continue

            except:
                log_message = f'     - item {item_number} NOT FOUND in NAV barcodes'
                logger.info(log_message)
                log_message = f'     - Saving UNKNOWN ITEM {item_number}'
                logger.info(log_message)

                item_to_add = [scanned_item_number, unknown, unknown, location, quantity, unknown, unknown, filename]
                unknowns.append(item_to_add)
                continue_loop = False

   
print('\n original data:', len(data_no_headers))
print(' identified_items:', len(identified_items))
print(' unknown_items:', len(unknowns))
print(' blocked_items:', len(blocked_items))
check = len(identified_items) + len(unknowns) + len(blocked_items)
print(' check:', check, check == len(data_no_headers))

if unknowns:
    final_unknows_list = [new_headers]
    final_unknows_list.extend(unknowns)
    fn_save_csv(final_unknows_list, 'output_unknown_items.csv')

if blocked:
    final_blocked_items_list = [new_headers]
    final_blocked_items_list.extend(blocked_items)
    fn_save_csv(final_blocked_items_list, 'output_blocked_items.csv')

final_list = [new_headers]   
final_list.extend(unknowns)
final_list.extend(blocked_items)
final_list.extend(identified_items)
fn_save_csv(final_list, 'output_matched_items.csv')

print('\n original data:', len(data_no_headers))
print(' final list:', len(final_list) - 1)
print(' check:', len(data_no_headers) == len(final_list) - 1)

input('PRESS ENTER TO EXIT...')