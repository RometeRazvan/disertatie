
def parse(file_name):
    import cssutils

    with open('./css/' + file_name, 'r') as f:
        css = f.read()

    dct = {}
    sheet = cssutils.parseString(css)

    for rule in sheet:
        if rule.type == rule.STYLE_RULE:
            selector = rule.selectorText
            styles = rule.style.cssText
            dct[selector] = styles
        if rule.type == rule.MEDIA_RULE:
            for r in rule:
                if r.type == r.STYLE_RULE:
                    selector = r.selectorText
                    styles = r.style.cssText
                    dct[selector] = styles

    output_file = file_name.split('.')[0] + '.json'

    print("\nParsing started for " + file_name + "!\n")

    import json
    with open('./parsed/' + output_file, "w") as file:
        json.dump(dct, file)
    
    print("Parsing completed for " + file_name + "!\n")

if __name__ == "__main__":
    menu = """
    -=-=-=-=- CSS Parser -=-=-=-=-
    0. Parse Bootstrap CSS to JSON
    1. Parse Materialize CSS to JSON
    2. Parse Tailwind CSS to JSON
    3. Parse Tailwind All CSS to JSON
    4. Parse All CSS to JSON
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    """
    print(menu)
    choice = int(input("Enter your choice: "))

    files = ['bootstrap.css', 'materialize.css', 'tailwind.css', 'tailwind-all.css']

    print("Parsing CSS to JSON...\n")

    if choice == 4:
        for file in files:
            parse(file)
    else:
        parse(files[choice])

    print("\nParsing completed!\nCheck the JSON files in the same directory.\nThank you!\n")