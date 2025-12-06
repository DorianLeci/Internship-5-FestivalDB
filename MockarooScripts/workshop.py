import random
import auto_directory
import json
from datetime import timedelta
import helper

def workshop_insert(cur,count=1000):

    cur.execute("SELECT COUNT(*) FROM workshop")

    if(cur.fetchone()[0]==0):

        with open(auto_directory.csv_data_path("workshop.json"), "r") as f:
            workshop_data = json.load(f)

        cur.execute("SELECT festival_id,start_date,end_date FROM festival")
        festival_list=cur.fetchall()

        for w in workshop_data:

            festival=random.choice(festival_list)
            start_time=helper.generate_purchase_time(festival[1],festival[2])
            duration=generate_random_interval()

            cur.execute("""INSERT INTO public.workshop (workshop_id,name,capacity,type,difficulty,duration,prior_knowledge_required,festival_id,start_time)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(w["workshop_id"],w["name"],w["capacity"],w["type"],w["difficulty"],duration,
                        w["prior_knowledge_required"],festival[0],start_time))

def generate_random_interval():
    duration_minutes=random.randint(30,300)
    return timedelta(minutes=duration_minutes)
