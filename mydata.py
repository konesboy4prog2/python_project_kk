#Quelle: Fabian Odoni (Demo)

import json

def opendata(): #json-File wird geöffnet
    try:
        with open("data.json") as open_file:
            data_content = json.load(open_file)
    except FileNotFoundError:
        data_content = []

    return data_content


def storedata(data_content): #Daten aus Formular werden gespeichert
    with open("data.json", "w") as open_file: #w steht für write
        json.dump(data_content, open_file, indent=2) #indent 2 steht für die Pakete, welche untereinander gelistet werden im json-File