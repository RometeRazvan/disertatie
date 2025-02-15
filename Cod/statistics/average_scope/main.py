import json
import uuid
from datetime import datetime, timedelta

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
                if item in html_tags and len(key) == 1:
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
                item = item.replace('.', ' .')
                item = item.split(' ')
                item = [i for i in item if i]
                item = ' '.join(item)
                dct2[item] = len(value)
        
        with open('data/css_presentation_properties/short/' + file_name + '.json', 'w') as file:
            json.dump(dct2, file)

        data[file_name] = count
        
    with open('data/simple_selectors_count.json', 'w') as file:
        json.dump(data, file)


def calc_local_scope(data):
    _sum = 0
    for key, value in data.items():
        if key[0] != '_':
            _sum += 1
            if isinstance(value, list):
                for item in value:
                    _sum += calc_local_scope(item)
            elif isinstance(value, dict):
                _sum += calc_local_scope(value)
    return _sum

def calc_class_scopes(data, css, lst, final_lst = []):
    for key, value in data.items():
        key_id = str(uuid.uuid4())[:8]
        if key[0] != '_' and isinstance(value, list):
            for item in value:
                if '_attributes' in item and 'class' in item['_attributes']:
                    for class_name in item['_attributes']['class']:
                        final_lst.append({key_id: [lst + [class_name], 1 + calc_local_scope(item)]})
                        calc_class_scopes(item, css, lst + [class_name], final_lst)
                else:
                    final_lst.append({key_id: []})
                    calc_class_scopes(item, css, lst, final_lst)

def calc_tag_scopes(data, css, lst, final_lst = []):
    for key, value in data.items():
        key_id = str(uuid.uuid4())[:8]
        if key[0] != '_' and isinstance(value, list):
            for item in value:
                final_lst.append({key_id: [lst + [key], 1 + calc_local_scope(item)]})
                calc_tag_scopes(item, css, lst + [key], final_lst)

def calc_average_scope():
    files = ['bootstrap', 'materialize', 'tailwind']
    results = {
        'bootstrap': [],
        'materialize': [],
        'tailwind': []
    }
    for file_name in files:
        with open('../../html-parser/parsed/' + file_name + '.json', 'r') as file:
            projects = json.load(file)
        
        with open('../../css-parser/parsed/scope/' + file_name + '.json', 'r') as file:
            css = json.load(file)
        
        for project in projects.items():
            project_name = project[0]
            project_data = project[1][0]

            start_time = datetime.now()
            print(project_name, start_time)
            try:
                if (file_name == 'bootstrap' and project_name != 'honda-cbr-bootstrap-assignment-Khansojib51222') or (file_name == 'materialize' and project_name != 'HTML5-CSS3-Materialize22') or (file_name == 'tailwind' and project_name != 'tailwind-ui-component'):
                    continue

                broken = False
                
                n = calc_local_scope(project_data)

                final_lst_tag = []
                final_lst_class = []
                calc_tag_scopes(project_data, css, [], final_lst_tag)
                calc_class_scopes(project_data, css, [], final_lst_class)

                class_list = css.keys()

                for item in final_lst_class:
                    for key, v in item.items():
                        if len(v) == 0:
                            continue
                        for i in range(len(v[0])):
                            v[0][i] = '.' + v[0][i]

                project_class_set = []
                final_lst = final_lst_tag + final_lst_class
                print(final_lst_tag)

                scope = 0

                past = []
                past_value = []

                pc = {}

                cycled = {}

                for item in final_lst:
                    for key, v in item.items():
                        if not v:
                            continue
                        value = v[0]
                        value = ' '.join(value)
                        value = value.split(' ')
                        value = [i for i in value if i]

                        diff = datetime.now() - start_time

                        if diff > timedelta(hours=1):
                            broken = True
                            break

                        
                        
                        for class_name in class_list:
                            class_name = class_name.split(' ')
                            class_name = [i for i in class_name if i]

                            if value and (
                                (len(value) > len(class_name) and value[:len(class_name)] == class_name and ' '.join(class_name) not in cycled) or
                                (len(value) == len(class_name) and all(i in class_name for i in value) and ' '.join(class_name) not in cycled)or
                                (len(value) >= len(class_name) and all(i in value for i in class_name) and ' '.join(class_name) not in cycled)
                            ) and class_name != past:
                            # if value and all(i in class_name for i in value):
                                # print(value, '|', class_name, v[1], class_name, past)
                                # print(value, class_name, v[1])
                                # if class_name == ['.container'] and '.container' in cycled:
                                #     print(cycled, class_name, ' '.join(class_name))
                                # remoev all keys in cycled that have a value less of len(value)
                                to_remove = []
                                for k, v2 in cycled.items():
                                    if v2 > len(value):
                                        to_remove.append(k)
                                for k in to_remove:
                                    del cycled[k]
                                cycled[' '.join(class_name)] = len(value)
                                if key not in pc:
                                    pc[key] = {
                                        'p': 1,
                                        'vp': css[' '.join(class_name)]
                                    }
                                else:
                                    pc[key]['p'] += 1
                                    pc[key]['vp'] += css[' '.join(class_name)]
                                if len(value) == 1 and '.' not in value[0]:
                                    scope += n
                                else:
                                    scope += v[1]
                                past = class_name
                                past_value = value
                                if class_name not in project_class_set:
                                    project_class_set.append(class_name)
                
                if broken:
                    print('Broken')
                    continue

                m = len(project_class_set)

                p = [i['p'] for i in pc.values()]
                vp = [i['vp'] for i in pc.values()]

                if n != 0 and m != 0:
                    p = sum(p) / len(p)
                    vp = sum(vp) / len(vp)

                    print(n, m, scope, scope / (n * m) * 100, project_name, p, vp, p * vp)

                    results[file_name].append(
                        {
                            project_name: {
                                'n': n,
                                'm': m,
                                'scope': scope,
                                'average_scope': scope / (n * m) * 100,
                                '#p': p,
                                '#vp': vp,
                                'pc': p * vp
                            }
                        }
                    )

                print(project_class_set)
                print('----------------------------------')                
                break
                    
                    # if file_name == 'tailwind':
                    #     break
            except Exception as e:
                print('Error for', project_name, e)
                pass
    
    # with open('data/average_scope.json', 'w') as file:
    #     json.dump(results, file)

def calc_average():

    with open('./data/average_scope.json', 'r') as file:
        data = json.load(file)

    files = ['bootstrap', 'materialize', 'tailwind']

    matrix = []

    boot = data['bootstrap']
    mat = data['materialize']
    tail = data['tailwind']

    # get max len of all projects by keys
    max_len = len(boot)
    if len(mat) > max_len:
        max_len = len(mat)
    if len(tail) > max_len:
        max_len = len(tail)
    
    for i in range(max_len):
        matrix.append([])
    
    for i in range(max_len):
        if i > len(boot):
            matrix[i].append('-')
            matrix[i].append('-')
            matrix[i].append('-')
            continue
        for j in boot[i].values():
            matrix[i].append(j['n'])
            matrix[i].append(j['m'])
            matrix[i].append(round(j['average_scope'], 2))
    for i in range(max_len):
        if i >= len(mat):
            matrix[i].append('-')
            matrix[i].append('-')
            matrix[i].append('-')
            continue
        for j in mat[i].values():
            matrix[i].append(j['n'])
            matrix[i].append(j['m'])
            matrix[i].append(round(j['average_scope'], 2))
    for i in range(max_len):
        if i >= len(tail):
            matrix[i].append('-')
            matrix[i].append('-')
            matrix[i].append('-')
            continue
        for j in tail[i].values():
            matrix[i].append(j['n'])
            matrix[i].append(j['m'])
            matrix[i].append(round(j['average_scope'], 2))
    i2 = 1
    a = ''
    for i in matrix:
        b = '\\textbf{' + str(i2) + '}'
        str1 = "{} & {} & {} & {} & {} & {} & {} & {} & {} & {} \\\ \n".format(b, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
        i2 += 1
        a += str1
    
    # write to file
    with open('data/average_scope_matrix.txt', 'w') as file:
        file.write(a)

    dct = {}

    for file_name in files:
        results = data[file_name]

        count = 0
        sum = 0
        sum_pc = 0
        sum_p = 0
        sum_vp = 0

        for item in results:
            for i in item.values():
                count += 1
                sum += i['average_scope']
                sum_pc += i['pc']
                sum_p += i['#p']
                sum_vp += i['#vp']
        
        print(file_name, sum / count, sum_pc / count)

        dct[file_name] = {
            'average_scope': sum / count,
            'p': sum_p / count,
            'vp': sum_vp / count,
            'pc': sum_pc / count
        }
    
    with open('data/average_scope222.json', 'w') as file:
        json.dump(dct, file)



if __name__ == '__main__':
    # calc_average_scope()
    # count_stand_alone_simple_selectors()
    calc_average()