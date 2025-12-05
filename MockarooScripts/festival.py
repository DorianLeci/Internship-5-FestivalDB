import auto_directory
import json
import random

def festival_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM festival")

    if(cur.fetchone()[0]==0):

        with open(auto_directory.csv_data_path("festival.json"), "r") as f:
            festival_data = json.load(f)

        cur.execute("SELECT city_id FROM city")
        city_id=[row[0] for row in cur.fetchall()]

        for f in festival_data:
            f["city_id"]=random.choice(city_id)
            cur.execute("INSERT INTO public.festival (festival_id,name,capacity,start_date,end_date,has_visitor_camp,city_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (f["festival_id"],f["name"],f["capacity"],f["start_date"],f["end_date"],f["has_visitor_camp"],f["city_id"]))
            