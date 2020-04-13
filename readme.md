
## Getting Started PyCharm

1. Repo clonen
2. In PyCharm virtualenv einrichten: File - Settings -
   Project Interpreter - Zahnrad - Add - Virtualenv environment - OK
3. Im Terminal requirements installieren: `pip install -r requirements.txt`
4. Run profile erstellen: oben rechts Edit Configurations - Plus - Python -
   Script Path ändern zu Module name - eintragen: app
Unter environment `BM_WP_DATABASE_URI` definieren nach diesem Format: `mysql://user:password@server/database`

5. Dann kann das Backend immer über den Play-Button oben rechts gestartet werden

## Getting Started Terminal

1. Repo clonen
2. `virtualenv venv --python=/usr/bin/python3`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `export BM_WP_DATABASE_URI=siehe oben`
6. `python app.py`

