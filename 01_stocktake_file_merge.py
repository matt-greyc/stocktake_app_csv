#!/usr/bin/env python3

import os, csv, logging


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


#------------------------------------- BLOCK1 - logger setup -----------------------------------
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
#------------------------------------- END OF BLOCK 1 -------------------------------------------


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


files = fn_list_of_files(path='.\\scans\\')
csv_files = [file for file in files if os.path.splitext(file)[1].lower() == '.csv']  # os.path.splitext() is used to split the path name into a pair root and extension
csv_files.sort()
# rejected_files = [file for file in files if os.path.splitext(file)[1].lower() != '.csv']


#-------------------- get headers from one of the files ------------------------------------------------
csv_data = fn_open_csv(csv_files[0]) # opens first file from csv files list

for line in csv_data: # grabs headers (first line) for the 1st part of the file
    # -> ['Item Number', 'Total QTY']
    if len(line) == 2:
        headers1 = line[:]
        headers1.append('File Name')
        break

for line in csv_data: # grabs headers (first line) for the 2nd part of the file
    # -> ['Item Number', 'Location', 'Total QTY in Location']
    if len(line) == 3:
        headers2 = line[:]
        headers2.append('File Name')
        break

for line in csv_data: # grabs headers (first line) for the 3rd part of the file
    # -> ['Item Number', 'Location', 'QTY Added', 'Date', 'Time']
    if len(line) == 5:
        headers3 = line[:]
        headers3.append('File Name')
        break

data1 = [headers1] # data for the first part of the file -> ['Item Number', 'Total QTY']
data2 = [headers2] # data for the second part of the file -> ['Item Number', 'Location', 'Total QTY in Location']
data3 = [headers3] # data for the thirs part of the file -> ['Item Number', 'Location', 'QTY Added', 'Date', 'Time']
#-------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------
for file in csv_files:
    message = f'\n\n -> MERGING FILE \'{os.path.basename(file)}\'. DATA FORMAT:\n' # the message is printed and saved to a file
    logger.info(message)
    csv_data = fn_open_csv(file)
    current_file = os.path.basename(file)
    print(current_file)

    #-------------------------------------------------------------------------------------------------------
    content1 = [(line + [current_file]) for line in csv_data if len(line) == 2]

    for i in range(2):
        message = '    ' + str(content1[i][:-1])
        logger.info(message)
    #-------------------------------------------------------------------------------------------------------
    content2 = [(line + [current_file]) for line in csv_data if len(line) == 3]

    logger.info('')
    for i in range(2):
        message = '    ' + str(content2[i][:-1])
        logger.info(message)
    #-------------------------------------------------------------------------------------------------------
    content3 = [(line + [current_file]) for line in csv_data if len(line) == 5]

    logger.info('')
    for i in range(2):
        message = '    ' + str(content3[i][:-1])
        logger.info(message)
    #-------------------------------------------------------------------------------------------------------

    data1.extend(content1[1:])
    data2.extend(content2[1:])
    data3.extend(content3[1:])
#-------------------------------------------------------------------------------------------------------


# fn_save_csv(data, file)
fn_save_csv(data=data1, file='item_by_total_qty_merged.csv')
fn_save_csv(data=data2, file='item_by_total_qty_by_location_merged.csv')
fn_save_csv(data=data3, file='item_by_stocktake_count_by_date_and_time_merged.csv')

logger.info(f'\n\n\n   scan files: {len(files)}, merged files: {len(csv_files)}')
logger.info('\n\n\n >>> END OF PROGRAM')

input('\n\n Press ENTER to exit.')



