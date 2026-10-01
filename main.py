from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import program

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def domov(request: Request):
    pocet, celkova_cena = program.stav_kosika()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "vysledky": None,
            "produkty": program.polozkyaceny,
            "kosik": program.kosik,
            "pocet": pocet,
            "celkova_cena": celkova_cena,
            "kupon_vysledok": None
        }
    )


@app.post("/", response_class=HTMLResponse)
async def skontroluj_vstup(
    request: Request,
    vyber: str = Form(...),
    value: int = Form(...)
):
    vysledok = program.nakup(vyber, value)

    pocet, celkova_cena = program.stav_kosika()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "vysledky": vysledok,
            "produkty": program.polozkyaceny,
            "kosik": program.kosik,
            "pocet": pocet,
            "celkova_cena": celkova_cena,
            "kupon_vysledok": None
        }
    )


@app.post("/kupony", response_class=HTMLResponse)
async def pouzi_kupon(
    request: Request,
    kupon: str = Form(...)
):
    kupon_vysledok = program.pouzi_kupon(kupon)

    pocet, celkova_cena = program.stav_kosika()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "vysledky": None,
            "produkty": program.polozkyaceny,
            "kosik": program.kosik,
            "pocet": pocet,
            "celkova_cena": celkova_cena,
            "kupon_vysledok": kupon_vysledok
        }
    )


@app.post("/reset")
async def reset_nakupu():
    program.reset_nakupu()

    return RedirectResponse(
        url="/",
        status_code=303
    )