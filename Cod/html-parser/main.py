pathToProjects = '../../Projects/' 

import os
# import html_to_json
import json

def extract_html(main_folder, folder, lst = []):
    for file in os.listdir(pathToProjects + main_folder + '/' + folder):

        if file.endswith('.html'):
            with open(f'{pathToProjects + main_folder}/{folder}/{file}', 'r', encoding='utf-8') as f:
                try:
                    # print(f'{pathToProjects + main_folder}/{folder}/{file}')
                    va = f.read()
                    lst.append(va)
                except:
                    print(f)

        elif os.path.isdir(f'{pathToProjects + main_folder}/{folder}/{file}'):
            extract_html(main_folder, f'{folder}/{file}', lst)

def count_html(main_folder, folder, count = 0):
    for file in os.listdir(pathToProjects + main_folder + '/' + folder):

        if file.endswith('.html'):
            count += 1

        elif os.path.isdir(f'{pathToProjects + main_folder}/{folder}/{file}'):
            count = count_html(main_folder, f'{folder}/{file}', count)
    
    return count

def read_folder(main_folder):

    dc = {}

    for folder in os.listdir(pathToProjects + main_folder):
        print(main_folder, folder)

        lst = []
        # extract_html(main_folder, folder, lst)

        oustputLst = []
        for i in range(len(lst)):
            # output_json = html_to_json.convert(lst[i])
            oustputLst.append(output_json)
        
        dc[folder] = oustputLst
    
    with open(f'parsed/{main_folder}.json', 'w') as file:
        json.dump(dc, file)

if __name__ == '__main__':
    folders = ['bootstrap', 'materialize', 'tailwind']

    # for folder in folders:
    #     read_folder(folder)

    dc = {}

    for folder in folders:
        with open(f'parsed/{folder}.json', 'r') as file:
            data = json.load(file)
            count = 0
            for v in data.values():
                count += len(v)

            count_proj = 0

            for folder2 in os.listdir(pathToProjects + folder):
                # for file3 in os.listdir(pathToProjects + folder + '/' + folder2):
                count_proj += 1

            dc[folder] = {}
            dc[folder]['total_projects'] = count_proj
            dc[folder]['total_pages'] = count

        with open(f'../statistics/average_scope/data/average_scope.json', 'r') as file:
            data = json.load(file)
            dc[folder]['used_projects'] = len(data[folder])
            # get the key of every object in list data[folder]
            key_list = []
            count = 0
            for i in data[folder]:
                key_list.append(list(i.keys())[0])
            for folder2 in os.listdir(pathToProjects + folder):
                if folder2 in key_list:
                    count += count_html(folder, folder2)
            dc[folder]['used_pages'] = count


    with open(f'parsed/stats.json', 'w') as file:
        json.dump(dc, file)
