from flask import Flask
from flask import render_template
from flask import request
import plotly.express as px
from plotly.offline import plot
from mydata import opendata, storedata

app = Flask("__name__")


@app.route("/")
def grafik():
    data = opendata()
    counter_Roman = 0
    counter_Krimi = 0
    counter_SciFi = 0
    counter_Liebe = 0
    counter_Sachbücher = 0
    counter_Rest = 0
    summe_buecher = []

    for alle_elemente in data:
        for values in alle_elemente.values():
            if values == "Roman":
                counter_Roman = counter_Roman + 1

            elif values == "Krimi":
                counter_Krimi = counter_Krimi + 1

            elif values == "Science Fiction":
                counter_SciFi = counter_SciFi + 1

            elif values == "Liebe":
                counter_Liebe = counter_Liebe + 1

            elif values == "Sachbücher":
                counter_Sachbücher = counter_Sachbücher + 1

            elif values == "Restliche Bücher":
                counter_Rest = counter_Rest + 1
    summe_buecher.append(counter_Roman)
    summe_buecher.append(counter_Krimi)
    summe_buecher.append(counter_SciFi)
    summe_buecher.append(counter_Liebe)
    summe_buecher.append(counter_Sachbücher)
    summe_buecher.append(counter_Rest)

    genre = ["Roman", "Krimi", "SciFi", "Liebe", "Sachbücher", "Restliche Bücher"]
    print(genre)
    print(summe_buecher)
    #2 unabhängige Listen -> Wert 1 aus Liste 1 wird Wert 1 aus Liste 2 zugewiesen -> genau so für die anderen auch!

#Visualisierung mit Plotly
    fig = px.bar(x=genre, y=summe_buecher)
    fig.update_layout(
        title="Bücher pro Genre in der Datenbank",
        xaxis_title="Genre",
        yaxis_title="Anzahl Bücher")
    div = plot(fig, output_type="div")
    return render_template("Index.html", visual=div)


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