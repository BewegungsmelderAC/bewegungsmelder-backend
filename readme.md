
## Getting Started PyCharm

1. Repo clonen
2. In PyCharm virtualenv einrichten: File - Settings -
   Project Interpreter - Zahnrad - Add - Virtualenv environment - OK
3. Im Terminal requirements installieren: `pip install -r requirements.txt`
4. Run profile erstellen: oben rechts Edit Configurations - Plus - Python -
   Script Path ändern zu Module name - eintragen: flask, Parameters: run -
Unter environment alle Variablen definieren, die in `config.py` required sind -
    zusätzlich `FLASK_APP=app`, `FLASK_ENV=development` und `BM_LOGGING_LEVEL=DEBUG`
5. Dann kann das Backend immer über den Play-Button oben rechts gestartet werden

## Getting Started Terminal

1. Repo clonen
2. `virtualenv venv --python=/usr/bin/python3`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `export FLASK_APP=app;export FLASK_ENV=development`
6. export auch alle required Parameter aus `config.py`
7. `flask run`

