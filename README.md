# Internship-5-FestivalDB

<b>Steps to install project</b>

```
git clone git@github.com:DorianLeci/Internship-5-FestivalDB.git
cd Internship-5-FestivalDB
```
After positioning inside project folder you will see the folder SqlFiles which you must open in PgAdmin.</br>
Inside there is 
</br>
1)<b>SqlCreationScript.sql</b> for creating database tables and adding constraints.
</br>
2) <b>TriggerFunctions.sql</b> for adding triggers to tables.
</br>
3)<b>QueryToDatabase.sql</b> for checking how database work with 15 querys.
</br>

Before running any of sql scripts in pgAdmin,you must create database with name 
```
Internship-5-FestivalDB
```

After creating database and running SqlCreationScript and TriggerFunctions you must create python virtual enviroment in main directory so you can install requirements for running "script.py" which automatically inserts data from json to created database.

Steps:

On windows:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On macos/linux:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then type 
```
cd MockarooScripts
python script.py
```

After running python script you can query your database.



