#!/usr/bin/env python3

import os, csv, logging
import json


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

with open('items.json', 'w') as file:
    json.dump(items_dict, file, indent=2)
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

with open('barcodes.json', 'w') as file:
    json.dump(barcodes_dict, file, indent=2)
#-------------------------------------------------------------------------------------------------------------------------


# ----------- 3. we match scannned item numbers to items exported from NAV -------------------------------------------
# data_file = 'item_by_total_qty_by_location_merged.csv'
data_file = 'item_by_total_qty_by_location_merged_test.csv'

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


# -- STEP 1: CHECK IF SCANNED ITEM NUMBER CAN BE FOUND IN NAV ITEMS



for item in data_no_headers:

    continue_loop = True
    logger.info(str(item))
    scanned_item_number = item[0]
    item_number = item[0]

    while continue_loop:

        log_message = f'\n\n >>> searching for item -> {scanned_item_number}\n'
        logger.info(log_message)

        # There only 2 options, item is either found or not found in items dict

        try: # item is found, if item doesn't exist then program will jump to except block
            items_dict[item_number]
            log_message = f'  - item {item_number} found in NAV items\n'
            logger.info(log_message)
            # format -> [scanned_item_number, item_number, title, location, quantity, blocked, unit_cost, filename]
            title = items_dict[item_number]['title']
            location = fn_lowercase_strip(item[1])
            quantity = fn_lowercase_strip(item[2])
            blocked = items_dict[item_number]['blocked']
            unit_cost = items_dict[item_number]['unit_cost']
            filename = fn_lowercase_strip(item[3])

            item_to_add = [scanned_item_number, item_number, title, location, quantity, blocked, unit_cost, filename]

            if blocked.lower() == 'false': # item isn't blocked so it is saved to identified items
                identified_items.append(item_to_add)
                log_message = f'  - saving item {item_to_add}\n'
                logger.info(log_message)
                continue_loop = False

            else:
                blocked_items.append(item_to_add)
                continue_loop = False
            

        except:
            break


        # break






# for scanned_item in data_no_headers:
#     scanned_item_number = fn_lowercase_strip(scanned_item[0])
#     print(scanned_item_number, scanned_item)

#     try:
#         items_dict[scanned_item_number]
#         item_number = scanned_item_number
#         title = items_dict[scanned_item_number]['title']
#         location = fn_lowercase_strip(scanned_item[1])
#         quantity = fn_lowercase_strip(scanned_item[2])
#         blocked = items_dict[scanned_item_number]['blocked']
#         unit_cost = items_dict[scanned_item_number]['unit_cost']
#         filename = fn_lowercase_strip(scanned_item[3])

#         item_to_add = [scanned_item_number, item_number, title, location, quantity, blocked, unit_cost, filename]

#         if blocked.lower() == 'false':
#             identified_items.append(item_to_add)
#         else:
#             blocked_items.append(item_to_add)

#         print(item_to_add)

#     except:
#         unidentified_items.append(scanned_item)

# # -- STEP 2: IF SCANNED NO WASN'T FOUND IN ITEMS WE CHECK IF IT CAN BE FOUND IN NAV BARCODES
# unidentified_items_2 = unidentified_items[:]
# unidentified_items = []

# for item in unidentified_items_2:
#     print(item)

#     try:
#         scanned_item_number = item[0]
#         new_item_number = barcodes_dict[scanned_item_number]

#         try:
#             items_dict[new_item_number]
#             item_number = new_item_number
#             title = items_dict[new_item_number]['title']
#             location = fn_lowercase_strip(item[1])
#             quantity = fn_lowercase_strip(item[2])
#             blocked = items_dict[new_item_number]['blocked']
#             unit_cost = items_dict[new_item_number]['unit_cost']
#             filename = fn_lowercase_strip(item[3])

#             item_to_add = [scanned_item_number, new_item_number, title, location, quantity, blocked, unit_cost, filename]

#             if blocked.lower() == 'false':
#                 identified_items.append(item_to_add)
#             else:
#                 blocked_items.append(item_to_add)

#             print(item_to_add)  

#         except:
#             unknowns.append(item)

#     except:
#         unknowns.append(item)

    


print('original data:', len(data_no_headers))
print('identified_items:', len(identified_items))
print('unknown_items:', len(unknowns))
print('blocked_items:', len(blocked_items))
check = len(identified_items) + len(unknowns) + len(blocked_items)
print('check:', check, check == len(data_no_headers))

fn_save_csv(unknowns, 'test_unknowns.csv')
fn_save_csv(blocked_items, 'test_blocked_items.csv')
fn_save_csv(identified_items, 'test_identified_items.csv')
# # # ------------------    open stocktake file with items to match to NAV

# # stocktake_file = 'item_by_total_qty_by_location_merged.csv'
# # # stocktake_file = 'item_by_total_qty_by_location_test.csv'
# # scanned_items_data1 = fn_open_csv(stocktake_file)



# # scanned_items = [line for line in scanned_items_data1 if len(line) == 4] # removing empty lines -> []
# # scanned_items_without_headers = scanned_items[1:] # removing first line (headers)
# # # ['9781929198832', '32073', '2', 'scan13.csv']

# # # output file headers
# # headers = ['Scanned Number', 'NAV Number', 'Title', 'Location', 'Quantity', 'Blocked', 'Unit Cost', 'File']
# # final_item_list = [headers] # list of items that will be saved to csv file
# # unknown_items = [headers] # list of unknown items that will be saved to csv file

# # blocked_count = 0 # blocked items count

# # print('\n')

# # for item in scanned_items_without_headers: 
# #     # scanned item -> [Item Number,	Location, Total QTY in Location, File Name]
# #     # NAV item -> {item_number: {'title': title, 'blocked': blocked, 'unit_cost': unit cost}}
# #     # headers -> ['Scanned Number', 'NAV Number', 'Title', 'Location', 'Quantity', 'Blocked', 'Unit Cost', 'File']

# #     pal('\n --------------------------------------------------------------------------\n') # pal -> print and log

# #     item_found = False
# #     scanned_item_number = item[0].upper() # [Item Number, Location, Total QTY in Location, File Name]
# #     nav_item_number = None
# #     title = None
# #     location = item[1] # [Item Number, Location, Total QTY in Location, File Name]
# #     quantity = item[2] # [Item Number, Location, Total QTY in Location, File Name]
# #     blocked = None
# #     unit_cost = None
# #     file_name = item[3] # [Item Number, Location, Total QTY in Location, File Name]

# #     line_to_write = [scanned_item_number, nav_item_number, title, location, quantity, blocked, unit_cost, file_name]

# #     # for z in zip(headers, line_to_write):
# #     #     print(z)

# #     # break

# #     # -- STEP 1: CHECK IF SCANNED ITEM NUMBER CAN BE FOUND IN NAV ITEMS

# #     if scanned_item_number not in items_dict_keys and fn_remove_zeros(scanned_item_number) in items_dict_keys:
# #         scanned_item_number = fn_remove_zeros(scanned_item_number)

# #     if scanned_item_number in items_dict_keys:

# #         item_found = True
# #         nav_item_number = scanned_item_number

# #         pal(f' Scanned number {scanned_item_number} found in NAV items')
# #         pal(f' Scanned item number: {scanned_item_number}')
# #         pal(f'     NAV_item_number: {nav_item_number}')


# #     elif scanned_item_number not in items_dict_keys:
# #         pal(f' >>> Scanned number {scanned_item_number} NOT FOUND in NAV items')

# #     # -- STEP 2: IF ITEM WASN'T FOUND IN THE 'ITEMS' FILE WE CHECK 'BARCODES' FILE
# #     if item_found == False:
# #         if scanned_item_number not in barcodes_dictionary.keys() and fn_remove_zeros(scanned_item_number) in barcodes_dictionary.keys():
# #             scanned_item_number = fn_remove_zeros(scanned_item_number)

# #     if item_found == False: # item not found yet

# #         if scanned_item_number in barcodes_dictionary.keys(): # number found in barcodes

# #             # we access barcodes dictionary to get item No. assigned to this barcode
# #             item_number_assigned_to_the_barcode = barcodes_dictionary[scanned_item_number].upper()

# #             pal(f' Scanned number {scanned_item_number} FOUND in NAV barcodes')
# #             pal(f' NEW ITEM NUMBER: {item_number_assigned_to_the_barcode}')

# #             # we have item No. assigned to the barcode so now we check if this number
# #             # exists in the items file

# #             if item_number_assigned_to_the_barcode in items_dictionary.keys(): # new number found in items

# #                 item_found = True
# #                 nav_item_number = item_number_assigned_to_the_barcode

# #                 pal(f' NEW ITEM NUMBER {item_number_assigned_to_the_barcode} found in NAV items')
# #                 pal(f' Scanned item number: {scanned_item_number}')
# #                 pal(f'     NAV_item_number: {item_number_assigned_to_the_barcode}')

# #             elif item_number_assigned_to_the_barcode in items_dictionary.keys(): # new number not found in items
# #                 pal(f' >>> NEW ITEM NUMBER {item_number_assigned_to_the_barcode} NOT FOUND in NAV items')
# #                 # this item is going to unknown items


# #         elif scanned_item_number not in barcodes_dictionary.keys(): # number not found in barcodes
# #             pal(f' >>> Scanned number {scanned_item_number} NOT FOUND in NAV barcodes')

# #     # -- STEP 3: SCANNED NUMBER DOESN'T EXIST IN ITEMS OR BARCODES SO IT'S GOING TO UNKNOWN ITEMS

# #     if item_found == False:
# #         pal(f' >>> UNKNOWN ITEM: {scanned_item_number}')
# #         # headers -> ['Scanned Number', 'NAV Number', 'Title', 'Location', 'Quantity', 'Blocked', 'Unit Cost', 'File']
# #         unknown_item_to_append = [scanned_item_number, 'UNKNOWN', 'UNKNOWN ITEM', location,
# #                                   quantity, 'FALSE', 'UNKNOWN', file_name]
# #         final_item_list.append(unknown_item_to_append)
# #         unknown_items.append(unknown_item_to_append)
# #         continue

# #     # -- STEP 4: WE'VE FOUND NAV ITEM NO. FOR THIS SCANNED NO., WE HAVE TO CHECK IF ITEM IS BLOCKED

# #     blocked = items_dictionary[nav_item_number]['blocked']

# #     if 'false' in blocked.lower():
# #         blocked = False
        
# #         # headers
# #         # ['Scanned Number', 'NAV Number', 'Title', 'Location', 'Quantity', 'Blocked', 'Unit Cost', 'File']
# #         # {item_number: {'title': title, 'blocked': blocked, 'unit_cost': unit_cost}}  -> items dict

# #         title = items_dictionary[nav_item_number]['title']
# #         pal(f'  ITEM BLOCKED -> FALSE')
# #         pal(f'  TITLE: {title}')
# #         unit_cost = items_dictionary[nav_item_number]['unit_cost']
# #         entry_to_append = [scanned_item_number, nav_item_number, title, location, quantity,
# #                            'FALSE', unit_cost, file_name]
# #         final_item_list.append(entry_to_append)

# #     elif 'true' in blocked.lower():
# #         blocked = True
# #         title = items_dictionary[nav_item_number]['title']
# #         pal(f' ITEM BLOCKED: TRUE -> TITLE: {title}')

# #         # if item is blocked we check if we can extract new item No. from the description/title
# #         # description -> BLOCKED ITEM USE 0232519307
# #         new_isbn = [item for item in title.split()][-1] # split on whitespace and extract last item from the list
# #         new_isbn = new_isbn.upper()
        
# #         # we check if new item No. can be found in NAV items
# #         if new_isbn in items_dict_keys:
# #             title = items_dictionary[new_isbn]['title']
# #             pal(f' NEW ITEM NO. EXTRACTED: {new_isbn}')
# #             pal(f' ITEM {new_isbn} FOUND IN NAV ITEMS: {title}')

# #             # headers
# #             # ['Scanned Number', 'NAV Number', 'Title', 'Location', 'Quantity', 'Blocked', 'Unit Cost', 'File']
# #             # {item_number: {'title': title, 'blocked': blocked, 'unit_cost': unit_cost}}  -> items dict

# #             unit_cost = items_dictionary[new_isbn]['unit_cost']
# #             blocked = items_dictionary[new_isbn]['blocked']

# #             if 'true' in blocked.lower():
# #                 blocked = 'TRUE'
# #             elif 'false' in blocked.lower():
# #                 blocked = 'FALSE'

# #             entry_to_append = [scanned_item_number, new_isbn, title, location, quantity,
# #                            blocked, unit_cost, file_name]
# #             final_item_list.append(entry_to_append)

# #         elif new_isbn not in items_dict_keys:

# #             pal(f' ITEM {new_isbn} NOT FOUND IN NAV ITEMS')

# #             # headers
# #             # ['Scanned Number', 'NAV Number', 'Title', 'Location', 'Quantity', 'Blocked', 'Unit Cost', 'File']
# #             # {item_number: {'title': title, 'blocked': blocked, 'unit_cost': unit_cost}}  -> items dict

# #             title = items_dictionary[nav_item_number]['title']
# #             unit_cost = items_dictionary[nav_item_number]['unit_cost']
# #             entry_to_append = [scanned_item_number, nav_item_number, title, location, quantity,
# #                                'TRUE', unit_cost, file_name]
# #             final_item_list.append(entry_to_append)

# # pal('\n --------------------------------------------------------------------------\n')


# # pal(f'\n initial list lines: {len(scanned_items)} \n final list lines: {len(final_item_list)}')
# # pal(f'\n unknowns: {len(unknown_items)}')


# # fn_save_csv(final_item_list, 'output_list_items_with_titles.csv')
# # fn_save_csv(unknown_items, 'output_list_unknown_items.csv')

# # with open(log_file_name, 'w') as file:
# #     for line in log_data:
# #         file.write(line)

# # # print(barcodes_dictionary.keys())
# # # print(type(barcodes_dictionary.keys()))

# # input('\n')







