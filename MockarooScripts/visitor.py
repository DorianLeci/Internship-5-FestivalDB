import auto_directory
import json
import random

def visitor_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM visitor")

    if(cur.fetchone()[0]==0):   

        with open(auto_directory.csv_data_path("visitor.json"), "r") as f:
            visitor_data = json.load(f)
        cur.execute("SELECT city_id FROM city")

        city_id=[row[0] for row in cur.fetchall()]

        for visitor in visitor_data:
            visitor["city_id"]=random.choice(city_id)
            cur.execute("INSERT INTO public.visitor (visitor_id,name,surname,email,birth_date,city_id) VALUES (%s,%s,%s,%s,%s,%s)",(visitor["visitor_id"],visitor["name"],
            visitor["surname"],visitor["email"],visitor["birth_date"],visitor["city_id"]))