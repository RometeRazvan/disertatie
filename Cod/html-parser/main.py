pathToProjects = '../../Projects/' 

import os
import html_to_json
import json

def extract_html(main_folder, folder, lst = []):
    for file in os.listdir(pathToProjects + main_folder + '/' + folder):

        if file.endswith('.html'):
            with open(f'{pathToProjects + main_folder}/{folder}/{file}', 'r') as f:
                va = f.read()
                lst.append(va)

        elif os.path.isdir(f'{pathToProjects + main_folder}/{folder}/{file}'):
            extract_html(main_folder, f'{folder}/{file}', lst)


def read_folder(main_folder):

    dc = {}

    for folder in os.listdir(pathToProjects + main_folder):
        print(main_folder, folder)

        lst = []
        extract_html(main_folder, folder, lst)

        oustputLst = []
        for i in range(len(lst)):
            output_json = html_to_json.convert(lst[i])
            oustputLst.append(output_json)
        
        dc[folder] = oustputLst
    
    with open(f'parsed/{main_folder}.json', 'w') as file:
        json.dump(dc, file)

if __name__ == '__main__':
    folders = ['bootstrap']#, 'materialize', 'tailwind']

    for folder in folders:
        read_folder(folder)