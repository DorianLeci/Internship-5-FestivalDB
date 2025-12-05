
import auto_directory
import json
import random_performers

def band_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM band")

    if(cur.fetchone()[0]==0):

        with open(auto_directory.csv_data_path("band.json"), "r") as f:
            band_data = json.load(f)

        for band in band_data:
            cur.execute("INSERT INTO public.band (band_id,band_name) VALUES (%s,%s)",(
                band["band_id"],random_performers.generate_random_names(random_performers.bands)))

