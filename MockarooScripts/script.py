import requests
import psycopg2
import random
from datetime import datetime, timedelta,time
from dotenv import load_dotenv
import os
import random_performers
import json
from faker import Faker

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR,".env"))


API_KEY=os.getenv("MOCKAROO_API_KEY")
print(API_KEY)

def Fetch(schema_id,count=1000):
    url=f"https://api.mockaroo.com/api/{schema_id}?count={count}&key={API_KEY}"
    response=requests.get(url)
    return response.json()

def get_data(cur,count=1000):   
    country_insert(cur)
    city_insert(cur)
    visitor_insert(cur)
    festival_insert(cur)
    band_insert(cur)
    performer_insert(cur)
    festival_performer_insert(cur)
    stage_insert(cur)
    performance_insert(cur)




def country_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM country")

    if(cur.fetchone()[0]==0):
        country_schema_id="8ca42db0"
        country=Fetch(country_schema_id)
        with open("/home/dorian/Downloads/country.json", "r") as f:
            country = json.load(f)
        for c in country:
            cur.execute("INSERT INTO public.country (country_id,name) VALUES (%s,%s)",(c["country_id"],c["name"]))       

def city_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM city")
    if(cur.fetchone()[0]==0):   
        city_schema_id="c27fc0b0"
        city_data=Fetch(city_schema_id)
        with open("/home/dorian/Downloads/city.json", "r") as f:
            city_data = json.load(f)
        cur.execute("SELECT country_id FROM country")

        country_id=[row[0] for row in cur.fetchall()]

        for city in city_data:
            city["country_id"]=random.choice(country_id)
            cur.execute(f"INSERT INTO public.city (city_id,name,postal_code,country_id) VALUES (%s,%s,%s,%s)",(city["city_id"],city["name"],city["postal_code"],city["country_id"]))


def visitor_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM visitor")
    if(cur.fetchone()[0]==0):   
        visitor_schema_id="b2b8bd60"
        visitor_data=Fetch(visitor_schema_id)
        with open("/home/dorian/Downloads/visitor.json", "r") as f:
            visitor_data = json.load(f)
        cur.execute("SELECT city_id FROM city")

        city_id=[row[0] for row in cur.fetchall()]

        for visitor in visitor_data:
            visitor["city_id"]=random.choice(city_id)
            cur.execute("INSERT INTO public.visitor (visitor_id,name,surname,email,birth_date,city_id) VALUES (%s,%s,%s,%s,%s,%s)",(visitor["visitor_id"],visitor["name"],
            visitor["surname"],visitor["email"],visitor["birth_date"],visitor["city_id"]))


def festival_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM festival")
    if(cur.fetchone()[0]==0):
        festival_schema_id="a8936230"
        festival_data=Fetch(festival_schema_id)

        with open("/home/dorian/Downloads/festival.json", "r") as f:
            festival_data = json.load(f)

        cur.execute("SELECT city_id FROM city")
        city_id=[row[0] for row in cur.fetchall()]

        for f in festival_data:
            f["city_id"]=random.choice(city_id)
            cur.execute("INSERT INTO public.festival (festival_id,name,capacity,start_date,end_date,has_visitor_camp,city_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (f["festival_id"],f["name"],f["capacity"],f["start_date"],f["end_date"],f["has_visitor_camp"],f["city_id"]))
            

import random
import json

def performer_insert(cur, count=1000):

    cur.execute("SELECT COUNT(*) FROM performer")
    if cur.fetchone()[0] == 0:

        cur.execute("SELECT band_id from band")
        band_id_list=[row[0] for row in cur.fetchall()]

        cur.execute("SELECT country_id FROM country")
        country_id_list = [row[0] for row in cur.fetchall()]

        member_name_schema_id="d0632080"
        member_name_data=Fetch(member_name_schema_id)
        with open("/home/dorian/Downloads/member_name.json", "r") as f:
            member_name_data = json.load(f)

        performer_schema_id = "d65d7d40"
        performer_data = Fetch(performer_schema_id)
        with open("/home/dorian/Downloads/performer.json", "r") as f:
            performer_data = json.load(f)


        for p in performer_data:
            performer_type=p["type"]
            country_id=random.choice(country_id_list)

            if(performer_type=="Solo"):
                name=random_performers.generate_random_names(random_performers.solo_performers)
                band_id=None

            elif(performer_type=="DJ"):
                name=random_performers.generate_random_names(random_performers.djs)
                band_id=None
            
            elif(performer_type=="Band_Member"):
                name=random.choice(member_name_data)["name"]
                band_id=random.choice(band_id_list)

            cur.execute("INSERT INTO public.performer (performer_id, name, genre, is_active,type,country_id,band_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (p["performer_id"],name,p["genre"],p["is_active"],performer_type,country_id,band_id))


                

def band_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM band")
    if(cur.fetchone()[0]==0):
        band_schema_id="49003cb0"
        band_data=Fetch(band_schema_id)
        with open("/home/dorian/Downloads/band.json", "r") as f:
            band_data = json.load(f)

        for band in band_data:
            cur.execute("INSERT INTO public.band (band_id,band_name) VALUES (%s,%s)",(band["band_id"],random_performers.generate_random_names(random_performers.bands)))


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

                    if is_there_overlap(fes_start,fes_end,start_date,end_date):
                        conflict=True
                        break
                        
            if(conflict==False):
                performer_schedule[perf_id].append((fes_start,fes_end))
                batch_insert.append((fes_id,perf_id))               



    cur.executemany("INSERT INTO public.festival_performer (festival_id,performer_id) VALUES (%s,%s) ON CONFLICT (festival_id,performer_id) DO NOTHING",batch_insert)

def stage_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM stage")

    if(cur.fetchone()[0]==0):
        stage_schema_id="8043ad60"
        stage_data=Fetch(stage_schema_id)
        with open("/home/dorian/Downloads/stage.json", "r") as f:
            stage_data = json.load(f)

        cur.execute("SELECT festival_id,capacity FROM festival")
        festival_info_list=cur.fetchall()

        for stage in stage_data:
            random.shuffle(festival_info_list)

            for fest_id,fest_capacity in festival_info_list:
                if check_stage_capacity(stage["capacity"],fest_capacity):
                    cur.execute("INSERT INTO stage (stage_id,name,capacity,is_covered,location,festival_id) VALUES (%s,%s,%s,%s,%s,%s)",
                                (stage["stage_id"],stage["name"],stage["capacity"],stage["is_covered"],stage["location"],fest_id))
                    break
            


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
            start_time,end_time=make_random_period(period_date_time_lower,period_date_time_upper)

            overlap=any(is_there_overlap(period_date_time_lower,period_date_time_upper,s,e) for s,e in performer_schedule[performer_id])
                
            if overlap:
                continue

            random.shuffle(stage_id_list)
                
            for stage_id in stage_id_list:
                overlap=any(is_there_overlap(start_time,end_time,s,e)for s,e in stage_schedule[stage_id])

                if overlap:
                    continue
                    
                    
                batch_insert.append((f"[{start_time.replace(microsecond=0)},{end_time.replace(microsecond=0)}]",stage_id,fp_id))
                stage_schedule[stage_id].append((start_time.replace, end_time))
                performer_schedule[performer_id].append((start_time, end_time))
                break
        
        cur.executemany("INSERT INTO public.performance (performance_period,stage_id,festival_performer_id) VALUES (%s,%s,%s)",batch_insert)

def make_random_period(start,end,min_duration=60,max_duration=240):
    fake=Faker()

    start_time=fake.date_time_between_dates(datetime_start=start,datetime_end=end-timedelta(minutes=max_duration))

    duration_minutes=fake.random_int(min=min_duration,max=max_duration)
    end_time=start_time+timedelta(minutes=duration_minutes)
    
    return start_time,end_time



 

def check_stage_capacity(stage_capacity,festival_capacity):
    return stage_capacity<=festival_capacity

def is_there_overlap(start1,end1,start2,end2):
    return start1 <= end2 and start2 <= end1

conn=psycopg2.connect(host="localhost",dbname="Internship-Festival-DB2",user="postgres",password="postgres")
cur=conn.cursor()

get_data(cur)
conn.commit()

cur.close()
conn.close()



