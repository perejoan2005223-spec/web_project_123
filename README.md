# ValoracioProfes

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0.2-092E20?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-Acad%C3%A8mic-lightgrey)

Plataforma web desenvolupada amb **Django** que permet consultar informació dels professors del Grau d'Informàtica de la **Universitat de Lleida (UdL)**, les assignatures que imparteixen, les seves publicacions i deixar valoracions constructives sobre la seva docència.

El projecte s'emmarca dins l'assignatura **Projecte Web** i ha estat realitzat en grup.

---

## Taula de continguts

- [Característiques](#característiques)
- [Stack tecnològic](#stack-tecnològic)
- [Estructura del projecte](#estructura-del-projecte)
- [Requisits previs](#requisits-previs)
- [Instal·lació i posada en marxa](#installació-i-posada-en-marxa)
  - [Opció A — Entorn virtual local](#opció-a--entorn-virtual-local)
  - [Opció B — Docker](#opció-b--docker)
- [Poblar la base de dades (scraper)](#poblar-la-base-de-dades-scraper)
- [Rutes principals](#rutes-principals)
- [Model de dades](#model-de-dades)
- [Panell d'administració](#panell-dadministració)
- [Autors](#autors)
- [Llicència](#llicència)

---

## Característiques

- **Catàleg de professors** del Grau d'Informàtica de la UdL, organitzats per departament.
- **Fitxa individual** de cada professor amb foto, departament i assignatures que imparteix.
- **Cercador amb autocompletar** (jQuery UI) a la llista de professors.
- **Sistema d'usuaris** integrat de Django: registre, inici i tancament de sessió.
- **Model de valoracions** amb nota global, nota de dificultat i comentari, validades entre 0 i 10.
- **Gestió de publicacions acadèmiques** vinculades a professors amb ordre d'autoria.
- **Scraper automàtic** que importa professors, assignatures i publicacions des del directori oficial del Grau.
- **Desplegament amb Docker** llest per produir.
- **Fitxers estàtics servits amb WhiteNoise** i aplicació servida amb **Gunicorn**.

---

## Stack tecnològic

| Capa | Tecnologia |
|------|------------|
| Backend | Python 3.13, Django 6.0.2 |
| Base de dades | SQLite 3 |
| Frontend | HTML5, CSS3, jQuery + jQuery UI |
| Scraping | Requests, BeautifulSoup 4, lxml |
| Servidor WSGI | Gunicorn |
| Fitxers estàtics | WhiteNoise |
| Gestor de dependències | uv |
| Contenidors | Docker, Docker Compose |

---

## Estructura del projecte

```
web_project/
├── blog/                           # App principal (professors, assignatures, valoracions)
│   ├── management/
│   │   └── commands/
│   │       └── scrape_professors.py   # Comanda per importar dades de la UdL
│   ├── migrations/                 # Migracions de la BD
│   ├── static/blog/                # CSS i recursos estàtics
│   ├── admin.py                    # Registre de models a l'admin
│   ├── apps.py
│   ├── models.py                   # Models: Department, Professor, Subject, Review...
│   ├── urls.py                     # Rutes de l'app blog
│   └── views.py                    # Vistes: home, llista i detall de professor, signup
│
├── templates/
│   ├── base.html                   # Plantilla base (navbar, footer)
│   ├── blog/
│   │   ├── home.html
│   │   ├── professor_list.html
│   │   └── professor_detail.html
│   └── registration/
│       ├── login.html
│       └── signup.html
│
├── web_project/                    # Configuració del projecte Django
│   ├── settings.py
│   ├── urls.py                     # URLs arrel
│   ├── wsgi.py
│   └── asgi.py
│
├── db.sqlite3                      # Base de dades SQLite
├── Dockerfile                      # Imatge Docker de l'aplicació
├── docker-compose.yml              # Orquestració del contenidor
├── manage.py                       # Utilitat de línia de comandes de Django
├── pyproject.toml                  # Dependències (gestionades amb uv)
├── uv.lock                         # Lockfile reproduïble
└── README.md
```

---

## Requisits previs

Abans de començar, assegura't de tenir instal·lat:

- **Python 3.13** o superior
- **pip** (inclòs amb Python) o **[uv](https://github.com/astral-sh/uv)** (recomanat)
- **Git** per clonar el repositori
- Opcionalment, **Docker** i **Docker Compose** si prefereixes l'opció contenidoritzada

---

## Instal·lació i posada en marxa

### Opció A — Entorn virtual local

1. **Clona el repositori**

   ```bash
   git clone <URL_DEL_REPOSITORI>
   cd web_project
   ```

2. **Crea i activa un entorn virtual**

   - A Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - A Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. **Instal·la les dependències**

   Amb **uv** (recomanat, ja que el projecte ja porta `pyproject.toml` i `uv.lock`):
   ```bash
   uv pip install -r pyproject.toml
   ```

   Amb **pip** tradicional:
   ```bash
   pip install django beautifulsoup4 lxml requests gunicorn whitenoise
   ```

4. **Aplica les migracions**

   ```bash
   python manage.py migrate
   ```

5. **Crea un superusuari** (per accedir a l'admin)

   ```bash
   python manage.py createsuperuser
   ```

6. **(Opcional) Pobla la BD amb dades reals**

   ```bash
   python manage.py scrape_professors
   ```

7. **Arrenca el servidor de desenvolupament**

   ```bash
   python manage.py runserver
   ```

   Accedeix a [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Opció B — Docker

El projecte inclou un `Dockerfile` i un `docker-compose.yml` que s'encarreguen d'instal·lar dependències, aplicar migracions, executar l'scraper i arrencar Gunicorn automàticament.

1. **Crea un fitxer `.env`** a l'arrel (pots deixar-lo buit o afegir variables com `PORT`):

   ```env
   PORT=8000
   ```

2. **Construeix i arrenca el contenidor**

   ```bash
   docker-compose up --build
   ```

3. **Accedeix a l'aplicació**: [http://localhost:8000/](http://localhost:8000/)

> El `Dockerfile` executa `collectstatic`, `migrate` i `scrape_professors` durant la construcció, de manera que l'aplicació arrencarà ja amb dades carregades.

---

## Poblar la base de dades (scraper)

El projecte inclou una comanda personalitzada de Django que extreu la informació dels professors del directori oficial del Grau d'Informàtica de la UdL:

```bash
python manage.py scrape_professors
```

Aquesta comanda:

- Descarrega la pàgina `https://grauinformatica.udl.cat/es/pla-formatiu/professorat/`.
- Crea automàticament els **departaments** i els **professors** que encara no existeixin a la BD.
- Visita la fitxa individual de cada professor per importar les seves **assignatures** i **publicacions**.
- Utilitza `get_or_create` per evitar duplicats, de manera que es pot tornar a executar amb seguretat.

> **Nota:** per defecte la comanda assigna 6 crèdits a cada assignatura i l'any 2026 a les relacions professor-assignatura. Aquests valors es poden ajustar manualment des del panell d'administració.

---

## Rutes principals

| URL | Vista | Descripció |
|-----|-------|------------|
| `/` | `home` | Pàgina d'inici amb presentació del projecte |
| `/profesores/` | `ProfessorListView` | Llistat de tots els professors amb cercador |
| `/profesores/<id>/` | `ProfessorDetailView` | Fitxa individual d'un professor |
| `/accounts/login/` | Django auth | Formulari d'inici de sessió |
| `/accounts/logout/` | Django auth | Tancament de sessió |
| `/signup/` | `PostSignUpView` | Registre de nous usuaris |
| `/admin/` | Django admin | Panell d'administració |

---

## Model de dades

L'aplicació gira al voltant de vuit entitats principals:

- **`Department`** — Departament universitari al qual pertany un professor.
- **`Professor`** — Professor del Grau (nom, foto de perfil, departament).
- **`Title`** — Títol acadèmic d'un professor (categoria i data d'expedició).
- **`Subject`** — Assignatura (nom, descripció, crèdits).
- **`Prof_Subject`** — Taula d'associació N:M entre `Professor` i `Subject`, amb l'any acadèmic com a atribut.
- **`Publication`** — Publicació científica (títol, any, URL).
- **`Professor_Publication`** — Taula d'associació N:M entre `Professor` i `Publication`, amb el camp `author_order` per indicar l'ordre d'autoria.
- **`Review`** — Valoració feta per un `User` sobre un `Prof_Subject`, amb nota global, nota de dificultat (0–10) i comentari.

> El diagrama UML complet del model es troba a la memòria del projecte.

---

## Panell d'administració

Un cop creat el superusuari, pots accedir a `/admin/` per gestionar **tots els models** del projecte (departaments, professors, assignatures, publicacions, valoracions i usuaris) de forma visual. Tots estan registrats a `blog/admin.py`.

---

## Autors

Projecte realitzat en grup per a l'assignatura **Projecte Web** del Grau en Enginyeria Informàtica de la Universitat de Lleida.

- *Oriol Armengol Capdevila*
- *Iker Farré Sanjoaquín*
- *Pere Joan Garriga Voltas*
- *Víctor Marín Martínez*
- *Joel Sisó Giribet*
- *Pol Suárez Giménez*


---

## Llicència

Aquest projecte s'ha desenvolupat amb finalitats **acadèmiques** i no té una llicència d'ús comercial. El codi pot ser consultat i reutilitzat amb finalitats educatives, citant-ne els autors.

---

<p align="center">
  <em>Valoracions Profes — 2026</em>
</p>