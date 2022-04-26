from flask import Flask
import daten


app = Flask("Daten")


@app.route("/speichern/<aktivitaet>")
def speichern(aktivitaet):
    zeitpunkt, aktivitaet = daten.aktivitaet_speichern(aktivitaet)

    return "Gespeichert: " + aktivitaet + " um " + str(zeitpunkt)


@app.route("/noten/<eingabe>")
def noten_eingabe(eingabe):
    teile = eingabe.split("WWW")
    student = teile[0]
    note = teile[1]
    daten.speichern("noten.json", student, note)
    return f"Die Note {note} für {student} wurde gespeichert."


@app.route("/liste")
def auflisten():
    aktivitaeten = daten.aktivitaeten_laden()

    aktivitaeten_liste = ""
    for key, value in aktivitaeten.items():
        zeile = str(key) + ": " + value + "<br>"
        aktivitaeten_liste += zeile

    return aktivitaeten_liste


if __name__ == '__main__':
    app.run(debug=True, port=5000)