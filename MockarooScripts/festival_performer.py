import random
import helper

def festival_performer_insert(cur,count=1000):
    batch_insert=[]

    cur.execute("SELECT festival_id,start_date,end_date FROM festival")
    festival_list=cur.fetchall()

    cur.execute("SELECT performer_id FROM performer")
    performer_id_list = [row[0] for row in cur.fetchall()]

    performer_schedule={performer_id:[] for performer_id in performer_id_list}

    for (fes_id,fes_start,fes_end) in festival_list:
        
        random.shuffle(performer_id_list)

        for perf_id in performer_id_list:

            conflict=False

            if(performer_schedule[perf_id]):
                for (start_date,end_date) in performer_schedule[perf_id]:

                    if helper.is_there_overlap(fes_start,fes_end,start_date,end_date):
                        conflict=True
                        break
                        
            if(conflict==False):
                performer_schedule[perf_id].append((fes_start,fes_end))
                batch_insert.append((fes_id,perf_id))               



    cur.executemany("INSERT INTO public.festival_performer (festival_id,performer_id) VALUES (%s,%s) ON CONFLICT (festival_id,performer_id) DO NOTHING",batch_insert)
