import requests
import psycopg2
import random
from datetime import datetime
from dotenv import load_dotenv
import os
import random_performers
import json

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




def country_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM country")
    if(cur.fetchone()[0]==0):
        country_schema_id="8ca42db0"
        country=Fetch(country_schema_id)

        for c in country:
            cur.execute("INSERT INTO public.country (country_id,name) VALUES (%s,%s)",(c["country_id"],c["name"]))       

def city_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM city")
    if(cur.fetchone()[0]==0):   
        city_schema_id="c27fc0b0"
        city_data=Fetch(city_schema_id)

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

        cur.execute("SELECT city_id FROM city")
        city_id=[row[0] for row in cur.fetchall()]

        for f in festival_data:
            f["city_id"]=random.choice(city_id)
            cur.execute("INSERT INTO public.festival (festival_id,name,capacity,start_date,end_date,has_visitor_camp,city_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (f["festival_id"],f["name"],f["capacity"],f["start_date"],f["end_date"],f["has_visitor_camp"],f["city_id"]))
            
def performer_insert(cur,count=1000):

     cur.execute("SELECT COUNT(*) FROM performer")
     if(cur.fetchone()[0]==0):
        performer_schema_id="d65d7d40"
        performer_data=Fetch(performer_schema_id)

        with open("/home/dorian/Downloads/performer.json", "r") as f:
            performer_data = json.load(f)

        with open("/home/dorian/Downloads/member_name.json", "r") as f:
            band_members = json.load(f)

        cur.execute("SELECT country_id FROM country")
        country_id=[row[0] for row in cur.fetchall()]

        query_params="(performer_id,name,genre,is_active,country_id) VALUES (%s,%s,%s,%s,%s)"

        for p in performer_data:
            p["country_id"]=random.choice(country_id)
            performer_type=p["type"]
                     
            if(performer_type=="Solo"):
                insert_query=f"INSERT INTO public.solo_performer {query_params}"
                cur.execute(insert_query,(p["performer_id"],random_performers.generate_random_names(random_performers.solo_performers),p["genre"],p["is_active"],p["country_id"]))

                insert_query=f"INSERT INTO public.performer {query_params}"
                cur.execute(insert_query,(p["performer_id"],random_performers.generate_random_names(random_performers.solo_performers),p["genre"],p["is_active"],p["country_id"]))

            elif(performer_type=="DJ"):
                insert_query=f"INSERT INTO public.dj {query_params}"
                cur.execute(insert_query,(p["performer_id"],random_performers.generate_random_names(random_performers.djs),p["genre"],p["is_active"],p["country_id"]))

                insert_query=f"INSERT INTO public.performer {query_params}"
                cur.execute(insert_query,(p["performer_id"],random_performers.generate_random_names(random_performers.djs),p["genre"],p["is_active"],p["country_id"]))

            elif(performer_type=="Band_Member"): 
                query_params_band_member="(performer_id,name,genre,is_active,country_id,band_id) VALUES (%s,%s,%s,%s,%s,%s)"
                insert_query=f"INSERT INTO public.band_member {query_params_band_member}"

 
                member_name=random.choice(band_members)["name"]

                cur.execute("SELECT band_id FROM band")
                band_id_list=[row[0] for row in cur.fetchall()]

                cur.execute(insert_query,(p["performer_id"],member_name,
                                          p["genre"],p["is_active"],p["country_id"],random.choice(band_id_list)))
                
                insert_query=f"INSERT INTO public.performer {query_params}"
                cur.execute(insert_query,(p["performer_id"],member_name,p["genre"],p["is_active"],p["country_id"]))

                

def band_insert(cur,count=1000):
    with open("/home/dorian/Downloads/band.json", "r") as f:
        band_data = json.load(f)

    cur.execute("SELECT COUNT(*) FROM band")
    if(cur.fetchone()[0]==0):
        for band in band_data:
            cur.execute("INSERT INTO public.band (band_id,band_name) VALUES (%s,%s)",(band["band_id"],random_performers.generate_random_names(random_performers.bands)))


def festival_performer_insert(cur,count=1000):
    batch_insert=[]

    cur.execute("SELECT festival_id,start_date,end_date FROM festival")
    festival_list=cur.fetchall()

    cur.execute("SELECT performer_id FROM performer")
    performer_id_list = [row[0] for row in cur.fetchall()]

    for (fes_id,fes_start,fes_end) in festival_list:

        fest_performers=random.sample(performer_id_list,k=100)
        for perf_id in fest_performers:
            batch_insert.append((fes_id,perf_id))

    cur.executemany("INSERT INTO public.festival_performer (festival_id,performer_id) VALUES (%s,%s) ON CONFLICT (festival_id,performer_id) DO NOTHING",batch_insert)




conn=psycopg2.connect(host="localhost",dbname="Internship-5-FestivalDB",user="postgres",password="postgres")
cur=conn.cursor()

get_data(cur)
conn.commit()

cur.close()
conn.close()



