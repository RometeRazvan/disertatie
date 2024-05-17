import json

if __name__ == "__main__":
    files = ['bootstrap', 'materialize', 'tailwind', 'tailwind-all']

    for file in files:
        print(f"File: {file}")

        with open(f"./parsed/{file}.json", 'r') as f:
            css = f.read()
        
        css = json.loads(css)

        dct = {}

        for key, value in css.items():

            key = key.replace('.',' .')
            key = key.split(', ')

            combinators = ['>', '+', '~', '<']

            count = len(value.split('\n'))

            for k in key:
                if any([combinator in k for combinator in combinators]):
                    continue

                else:
                    # it = k.split(' ')

                    # it = [i for i in it if i]

                    # k = ' '.join(it[1:])

                    # if it[0] not in dct:
                    #     if len(it) == 1:
                    #         dct[it[0]] = {
                    #             '': count,
                    #         }
                    #     else:
                    #         dct[it[0]] = {
                    #             k: count,
                    #         }
                    # elif len(it) == 1:
                    #     if '' not in dct[it[0]]:
                    #         dct[it[0]][''] = count
                    #     else:
                    #         dct[it[0]][''] += count
                    # else:
                    #     if k not in dct[it[0]]:
                    #         dct[it[0]][k] = count
                    #     else:
                    #         dct[it[0]][k] += count
                    k = k.replace('.', ' .')
                    k = k.split(' ')
                    k = [i for i in k if i]
                    k = ' '.join(k)

                    dct[k] = count
    
        with open(f"./parsed/scope/{file}.json", 'w') as f:
            f.write(json.dumps(dct, indent=4))
            print(f"File {file} written successfully")