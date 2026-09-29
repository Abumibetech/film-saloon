# FILM SALOON — Full Modern Website + PWA

This is a clean standalone Django 5.2 project using the supplied FILM SALOON logo.

PowerShell:
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations movies
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_film_saloon
python manage.py collectstatic --noinput
python manage.py runserver

Open: http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/

Features:
- Most Recommended
- Top 5 Movies of the Day
- Other Recommended Movies
- Likes / dislikes
- Weekly voting, one vote per browser session per active vote
- Genres: romance, comedy, action, sci-fi, suspense, thriller, adventure, faith based
- Movie search
- Actor profiles and actor search
- Best Movie Clips
- Advertisements
- Light/dark mode
- Pure black dark theme
- Responsive mobile UI
- PWA manifest + service worker + install button
- Supplied FILM SALOON logo used for branding and app icons

For production, use HTTPS. Chromium browsers expose the native install prompt only when the browser considers the PWA installable; the button uses beforeinstallprompt. iPhone/iPad Safari uses Share -> Add to Home Screen.
