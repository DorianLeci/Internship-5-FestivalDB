import auto_directory
import json
import random

def city_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM city")

    if(cur.fetchone()[0]==0):   

        with open(auto_directory.csv_data_path("city.json"), "r") as f:
            city_data = json.load(f)

        cur.execute("SELECT country_id FROM country")

        country_id=[row[0] for row in cur.fetchall()]

        for city in city_data:

            city["country_id"]=random.choice(country_id)
            cur.execute(f"INSERT INTO public.city (city_id,name,postal_code,country_id) VALUES (%s,%s,%s,%s)",(city["city_id"],city["name"],city["postal_code"],city["country_id"]))