
polozkyaceny = {
    "jablko": (1, "ovocie", 100),
    "marhula": (1.5, "ovocie", 60),
    "banan": (1.5, "ovocie", 20),
    "petrzlen": (2, "zelenina", 35),
    "cukor": (2.3, "sladkosti", 5),
    "mrkva": (2, "zelenina", 35),
    "cokolada": (3, "sladkosti", 20),
    "rohlik": (0.10, "ine", 300)
}

povodne_mnozstva = {
    polozka: data[2]
    for polozka, data in polozkyaceny.items()
}

kupon = {
    "beli67": 30,
    "dariuskral": 30,
    "matojegoat": 20,
    "MGfitman69": 20,
    "LIMITED": 40
}

kosik = []
pouzity_kupon = None


def uvod():
    text = "Dobry den, nech sa paci mozte si vybrat\n"
    vysledok = ""

    for polozka, (cena, kategoria, mnozstvo) in polozkyaceny.items():
        vysledok += f"{polozka} - {cena}€ - ostava {mnozstvo}\n"

    return text + vysledok


def nakup(vyber, value):
    vyber = str(vyber).strip().lower()

    if vyber not in polozkyaceny:
        return "Takýto produkt neexistuje."

    try:
        kolko = int(value)
    except (ValueError, TypeError):
        return "Napis cislo."

    if kolko <= 0:
        return "Nechoď do minusu."

    cena, kategoria, mnozstvo = polozkyaceny[vyber]

    if kolko > mnozstvo:
        return "Nemame tolko kusov."

    mnozstvo -= kolko

    polozkyaceny[vyber] = (
        cena,
        kategoria,
        mnozstvo
    )

    kosik.append([
        vyber,
        cena,
        kategoria,
        kolko
    ])

    return f"Pridane do kosika: {vyber} x {kolko}"


def stav_kosika():
    pocet = 0
    cena = 0

    for polozka, cena_jednej, kategoria, mnozstvo in kosik:
        pocet += mnozstvo
        cena += cena_jednej * mnozstvo

    if pouzity_kupon is not None:
        zlava = kupon[pouzity_kupon]
        cena = cena - (cena * zlava / 100)

    return pocet, cena


def pouzi_kupon(kod):
    global pouzity_kupon

    kod = str(kod).strip()

    if kod not in kupon:
        return "Neplatny kupon"

    if not kosik:
        return "Kosik je prazdny"

    povodna_cena = 0

    for polozka, cena, kategoria, mnozstvo in kosik:
        povodna_cena += cena * mnozstvo

    if kod == "LIMITED" and povodna_cena < 50:
        return "Pre kupon LIMITED musi byt nakup aspon 50 €"

    pouzity_kupon = kod

    zlava = kupon[kod]
    nova_cena = povodna_cena - (povodna_cena * zlava / 100)

    return (
        f"Kupon {kod} pouzity! "
        f"Zlava {zlava}% → cena: {nova_cena:.2f} €"
    )


def reset_nakupu():
    global pouzity_kupon

    kosik.clear()
    pouzity_kupon = None

    for polozka, (cena, kategoria, mnozstvo) in polozkyaceny.items():

        povodne = povodne_mnozstva.get(polozka, 0)

        polozkyaceny[polozka] = (
            cena,
            kategoria,
            povodne
        )

def pridaj_produkt(polozka, cena, kategoria, mnozstvo):
    polozka = polozka.strip()
    kategoria = kategoria.strip()

    if not polozka or not kategoria:
        return False, "Polozka musi mat nazov aj kategoriu"

    if polozka in polozkyaceny:
        return False, "polozka uz s tymto nazvvom existuje"

    if cena < 0 or mnozstvo < 0:
        return False, "cena aj mnozstvo nemozu byt zaporne"

    polozkyaceny[polozka] = (
        float(cena),
        str(kategoria),
        int(mnozstvo)
    )

    povodne_mnozstva[polozka] = int(mnozstvo)

    return True, "produkt bol pridany"

def uprav_produkt(novy_nazov, stary_nazov, cena, kategoria, mnozstvo):
    novy_nazov = novy_nazov.strip()
    kategoria = kategoria.strip()

    if stary_nazov not in polozkyaceny:
        return False, "produkt sa nenasiel"

    if not novy_nazov or not kategoria:
        return False, "nazov aj kategoria su povinne"

    if cena < 0 or mnozstvo < 0:
        return False, "cena aj mnozstvo nemoze byt zaporne"

    if novy_nazov != stary_nazov and novy_nazov in polozkyaceny:
        return False, "produkt s tymto nazvom uz existuje"

    nova_hodnota = (
        float(cena),
        str(kategoria),
        int(mnozstvo)
    )

    nove_produkty = {}

    for nazov, data in polozkyaceny.items():
        if nazov == stary_nazov:
         nove_produkty[novy_nazov] = nova_hodnota
        else:
            nove_produkty[nazov] = data

    if novy_nazov != stary_nazov:
        povodne_mnozstva.pop(stary_nazov, None)

    povodne_mnozstva[novy_nazov] = int(mnozstvo)

    polozkyaceny.clear()
    polozkyaceny.update(nove_produkty)

    return True, "podukt bol upraveny"

def odstran_produkt(polozka):
    if polozka not in polozkyaceny:
        return False, "produkt sa nenasiel"

    del polozkyaceny[polozka]
    povodne_mnozstva.pop(polozka, None)

    return True, "produkt bol odstraneny"
