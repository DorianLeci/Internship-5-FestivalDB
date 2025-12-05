import auto_directory
import json
import random_performers
import random

def performer_insert(cur, count=1000):

    cur.execute("SELECT COUNT(*) FROM performer")
    if cur.fetchone()[0] == 0:

        cur.execute("SELECT band_id from band")
        band_id_list=[row[0] for row in cur.fetchall()]

        cur.execute("SELECT country_id FROM country")
        country_id_list = [row[0] for row in cur.fetchall()]

        with open(auto_directory.csv_data_path("member_name.json"), "r") as f:
            member_name_data = json.load(f)

        with open(auto_directory.csv_data_path("performer.json"), "r") as f:
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