import auto_directory
import json

def country_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM country")

    if(cur.fetchone()[0]==0):
        with open(auto_directory.csv_data_path("country.json"), "r") as f:
            country = json.load(f)
        for c in country:
            cur.execute("INSERT INTO public.country (country_id,name) VALUES (%s,%s)",(c["country_id"],c["name"]))       