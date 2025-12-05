
import random
import helper
from datetime import datetime,time
from psycopg2.extras import DateTimeRange

def performance_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM performance")

    if(cur.fetchone()[0]==0):

        batch_insert=[]

        cur.execute("SELECT *FROM festival_performer")
        festival_performer_list=cur.fetchall()

        cur.execute("SELECT stage_id FROM stage")
        stage_id_list=cur.fetchall()

        cur.execute("SELECT performer_id FROM performer")
        performer_id_list = [row[0] for row in cur.fetchall()]

        performer_schedule={performer_id:[] for performer_id in performer_id_list}
        stage_schedule={stage_id:[] for stage_id in stage_id_list}
    
        random.shuffle(festival_performer_list)

        for fp_id,performer_id,festival_id,fest_period in festival_performer_list:
                
            period_date_time_lower=datetime.combine(fest_period.lower, time.min)
            period_date_time_upper=datetime.combine(fest_period.upper, time.max)
            start_time,end_time=helper.make_random_period(period_date_time_lower,period_date_time_upper)

            overlap=any(helper.is_there_overlap(period_date_time_lower,period_date_time_upper,s,e) for s,e in performer_schedule[performer_id])
                
            if overlap:
                continue

            random.shuffle(stage_id_list)
                
            for stage_id in stage_id_list:
                overlap=any(helper.is_there_overlap(start_time,end_time,s,e)for s,e in stage_schedule[stage_id])

                if overlap:
                    continue
                    
                interval = DateTimeRange(start_time.replace(second=0, microsecond=0),end_time.replace(second=0, microsecond=0),bounds='[]')    
                batch_insert.append((interval,stage_id,fp_id))
                stage_schedule[stage_id].append((start_time, end_time))
                performer_schedule[performer_id].append((start_time, end_time))
                break
        
        cur.executemany("INSERT INTO public.performance (performance_period,stage_id,festival_performer_id) VALUES (%s,%s,%s)",batch_insert)