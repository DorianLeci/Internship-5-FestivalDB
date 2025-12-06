import random
import helper

def festival_performer_insert(cur,count=1000):

    cur.execute("SELECT COUNT(*) FROM festival_performer")

    if(cur.fetchone()[0]==0):
        batch_insert=[]

        cur.execute("SELECT festival_id,start_date,end_date FROM festival")
        festival_list=cur.fetchall()

        cur.execute("SELECT performer_id FROM performer")
        performer_id_list = [row[0] for row in cur.fetchall()]

        performer_schedule={performer_id:[] for performer_id in performer_id_list}

        for (fes_id,fes_start,fes_end) in festival_list:
            
            random.shuffle(performer_id_list)

            availible_performers=[p for p in performer_id_list 
                if not any(helper.is_there_overlap(fes_start,fes_end,start_date,end_date) for start_date,end_date in performer_schedule[p])]
            
            if(not availible_performers):
                continue
            
            chosen_performer=random.choice(availible_performers)

            performer_schedule[chosen_performer].append((fes_start,fes_end))
            batch_insert.append((fes_id,chosen_performer))               



        cur.executemany("INSERT INTO public.festival_performer (festival_id,performer_id) VALUES (%s,%s) ON CONFLICT (festival_id,performer_id) DO NOTHING",batch_insert)
