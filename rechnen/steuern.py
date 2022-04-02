
def berechnen(betrag, prozent=10):
    ergebnis = betrag * (prozent / 100)
    return ergebnis

def abgaben(betrag):
    ergebnis = betrag * 0.1

    #return "{} {}" .format("CHF", ergebnis)
    return ergebnis


#steuer_betrag = steuern(100)
#print(steuer_betrag)

#buch_steuer = steuern(100, prozent = 5)
#print(buch_steuer)