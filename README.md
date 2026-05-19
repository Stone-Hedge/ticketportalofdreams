# The Ticket Portal of Dreams
Private Django app for shared Arsenal season ticket allocations.

## Setup
1. `python3 -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `cp .env.example .env`
4. `python manage.py migrate`
5. `python manage.py create_sample_data`
6. `python manage.py runserver`

## Git sync
- First-time clone: `git clone <repo-url> && cd ticketportalofdreams`
- Pull latest changes on current branch: `git pull`
- Pull latest changes from main explicitly: `git pull origin main`

## Pages
/passcode /choose-person /fixtures /dashboard /audit /admin-portal

## Import/export
- Import: `python manage.py import_xlsx path.xlsx` or admin portal upload.
- Export xlsx: `python manage.py export_xlsx out.xlsx`
- Export csv: `python manage.py export_xlsx out.csv --csv`

## VPS deploy
- Run app on localhost:8000.
- Configure Caddy using `deploy/Caddyfile.example`.
- Configure systemd using `deploy/ticketportal.service`.

## Backup/restore
- Backup: `python manage.py backup_db` or `scripts/backup_db.sh`
- Restore: replace sqlite file at `DATABASE_PATH`.

## Security
- Use `GENERAL_PASSCODE_HASH` and `ADMIN_PASSCODE_HASH` in production.
- Set `DJANGO_DEBUG=False`, HTTPS via Caddy, secure cookies enabled.
- Sensitive details are stored in `SensitiveDetail` and only available via admin portal flows.

## Troubleshooting
- If passcode lockout occurs, wait 5 minutes or clear browser session.
- If static files missing, run `python manage.py collectstatic`.

## Future improvements
- richer importer mapping preview
- pagination and better audit filters
- recurring automated encrypted backups
