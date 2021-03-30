#!/usr/bin/env python3

import os, csv, logging


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
        mkdir(f_path+'\\'+folder)
#--------------------------------------------------------------------------------


fn_folder_exists_check('logs')  # 'logs' folder is created if it doesn't exist already
log_file_name = fn_create_log_file_name()
log_file_folder = '.\\logs\\'
log_file_path = log_file_folder + log_file_name

#------------------------------------- BLOCK1 -------------------------------------------
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

csv_files = fn_list_of_files('.\\scans')  # list of files in the 'scans' folder
csv_files.sort()

#------------------------------------------ BLOCK 2 --------------------------------------
# this block of code iterates over files in 'scans' folder and compares them to each other to check if
# the same location can be found in more than 1 file, this might indicate that location was scanned twice
# and file should be deleted

# DATA FORMAT:
# Item Number,Location,Total QTY in Location
# 0901810622,72003,330

for i in range(len(csv_files)): # iterates over csv files in the 'scans' folder
    file1 = csv_files[i]
    file1_no_path = os.path.basename(file1)
    message = f'\n -> checking {file1_no_path}'
    logger.info(message)

    try:
        with open(file1, 'r') as datafile:
            csv_object = csv.reader(datafile)
            data1 = set([line[1] for line in csv_object if len(line) == 3][1:])            
    except:
        logger.exception(f'\n\n !!!! ERROR: UNABLE TO PROCESS FILE \'{file1_no_path}\' !!!!\n\n\n')
        input('\n\n Press ENTER to exit. ')
        exit()       

    for item in csv_files[i + 1:]:
        file2 = item
        file2_no_path = os.path.basename(file2)

        try:
            with open(file2, 'r') as datafile:
                csv_object = csv.reader(datafile)
                data2 = set([line[1] for line in csv_object if len(line) == 3][1:])
                common_locations = data1.intersection(data2)
                
                if len(common_locations) > 0: # if the same location(s) is found in both files message is saved in log file
                    message = '\n\n ----------------------------------------------------------------------'
                    logger.info(message)
                    message = f'\n File \'{file1_no_path}\' and file \'{file2_no_path}\' have {len(common_locations)} common location(s):\n'
                    logger.info(message)
                    common_locations = [location for location in common_locations]
                    common_locations_string = ', '.join(common_locations)
                    message = ' ' + common_locations_string + '\n'
                    logger.info(message)
                    message = ' ----------------------------------------------------------------------\n'
                    logger.info(message)
        except:
            logger.exception(f'\n\n !!!! ERROR: UNABLE TO PROCESS FILE \'{file2_no_path}\' !!!!\n\n\n')
            input('\n\n Press ENTER to exit. ')
            exit()
#---------------------------------------- END OF BLOCK 2 ----------------------------------------

logger.info('\n\n >>> END OF PROGRAM')
input('\n\n Press ENTER to exit. ')



