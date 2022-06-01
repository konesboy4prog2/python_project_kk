#Quelle: Fabian Odoni (Demo)

import json

def opendata():
    try:
        with open("data.json") as open_file:
            data_content = json.load(open_file)
    except FileNotFoundError:
        data_content = []

    return data_content


def storedata(data_content):
    with open("data.json", "w") as open_file:
        json.dump(data_content, open_file, indent=2)