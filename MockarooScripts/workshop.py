import random
import auto_directory
import json
from datetime import timedelta

def workshop_insert(cur,count=1000):

    cur.execute("SELECT COUNT(*) FROM workshop")

    if(cur.fetchone()[0]==0):

        with open(auto_directory.csv_data_path("workshop.json"), "r") as f:
            workshop_data = json.load(f)

        cur.execute("SELECT festival_id FROM festival")
        festival_id_list=[row[0] for row in cur.fetchall()]

        for w in workshop_data:

            festival_id=random.choice(festival_id_list)
            duration=generate_random_interval()

            cur.execute("""INSERT INTO public.workshop (workshop_id,name,capacity,type,difficulty,duration,prior_knowledge_required,festival_id)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(w["workshop_id"],w["name"],w["capacity"],w["type"],w["difficulty"],duration,
                        w["prior_knowledge_required"],festival_id))

def generate_random_interval():
    duration_minutes=random.randint(30,180)
    return timedelta(minutes=duration_minutes)
