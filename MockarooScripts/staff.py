import auto_directory
import json
from dateutil.relativedelta import relativedelta
from datetime import date,datetime

def staff_insert(cur,count=1000):

    cur.execute("SELECT COUNT(*) FROM staff")

    if(cur.fetchone()[0]==0):

        with open(auto_directory.csv_data_path("staff.json"), "r") as f:
            staff_data = json.load(f)

        for s in staff_data:
            birth_date=datetime.strptime(s["birth_date"],"%m/%d/%Y")
            if(s["role"]=='zastitar' and relativedelta(date.today(),birth_date).years<21):
                continue

            cur.execute("INSERT INTO public.staff (staff_id,name,surname,birth_date,role,contact,has_safety_training) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                        (s["staff_id"],s["name"],s["surname"],s["birth_date"],s["role"],s["contact"],s["has_safety_training"]))

