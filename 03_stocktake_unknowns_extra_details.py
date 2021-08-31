
#!/usr/bin/env python3

import csv, os, logging


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



unknowns_file = 'output_unknown_items.csv'
scan_data_file = 'item_by_stocktake_count_by_date_and_time_merged.csv'
identified_items_file = 'output_matched_items.csv'

identified_items_data = fn_open_csv(identified_items_file)[1:]
identified_items_dict = {item[0]: item[2] for item in identified_items_data}

scan_data = fn_open_csv(scan_data_file)[1:]
# logger.info('\n\n')
# for i in range(2):
#     logger.info(scan_data[i])

unknowns_data = fn_open_csv(unknowns_file)[1:]
unknowns_data = sorted(unknowns_data, key=lambda item: item[3]) # sorts data using location as the key

item_count = 1
for row in unknowns_data:

    item_number = row[0]
    location = row[3]
    quantity = row[4]
    scan_file = row[7]
    
    # location_content = []
    # num_in_location = 1
    # logger.info(f'\n location: {location} - scanned No: {item_number} - QTY: {quantity} - file: {scan_file}')

    # for line in scan_data:
    #     line_item_no = line[0]
    #     # line_quantity = line[2]
    #     line_scan_time = line[4]
    #     scan_data_location = line[1]
    #     scan_data_file = line[5]

    #     if location == scan_data_location and scan_file == scan_data_file:
    #         # location_content.append([num_in_location] + line)
    #         # location_content.append([num_in_location, line_item_no, line_quantity, line_scan_time])
    #         location_content.append([num_in_location, line_item_no, line_scan_time])
    #         # location_content.append(f'{num_in_location}. Item: {line_item_no}. QTY: {line_quantity}. Scan time: {line_scan_time}')

    #         num_in_location += 1
    
    # logger.info(f' location length: {len(location_content)}')

    # for line in location_content:
    #     logger.info(f'{line[0]}. Item: {line[1]}. Scanned: {line[2]}')

    

    # merged location
    location_content = []
    num_in_location = 1
    # logger.info('\n\nmerged location')
    # logger.info(f'\n\nlocation: {location} -> scanned No: {item_number} -> QTY: {quantity} -> file: {scan_file}')
    logger.info(f'\n\n{item_count}. location: {location}, unknown item: {item_number}, scan file: {scan_file}')

    previous_item = None
    next_item = None

    for line in scan_data:
        line_item_no = line[0]
        # line_quantity = line[2]
        line_scan_time = line[4]
        item_no = line[0]
        scan_data_location = line[1]
        scan_data_file = line[5]

        if item_no == previous_item:
            previous_item = item_no
            continue

        if location == scan_data_location and scan_file == scan_data_file:
            # location_content.append([num_in_location] + line)
            # location_content.append([num_in_location, line_item_no, line_quantity, line_scan_time])
            location_content.append([num_in_location, line_item_no, line_scan_time])

            num_in_location += 1

        previous_item = item_no
    
    # previous_item = None
    # logger.info(f'location length: {len(location_content)}')

    data = []

    for i in range(len(location_content)):

        line = location_content[i]
        
        if line[1] == item_number:
            unknown_item = line
            
            # previous item
            try:
                previous_item = location_content[i-1]

                if i == 0:
                    previous_item = []
            except:
                previous_item = ['?????', '?????', '?????']
            # next item
            try:
                next_item = location_content[i+1]

            except:
                next_item = ['?????', '?????', '?????']

                if i == len(location_content) - 1:
                    next_item = [] 

            data = [previous_item, unknown_item, next_item]

            for item in data:

                try:
                    title = identified_items_dict[item[1]][0:30]
                    if title == 'UNKNOWN' and item[1] != item_number:
                        title = '???????????????'
                    elif title == 'UNKNOWN' and item[1] == item_number:
                        title = '-----  UNKNOWN  -----'
                except:
                    title = '???????????????'

                if item:
                    # logger.info(f'  {item[0]}. Item: {item[1]}. Title: {title}. Scanned: {item[2]}')
                    logger.info(f'  {item[0]}. Item: {item[1]}. Title: {title}')

            logger.info(f' Item {unknown_item[0]} ({len(location_content) - unknown_item[0] + 1} from the end). Location length: {len(location_content)}')

            break

    item_count += 1


with open(log_file_path) as file:
    content = file.read()

with open(log_file_name.replace('log', 'txt'), 'w') as file:
    file.write(content)