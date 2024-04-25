import json

filePaths = ['bootstrap', 'materialize', 'tailwind-all']

def count_stand_alone_simple_selectors():
    files = ['bootstrap', 'materialize', 'tailwind', 'tailwind-all']
    data = {}

    with open('../config/config.json', 'r') as file:
        config = json.load(file)
        
    html_tags = config['html_tags']

    for file_name in files:
        with open('../../css-parser/parsed/' + file_name + '.json', 'r') as file:
            css = json.load(file)

        count = 0
        dct = {}
        
        for key, value in css.items():
            original_key = key

            key = key.strip()
            key = key.replace(' ', '')

            key = key.split(',')

            for item in key:
                if item in html_tags:
                    count += 1

            value = value.split('\n')
            for i in range(len(value)):
                value[i] = value[i].strip()
            
            dct[original_key] = value
        
        with open('data/css_presentation_properties/long/' + file_name + '.json', 'w') as file:
            json.dump(dct, file)
        
        dct2 = {}  
        for key, value in dct.items():
            key = key.split(', ')
            for item in key:
                dct2[item] = len(value)
        
        with open('data/css_presentation_properties/short/' + file_name + '.json', 'w') as file:
            json.dump(dct2, file)

        data[file_name] = count
        
    with open('data/simple_selectors_count.json', 'w') as file:
        json.dump(data, file)


def calc_local_scope(data):
    sum = 0
    for key, value in data.items():
        if key[0] != '_':
            sum += 1
            if isinstance(value, list):
                for item in value:
                    sum += calc_local_scope(item)
            elif isinstance(value, dict):
                sum += calc_local_scope(value)
    return sum

def calc_average_scope():
    files = ['bootstrap', 'materialize', 'tailwind']

    with open('../config/config.json', 'r') as file:
        config = json.load(file)
        
    html_tags = config['html_tags']

    for file_name in files:
        with open('../../html-parser/parsed/' + file_name + '.json', 'r') as file:
            projects = json.load(file)
        
        with open('data/css_presentation_properties/short/' + file_name + '.json', 'r') as file:
            css = json.load(file)
        
        for project in projects.items():
            project_name = project[0]
            project_data = project[1][0]

            n = calc_local_scope(project_data)

if __name__ == '__main__':
    calc_average_scope()