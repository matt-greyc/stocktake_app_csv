
#!/usr/bin/env python3

# import os
import csv


#-------------------------------------------------------------------------
def fn_open_csv(data_file): 
    '''opens a csv file and returns the content as a list'''
    try:
        with open(data_file, 'r') as file:
            csv_object = csv.reader(file)
            csv_data = list(csv_object)
        return csv_data
    except IOError:
        input(f'\n FILE NOT FOUND: {data_file} ')
        exit()
    except UnicodeDecodeError:
        input(f'\n WRONG FILE FORMAT (NOT CSV). FILE CAN\'T BE DECODED: {data_file} ')
        exit()
#-------------------------------------------------------------------------


# ------------------   create items dictionary {item_number: {'title': title, 'blocked': blocked}}

# ----- open unknows file and get the data
unknown_items_data = fn_open_csv('output_unknown_items.csv')
unknown_items_headers = unknown_items_data[0]
unknown_items = unknown_items_data[1:]

# print('\n')
# for num in range(3):
#     print(unknown_items_data[num])

# ----- open scanned data file and get the data with extra details like the time of scan
scanned_items_data = fn_open_csv('item_by_stocktake_count_by_date_and_time_merged.csv')
scanned_items_headers = scanned_items_data[0] # headers only
scanned_items = scanned_items_data[1:] # data without headers - items only

# print('\n')
# for num in range(3):
#     print(scanned_items_data[num])

count = 0

data_by_location = []
processed_locations = []

item_count = 0

for item in unknown_items:
    item_count += 1
    location_content = []
    scanned_number = item[0]
    print(f'\n PROCESSING ITEM {item_count}: {scanned_number}')
    location = item[3]

    # there could be more than 1 unknown in one location so this condition skips the location if it was already processed
    if location in processed_locations:
        continue
    else:
        processed_locations.append(location)
    # print(f' unknown item -> scanned number: {scanned_number}, location: {location}')

    # get all the items in the current location
    for item in scanned_items:
        if location in item:
            processed_locations.append(location)
            location_content.append(item)

    # print('  -> location content:')
    # for item in location_content:
    #     print(' ', item)

    # print('')

    data_by_location.append([int(location), location_content])
    # break

# print(data_by_location_dictionary)

with open('unknowns_extra_details_full.txt', 'w') as file:
    file.write('')

with open('unknowns_extra_details_for_printing.txt', 'w') as file:
    file.write('')

data_to_write = ''
data_to_print = ''

# -- create a dictionary of identified item from matched titles file
matched_items_dict = {x[0]: x[2] for x in fn_open_csv('output_matched_items.csv')}


for item in sorted(data_by_location):
    location1 = item[0]
    data1 = item[1]
    # print(location1)
    # print(data1)

    line_number = 0
    
    
    # data_to_write += f'location {location1}\n'
    # data_to_write += f'Time       Item No.        Title\n'

    new_data = [data1[0]]

    for line in data1[1:]:
    # line -> ['9781570758706', '33039', '1', '2020-02-27', '09:56:49']
        if line[0] == new_data[-1][0]:  # if previous line has the same item number it is overriten
            new_data[-1] = line
        elif line[0] != new_data[-1][0]:
            new_data.append(line)
            
    for line in new_data:
        # line -> ['9780745962719', '330899', '7', '2020-02-27', '14:48:58']
        time_of_scan1 = line[4]
        scanned_item_number1 = line[0]
        quantity1 = line[2]
        line_number += 1

        title1 = matched_items_dict[scanned_item_number1.lower()]
        if title1 == 'UNKNOWN':
            title1 = '----------  UNKNOWN  ----------'

            # ----------------- short version for printing
            line_index = line_number - 1

            try:
                if line_index == 0: 
                    line_before = None
                else:
                    line_before = new_data[line_index - 1]
            except:
                line_before = None

            try:
                line_after = new_data[line_index + 1]
            except:
                line_after = None

            data_for_printing = [line_before, new_data[line_index], line_after]

            for line2 in data_for_printing:
                 # line -> ['9780745962719', '330899', '7', '2020-02-27', '14:48:58']
                
                if line2 == None:
                    continue
                else:
                    time_of_scan2 = line2[4]
                    scanned_item_number2 = line2[0]
                    quantity2 = line2[2]

                    title2 = matched_items_dict[scanned_item_number2.lower()]

                    if len(title2) > 45:
                        title2 = title2[:45]
                    if title2 == 'UNKNOWN':
                        title2 = '----------  UNKNOWN  ----------'

                    message2 = f'loc. {location1} - item {scanned_item_number2} - {title2}'
                    data_to_print += message2 + '\n'

            data_to_print += '\n\n'


        message = f'location {location1} - time {time_of_scan1} - item {scanned_item_number1} - {title1}'
        data_to_write += message + '\n'

    data_to_write += '\n\n'


with open('unknowns_extra_details_full.txt', 'a') as file:
        file.write(data_to_write)

with open('unknowns_extra_details_for_printing.txt', 'a') as file:
        file.write(data_to_print)

# for line in data_to_print:
#     print(line)

input('\n PRESS ENTER TO EXIT... ')
