

import plotly.express as px

from flask import Flask
from flask import render_template
from flask import request

from mydata import opendata, storedata

app = Flask("__name__")


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/form", methods=["get", "post"])
def form():
    if request.method.lower() == "get":
        return render_template("formular.html")
    if request.method.lower() == "post":
        name = request.form.get("Name") #json Verknüpfung - holt Daten aus Formular ab und speichert sie ab
        autor = request.form.get("Autor")
        c=request.form.get("Genre")
        d=request.form.get("Anzahl Seiten")
        e=request.form.get("Comment")
        f= request.form.getlist("gelesen")
        my_data = {"Name": name, "Autor": autor, "Genre": c, "Anzahl Seiten": d, "Comment": e, "gelesen": f}

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


@app.route("/genre", methods=["POST", "GET"])
def genre_filter():
    if request.method.lower() == "get":
        return render_template("genre.html")
    if request.method.lower() == "post":
        genre = request.form.get("Genre")
    genrefilter = []
    data = opendata()
    for element in data:
        if element["Genre"] == genre:
            genrefilter.append([element["Name"], element["Autor"], element["Genre"], element["Anzahl Seiten"], element["Comment"]])
    return render_template("genre.html", liste=genrefilter)


@app.route("/gelesen")
def gelesen():
        gelesen = []
        data = opendata()
        for element in data:
            if element["gelesen"] == ["on"]:
                gelesen.append([element["Name"], element["Autor"], element["Genre"], element["Anzahl Seiten"], element["Comment"]])
        return render_template("übersicht.html", liste=gelesen)


if __name__ == "__main__":
    app.run(debug=True, port=5000)