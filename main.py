from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from mydata import opendata, storedata
import random

app = Flask("__name__")


@app.route("/")
def hello():
    names = ["Gian-Luca", "Luca", "Kones", "Manu", "Marion"]
    name_choice = random.choice(names)
    about_link = url_for("about")
    return render_template("index.html", name=name_choice, link=about_link)


@app.route("/about")
def about():
    return "Mein Name ist Karthik Kones und ich bin der Initiator dieser Seite. Erstellt wurde diese Seite in Zusammenarbeit mit meinem Dozenten."


@app.route("/form", methods=["get", "post"])
def form():
    if request.method.lower() == "get":
        return render_template("formular.html")
    if request.method.lower() == "post":
        a=request.form.get("Name") #json Veknküpfung - holt Daten aus Formular ab und speichert sie ab
        b=request.form.get("Autor")
        c=request.form.get("Genre")
        d=request.form.get("Anzahl Seiten")
        e=request.form.get("Comment")
        my_data = {"Name": a, "Autor": b, "Genre": c, "Anzahl Seiten": d, "Comment": e}

        data=opendata()
        data.append(my_data)
        storedata(data)

        return render_template("formular.html")


@app.route("/übersicht")
def ubersicht():
        bucherliste = []
        data = opendata()
        for element in data:
            bucherliste.append([element["Name"], element["Autor"], element["Genre"], element["Anzahl Seiten"], element["Comment"]])
        return render_template("übersicht.html", liste=bucherliste)



@app.route("/suche")
def suche():
    return render_template("suche.html")


@app.route("/gelesen")
def gelesen():
    return render_template("gelesen.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)