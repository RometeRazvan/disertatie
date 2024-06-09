import json

def calc_universality():
        
    results = {}
    files = ['bootstrap', 'materialize', 'tailwind', 'tailwind-all']
    
    for file_name in files:

        with open('../../css-parser/parsed/' + file_name + '.json', 'r') as file:
            css = json.load(file)
        
        with open('../config/config.json', 'r') as file:
            config = json.load(file)

        combinators = config['combinators']    
        
        count_not_hidden = 0

        lst = []
        for key, value in css.items():

            for combinator in combinators:
                if combinator != ' ':
                    key = key.replace(combinator, '')

            key = key.strip()
            # add sapce after each . that is not first character
            key = key.replace('.', ' .')
            key = key.replace('( .', '(.')
            key = key.replace('\" \"', '\"^spc^\"')
            key = key.split(' ')
            # remnove empty strings
            key = list(filter(None, key))

            for i in range(len(key)):
                key[i] = key[i].strip()
                if '.' not in key[i] and key[i] == ':not([hidden])':
                    count_not_hidden += 1
                lst.append(key[i])
        
            # lst.append(key)
        with open('data/refined_css/' + file_name + '.json', 'w') as file:
            json.dump(lst, file)

        results[file_name] = calculate_universality(file_name)
        results[file_name]['NotHidden'] = count_not_hidden

    with open('data/universality_results.json', 'w') as file:
        json.dump(results, file)

def calculate_universality(file_name):
    with open('data/refined_css/' + file_name + '.json', 'r') as file:
        data = json.load(file)

    
    countHTML = 0
    countOther = 0

    for item in data:
        if '.' in item or '#' in item:
            countOther += 1
        else:
            countHTML += 1

    return {
        'HTML': countHTML,
        'Other': countOther,
        'Total': countHTML + countOther,
        'Percentage': countHTML/(countHTML + countOther) * 100
    }

if __name__ == '__main__':
    calc_universality()