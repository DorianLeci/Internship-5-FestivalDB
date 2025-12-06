import random

def workshop_mentor_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM workshop_mentor")

    if(cur.fetchone()[0]==0):

        cur.execute("SELECT workshop_id FROM workshop")
        workshop_id_list=[row[0] for row in cur.fetchall()]

        cur.execute("SELECT mentor_id FROM mentor")
        mentor_id_list=[row[0] for row in cur.fetchall()]

        batch_insert=[]

        for _ in range(count):
            workshop_id=random.choice(workshop_id_list)
            mentor_id=random.choice(mentor_id_list)

            batch_insert.append((workshop_id,mentor_id))

        cur.executemany("INSERT INTO public.workshop_mentor (workshop_id,mentor_id) VALUES (%s,%s) ON CONFLICT (workshop_id,mentor_id ) DO NOTHING",batch_insert)