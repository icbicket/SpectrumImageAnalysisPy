from __future__ import print_function
import os
import glob


def name_file(filepath):
    ''' If the filepath exists, find the last number associated with that
    filename and add one more to it. If it does not exist, save the file
    with the filename given'''
    if os.path.exists(filepath):
        new_name = find_latest_filename(filepath)
    else:
        new_name = filepath
    print('Saving file as...', new_name)
    return new_name


def find_latest_filename(filepath):
    if len(filepath.rsplit('/', 1)) == 2:
        folder_name = filepath.rsplit('/', 1)[0]  # Split out folder path
        filename = filepath.rsplit('/', 1)[-1]  # retrieve filename
        file_list = glob.glob('%s/%s*.%s' % (
            folder_name,
            filename.rsplit('.', 1)[0],
            filename.rsplit('.')[-1]))  # find list of files within folder
        nums = []
        last_file = None
        for file_num in file_list:
            # if the filename ends in -digit...
            if file_num.rsplit('.', 1)[-2].rsplit('-', 1)[-1].isdigit():
                # append the number to the list
                nums.append(int(
                    file_num.rsplit('.', 1)[-2].rsplit('-', 1)[-1]))
                last_num = max(nums)  # find maximum number
                last_file = '%s-%d.%s' % (
                    file_num.rsplit('.', 1)[-2].rsplit('-', 1)[-2],
                    last_num,
                    file_num.rsplit('.', 1)[-1])
            elif last_file is not None:
                last_file = last_file
            else:
                last_file = '%s.%s' % (
                    file_num.rsplit('.', 1)[-2],
                    file_num.rsplit('.', 1)[-1])
        new_filename = number_file_names(last_file)
    else:
        folder_name = ''
        filename = filepath
        new_filename = number_file_names(filename)
    return new_filename


def number_file_names(filepath):
    # If the input filepath has a folder path included
    if len(filepath.rsplit('/', 1)) == 2:
        folder_name = filepath.rsplit('/', 1)[0]
        filename = filepath.rsplit('/', 1)[-1]
    else:
        folder_name = ''
        filename = filepath

    if filename.rsplit('-', 1)[-1].rsplit('.', 1)[0].isdigit():
        filename = '%s-%d.%s' % (
            filename.rsplit('-', 1)[0],
            1+int(filename.rsplit('-', 1)[-1].rsplit('.', 1)[0]),
            filename.rsplit('.', 1)[-1])
    else:
        filename = '%s-1.%s' % (
            filename.rsplit('.', 1)[-2],
            filename.rsplit('.', 1)[-1])
    filepath = os.path.join(folder_name, filename)
    return filepath
