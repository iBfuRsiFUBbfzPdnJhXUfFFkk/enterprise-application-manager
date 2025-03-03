# Commands Python UNIX

## Activate The Python VENV

```bash
bash .venv/bin/activate
```

## Freeze The VENV Requirements

```bash
.venv/bin/python -m pip freeze > requirements.txt
```

## Dump The Database

```bash
.venv/bin/python manage.py dumpdata --indent=2 > data.json
```

## Load The Database

```bash
.venv/bin/python manage.py loaddata data.json
```

## Deactivate The VENV

```bash
deactivate
```