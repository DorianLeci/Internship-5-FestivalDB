import json
import auto_directory
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta


def mentor_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM mentor")

    if(cur.fetchone()[0]==0):

        with open(auto_directory.csv_data_path("mentor.json"),"r") as f:
            mentor_data = json.load(f)

        cur.execute("SELECT performer_id FROM performer")
        performer_id_list=[row[0] for row in cur.fetchall()]

        cur.execute("SELECT staff_id FROM staff")
        staff_id_list=[row[0] for row in cur.fetchall()]

        for m in mentor_data:
            
            birth_date=datetime.strptime(m["birth_date"],"%m/%d/%Y")
            years_old=relativedelta(datetime.now(),birth_date).years

            if(m["years_of_experience"]<2 or years_old<18):
                continue
            
            if random.random()<0.5:
                performer=random.choice(performer_id_list)
                cur.execute("""
                INSERT INTO mentor (mentor_id, performer_id, birth_date, expertise_area, years_of_experience)
                VALUES (%s, %s, %s, %s, %s)
                """,(m["mentor_id"],performer,m["birth_date"],m["expertise_area"],m["years_of_experience"]))

                performer_id_list.remove(performer)

            else:
                staff=random.choice(staff_id_list)
                cur.execute("""
                INSERT INTO mentor (mentor_id, staff_id, birth_date, expertise_area, years_of_experience)
                VALUES (%s, %s, %s, %s, %s)
                """,(m["mentor_id"],staff,m["birth_date"],m["expertise_area"],m["years_of_experience"]))

                staff_id_list.remove(staff)