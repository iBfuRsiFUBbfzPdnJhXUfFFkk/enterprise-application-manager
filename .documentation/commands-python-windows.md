# Commands Python Windows

## Activate The Python VENV

```bash
bash .venv/Scripts/activate
```

## Freeze The VENV Requirements

```bash
.venv/Scripts/python -m pip freeze > requirements.txt
```

## Dump The Database

```bash
.venv/Scripts/python manage.py dumpdata --indent=2 > data.json
```

## Load The Database

```bash
.venv/Scripts/python manage.py loaddata data.json
```

## Deactivate The VENV

```bash
deactivate
```