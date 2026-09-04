# Portfolio Website

Afraim Elkes Eleia's Django portfolio, with an animated responsive landing page and projects managed through Django admin.

## Run locally on Windows

```powershell
cd D:\Education\Portfolio\portfolio_website
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

If the included `.venv` already exists on your machine, start with the activation command.

Open <http://127.0.0.1:8000/> in your browser.

## Add portfolio projects

Create an admin account, start the server, then visit <http://127.0.0.1:8000/admin/>:

```powershell
python manage.py createsuperuser
python manage.py runserver
```

Project cards are ordered by `display_order`; lower values appear first. Only projects marked as featured appear on the home page. Each project supports:

- A reusable slug and project type
- Summary and feature bullets
- Comma-separated technologies
- Local or remote artwork
- Source and live links

Rihla and VoltMarket are created by the project data migration, so a fresh database receives the current portfolio content automatically.
When a live link is present, the project artwork opens it; otherwise the artwork opens the source repository.

### DEPI projects

The DEPI subsection inside Selected work uses compact repository cards without screenshots.
Set a project's **Section** to **DEPI projects** and keep **Featured** enabled to show it there.
The migration adds three clearly labeled mock projects: TaskFlow, Weatherly, and SpendWise.
Replace their titles, summaries, features, and technologies in Django admin, add the real
**Source URL**, then uncheck **Is mock**. Empty source URLs display “Repository coming soon”
without linking to a made-up repository. **Display order** controls the order within each section.

The DEPI logo is stored locally at `static/images/depi-logo.webp`; it is sourced from
[eYouth's partner logo](https://eyouthlearning.com/businessLogos/business64.webp).
The program name and official website are [Digital Egypt Pioneers Initiative](https://depi.gov.eg/).

### ITI Summer Training

The ITI Summer Training subsection follows DEPI and focuses on Python, Django, and Flask.
**CrowdFund** replaces the original mock entry with the real Django crowdfunding project,
its [GitHub repository](https://github.com/AfraimElkesEleia/ITI-SummerTraining-FullStack-Crowdfunding),
and the supplied banner at `static/images/iti-crowdfund-project-banner.png`.
The project uses Django and PostgreSQL; Flask remains part of the broader training description.
ITI projects with artwork use a full-width preview; projects without artwork retain compact repository cards.
In Django admin, choose **Section → ITI Summer Training** to edit these entries. Keep **Featured** enabled
to display a project, and use **Is mock** only for placeholder content.

The ITI logo is stored locally at `static/images/iti-logo.png`, downloaded from the
[official ITI website](https://iti.gov.eg/assets/images/organization/iti-logo.png).

## Validate changes

```powershell
python manage.py check
python manage.py makemigrations --check
python manage.py test
```

## Customize the site

- Replace the placeholder name, biography, skills, email, and location in `templates/portfolio/home.html` and `templates/base.html`.
- Change colors and layout in `static/css/site.css`.
- For deployment, set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and `DJANGO_ALLOWED_HOSTS` in the environment.
