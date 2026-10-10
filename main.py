
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os
import secrets
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

import program


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    SessionMiddleware,
    secret_key= os.environ["SESSION_SECRET"],
    max_age=3600,
    same_site= "lax",
    https_only= False
)

@app.get("/admin/login")
async def prihlasenie(
    request: Request
):
    return templates.TemplateResponse(
        request,
        "admin_login.html"
    )

@app.post("/admin/login")
async def admin_vstup(
    request: Request,
    password: str = Form(...)
):
    admin_password = os.environ["ADMIN_PASSWORD"]

    if secrets.compare_digest(password, admin_password):
        request.session["admin_authenticated"] = True
        return RedirectResponse("/admin", status_code=303)
    
    return RedirectResponse("/admin/login", status_code=303)

@app.get("/admin")
async def adminpanel(request: Request):
    if not request.session.get("admin_authenticated"):
        return RedirectResponse("/admin/login", status_code=303)

    return templates.TemplateResponse(
        request,
        "admin.html",
        {
            "produkty": program.polozkyaceny,
            "sprava": None,
            "chyba": None
        }
    )

@app.post("/admin/add")
async def admin_add(
    request: Request,
    polozka: str = Form(...),
    cena: float = Form(...),
    kategoria: str = Form(...),
    mnozstvo: int = Form(...)
):
    if not request.session.get("admin_authenticated"):
        return RedirectResponse("/admin/login", status_code=303)

    uspech, sprava = program.pridaj_produkt(
        polozka, cena, kategoria, mnozstvo
    )

    return templates.TemplateResponse(
        request,
        "admin.html",
        {
            "produkty": program.polozkyaceny,
            "sprava": sprava if uspech else None,
            "chyba": None if uspech else sprava
        },
        status_code=200 if uspech else 400
    )

@app.post("/admin/edit")
async def admin_edit(
    request: Request,
    povodny_nazov: str = Form(...),
    polozka: str = Form(...),
    cena: float = Form(...),
    kategoria: str = Form(...),
    mnozstvo: int = Form(...)
):
    if not request.session.get("admin_authenticated"):
        return RedirectResponse("/admin/login", status_code=303)

    uspech, sprava = program.uprav_produkt(
        povodny_nazov,
        polozka,
        cena,
        kategoria,
        mnozstvo
    )

    return templates.TemplateResponse(
        request,
        "admin.html",
        {
            "produkty": program.polozkyaceny,
            "sprava": sprava if uspech else None,
            "chyba": None if uspech else sprava
        },
        status_code=200 if uspech else 400
    )

@app.post("/admin/delete")
async def admin_delete(
    request: Request,
    polozka: str = Form(...)
):
    if not request.session.get("admin_authenticated"):
        return RedirectResponse("/admin/login", status_code=200)

    uspech, sprava = program.odstran_produkt(polozka)

    return templates.TemplateResponse(
        request,
        "admin.html",
        {
            "produkty": program.polozkyaceny,
            "sprava": sprava if uspech else None,
            "chyba": None if uspech else sprava
        },
        status_code=200 if uspech else 400
    )

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

@app.get("/about", response_class=HTMLResponse)
async def aboutvstup(
    request: Request
):

    return templates.TemplateResponse(
        request,
        "about.html"
    )
