import requests
import psycopg2
import random
from datetime import datetime
from dotenv import load_dotenv
import os

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR,".env"))


API_KEY=os.getenv("MOCKAROO_API_KEY")
print(API_KEY)

def Fetch(schema_id,count=1000):
    url=f"https://api.mockaroo.com/api/{schema_id}?count={count}&key={API_KEY}"
    response=requests.get(url)
    return response.json()

def GetData(cur,count=1000):   
    CountryInsert(cur)
    CityInsert(cur)
    VisitorInsert(cur)
    FestivalInsert(cur)





def CountryInsert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM country")
    if(cur.fetchone()[0]==0):
        country_schema_id="8ca42db0"
        country=Fetch(country_schema_id)

        for c in country:
            cur.execute("INSERT INTO public.country (country_id,name) VALUES (%s,%s)",(c["country_id"],c["name"]))       

def CityInsert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM city")
    if(cur.fetchone()[0]==0):   
        city_schema_id="c27fc0b0"
        cityData=Fetch(city_schema_id)

        cur.execute("SELECT country_id FROM country")

        country_id=[row[0] for row in cur.fetchall()]

        for city in cityData:
            city["country_id"]=random.choice(country_id)
            cur.execute(f"INSERT INTO public.city (city_id,name,postal_code,country_id) VALUES (%s,%s,%s,%s)",(city["city_id"],city["name"],city["postal_code"],city["country_id"]))


def VisitorInsert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM visitor")
    if(cur.fetchone()[0]==0):   
        visitor_schema_id="b2b8bd60"
        visitorData=Fetch(visitor_schema_id)

        cur.execute("SELECT city_id FROM city")

        city_id=[row[0] for row in cur.fetchall()]

        for visitor in visitorData:
            visitor["city_id"]=random.choice(city_id)
            cur.execute("INSERT INTO public.visitor (visitor_id,name,surname,email,birth_date,city_id) VALUES (%s,%s,%s,%s,%s,%s)",(visitor["visitor_id"],visitor["name"],
            visitor["surname"],visitor["email"],visitor["birth_date"],visitor["city_id"]))


def FestivalInsert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM festival")
    if(cur.fetchone()[0]==0):
        festival_schema_id="a8936230"
        festivalData=Fetch(festival_schema_id)

        cur.execute("SELECT city_id FROM city")
        city_id=[row[0] for row in cur.fetchall()]

        for f in festivalData:
            f["city_id"]=random.choice(city_id)
            cur.execute("INSERT INTO public.festival (festival_id,name,capacity,start_date,end_date,has_visitor_camp,city_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (f["festival_id"],f["name"],f["capacity"],f["start_date"],f["end_date"],f["has_visitor_camp"],f["city_id"]))

conn=psycopg2.connect(host="localhost",dbname="Internship-5-FestivalDB",user="postgres",password="postgres")
cur=conn.cursor()

GetData(cur)
conn.commit()

cur.close()
conn.close()



