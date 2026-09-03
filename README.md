# Portfolio Website

A Django portfolio starter with a responsive landing page and projects managed through Django admin.

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

Project cards are ordered by `display_order`; lower values appear first. Only projects marked as featured appear on the home page.

## Customize the site

- Replace the placeholder name, biography, skills, email, and location in `templates/portfolio/home.html` and `templates/base.html`.
- Change colors and layout in `static/css/site.css`.
- For deployment, set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and `DJANGO_ALLOWED_HOSTS` in the environment.
