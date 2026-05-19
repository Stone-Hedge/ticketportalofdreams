PY=python3
run:
	$(PY) manage.py runserver 0.0.0.0:8000
migrate:
	$(PY) manage.py migrate
sample:
	$(PY) manage.py create_sample_data
test:
	$(PY) manage.py test
import:
	$(PY) manage.py import_xlsx $(FILE)
export:
	$(PY) manage.py export_xlsx $(FILE)
backup:
	$(PY) manage.py backup_db
