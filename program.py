
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
        polozkyaceny[polozka] = (
            cena,
            kategoria,
            povodne_mnozstva[polozka]
        )