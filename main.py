from flask import Flask
from flask import render_template
from flask import request
import plotly.express as px
from plotly.offline import plot
from mydata import opendata, storedata

app = Flask("__name__")


@app.route("/") #Mitteilung an App, welche URL ausgeführt werden soll
def grafik(): #Funktion beim Aufruf der URL
    data = opendata()
    counter_Roman = 0
    counter_Krimi = 0
    counter_SciFi = 0
    counter_Liebe = 0
    counter_Sachbuecher = 0
    counter_Rest = 0
    summe_buecher = []

    for alle_elemente in data: #Elemente der data.json werden hier in einem Loop geprüft
        for values in alle_elemente.values(): #Values der Elemente werden nach Genre in einem Loop geprüft und dazugezählt
            if values == "Roman":
                counter_Roman = counter_Roman + 1

            elif values == "Krimi":
                counter_Krimi = counter_Krimi + 1

            elif values == "Science Fiction":
                counter_SciFi = counter_SciFi + 1

            elif values == "Liebe":
                counter_Liebe = counter_Liebe + 1

            elif values == "Sachbücher":
                counter_Sachbuecher = counter_Sachbuecher + 1

            elif values == "Restliche Bücher":
                counter_Rest = counter_Rest + 1
    summe_buecher.append(counter_Roman) #alle gezählten werden zur Liste summe_buecher hinzugefügt
    summe_buecher.append(counter_Krimi)
    summe_buecher.append(counter_SciFi)
    summe_buecher.append(counter_Liebe)
    summe_buecher.append(counter_Sachbuecher)
    summe_buecher.append(counter_Rest)

    genre = ["Roman", "Krimi", "SciFi", "Liebe", "Sachbücher", "Restliche Bücher"]

    # 2 unabhängige Listen -> Wert 1 aus Liste 1 wird Wert 1 aus Liste 2 zugewiesen -> genau so für die anderen auch!

    # Visualisierung mit Plotly
    # https://plotly.com/python/bar-charts/
    fig = px.bar(x=genre, y=summe_buecher) #aus Liste genre werden x-Werte herausgezogen und aus Liste summe_buecher werden y-Werte gezogen
    fig.update_layout(
        title="Bücher pro Genre in der Datenbank",
        xaxis_title="Genre",
        yaxis_title="Anzahl Bücher")
    div = plot(fig, output_type="div")
    return render_template("index.html", visual=div) #index.html mit diesem Befehl ausgegeben und die visual steht für den Jinja-Eintrag auf der HTMl-Seite


@app.route("/about") #Mitteilung an App, welche URL ausgeführt werden soll
def about():
    return render_template("about.html") #about.html mit diesem Befehl ausgegeben


@app.route("/form", methods=["get", "post"]) #Mitteilung an App, welche URL ausgeführt werden soll + Methode Post und Get lassen die Dateingabe und Verwaltung zu
def form(): #Funktion für die obengenannte URL
    if request.method.lower() == "get": #Mit dem Formular werden Daten per Get abgeholt
        return render_template("formular.html")
    if request.method.lower() == "post":
        name = request.form.get("Name") #json Verknüpfung - holt Daten aus Formular ab und speichert sie ab
        autor = request.form.get("Autor")
        c=request.form.get("Genre")
        d=request.form.get("Anzahl Seiten")
        e=request.form.get("Comment")
        f= request.form.getlist("gelesen")
        my_data = {"Name": name, "Autor": autor, "Genre": c, "Anzahl Seiten": d, "Comment": e, "gelesen": f} #Dictionary-Struktur, welche im json File abgelegt ist

        data=opendata() #Daten werden hier zur json Datei hinzugefügt
        data.append(my_data) #data_content ist eine Liste und mit diesem Befehl wird die Liste ergänzt
        storedata(data) #hier werden eingegebene Daten gespeichert

        return render_template("formular.html") #formular.html mit diesem Befehl ausgegeben


@app.route("/übersicht") #Mitteilung an App, welche URL ausgeführt werden soll
def ubersicht(): #Funktion für die URL
        bucherliste = [] #Liste, worin die eingegeben Einträge aus dem json abgelegt werden
        data = opendata() #wo die Daten vorhanden sind
        for element in data: #For-Loop damit die gespeichereten Daten für die neue Liste gefunden werden können
            bucherliste.append([element["Name"], element["Autor"], element["Genre"], element["Anzahl Seiten"], element["Comment"]]) #hinzufügen der Daten auf die neue Liste
        return render_template("übersicht.html", liste=bucherliste) #übersicht.html mit diesem Befehl ausgegeben + liste wird auf der Seite ersichtlich


@app.route("/genre", methods=["POST", "GET"])#Mitteilung an App, welche URL ausgeführt werden soll + Methode Post und Get lassen die Dateingabe und Verwaltung zu
def genre_filter(): #Funktion für die URL
    if request.method.lower() == "get": #hier werden Daten per Get abgeholt
        return render_template("genre.html") #genre.html mit diesem Befehl ausgegeben
    if request.method.lower() == "post": #post-Methode für die Ausgabe der Genre
        genre = request.form.get("Genre")
    genrefilter = [] #Liste, für die Ausgabe der einzelnen Genre
    data = opendata() #wo die Daten vorhanden sind
    for element in data: #for-Loop für data um Elemente durchsuchen zu können
        if element["Genre"] == genre:
            genrefilter.append([element["Name"], element["Autor"], element["Genre"], element["Anzahl Seiten"], element["Comment"]]) #wenn Element Genre vorhanden, sollen alle Elemente zur Liste hinzugefügt werden
    return render_template("genre.html", liste=genrefilter) #genre.html mit diesem Befehl ausgegeben + liste wird auf der Seite ersichtlich


@app.route("/gelesen") #Mitteilung an App, welche URL ausgeführt werden soll
def gelesen():
        gelesen = [] #neue Liste für die gelesenen Bücher
        data = opendata()
        for element in data: #for-Loop für data um Elemente durchsuchen zu können
            if element["gelesen"] == ["on"]: #wenn Häckchen beim Formular gesetzt, dann werden die Datensätze "on" beinhalten und nur diese Daten werden zur neuen Liste hinzugefügt
                gelesen.append([element["Name"], element["Autor"], element["Genre"], element["Anzahl Seiten"], element["Comment"]])
        return render_template("übersicht.html", liste=gelesen) #genre.html mit diesem Befehl ausgegeben + liste wird auf der Seite ersichtlich


if __name__ == "__main__":
    app.run(debug=True, port=5000)