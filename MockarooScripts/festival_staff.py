import helper
import random

def festival_staff_insert(cur,count=1000):

    cur.execute("SELECT COUNT(*) FROM festival_staff")

    if(cur.fetchone()[0]==0):
        batch_insert=[]

        cur.execute("SELECT festival_id,start_date,end_date FROM festival")
        festival_list=cur.fetchall()

        cur.execute("SELECT staff_id FROM staff")
        staff_id_list =[row[0] for row in cur.fetchall()]

        staff_schedule={staff_id:[] for staff_id in staff_id_list}

        for (fes_id,fes_start,fes_end) in festival_list:
            
            random.shuffle(staff_id_list)
                        
            availible_staff=[s for s in staff_id_list 
            if not any(helper.is_there_overlap(fes_start,fes_end,start_date,end_date) for start_date,end_date in staff_schedule[s])]

            chosen_staff=random.choice(availible_staff)

            staff_schedule[chosen_staff].append((fes_start,fes_end))
            batch_insert.append((fes_id,chosen_staff))  



        cur.executemany("INSERT INTO public.festival_staff (festival_id,staff_id) VALUES (%s,%s)",batch_insert)



