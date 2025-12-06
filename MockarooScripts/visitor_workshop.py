import random
import helper
from datetime import datetime,time,timedelta

def visitor_workshop_insert(cur,count=1000):

    cur.execute("SELECT COUNT(*) FROM visitor_workshop")

    if(cur.fetchone()[0]==0):
        batch_insert=[]

        cur.execute("SELECT workshop_id,start_time,duration,festival_id,capacity FROM workshop")
        workshop_list=cur.fetchall()

        cur.execute("SELECT visitor_id FROM visitor")
        visitor_id_list = [row[0] for row in cur.fetchall()]

        visitor_schedule={visitor_id:[] for visitor_id in visitor_id_list}

        enrollment_counter={}
        capacity_counter={}

        visitor_festivals_dict=get_visitor_festivals(cur)


        for visitor_id in visitor_id_list:
            
            visitor_festivals=visitor_festivals_dict.get(visitor_id,[])
            
            availible_workshops=[w for w in workshop_list if w[3] in visitor_festivals]

            num_workshops=random.randint(1,5)

            for _,start_time,duration,_,_ in availible_workshops:

                availible_workshops_filtered = [ w for w in availible_workshops if not any(helper.is_there_overlap(w[1], w[1]+w[2], s, e) 
                                                                                           for s, e in visitor_schedule[visitor_id])]

                if(not availible_workshops_filtered):
                    continue

                chosen_workshop=random.choice(availible_workshops_filtered)
                set_default(enrollment_counter,capacity_counter,chosen_workshop)

                if(not can_enroll(cur,enrollment_counter[chosen_workshop[0]],capacity_counter[chosen_workshop[4]])):
                    continue
                
                enrollment_time=start_time-timedelta(days=random.randint(1,5))
                status=get_status(datetime.now(),chosen_workshop[1],chosen_workshop[1]+chosen_workshop[2])

                if(status=="prijavljen" or status=="ceka_na_potvrdu"):

                    enrollment_counter[chosen_workshop[0]]+=1

                batch_insert.append((chosen_workshop[0],visitor_id,enrollment_time,status))


        cur.executemany("INSERT INTO public.visitor_workshop (workshop_id,visitor_id,enrollment_time,status) VALUES (%s,%s,%s,%s) " \
        "ON CONFLICT (visitor_id, workshop_id) DO NOTHING;",batch_insert)

def get_visitor_festivals(cur):

    cur.execute("""SELECT o.visitor_id,t.festival_id
                FROM orders o
                JOIN order_item i ON i.order_id=o.order_id
                JOIN ticket t ON t.ticket_id=i.ticket_id""")
    
    visitor_festival_dict={}

    list=cur.fetchall()

    for visitor_id,festival_id in list:
        visitor_festival_dict.setdefault(visitor_id, []).append(festival_id)

    return visitor_festival_dict

def get_status(now,start,end):

    if now<start and random.random()<0.1:
        return "otkazao"
    
    if now<start:
        return "prijavljen" if random.random()<0.7 else "ceka_na_potvrdu"
    
    if now>=end:
        return "prisustvovao"
    
    if start <= now < end:
        return "prijavljen"
    

def can_enroll(cur,enrollment_counter,capacity):

    return enrollment_counter<capacity

def set_default(enrollment_counter,capacity_counter,chosen_workshop):

    enrollment_counter.setdefault(chosen_workshop[0],0)
    capacity_counter.setdefault(chosen_workshop[4],0)