import json
import auto_directory
import random
from helper import check_stage_capacity


def stage_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM stage")

    if(cur.fetchone()[0]==0):

        with open(auto_directory.csv_data_path("stage.json"),"r") as f:
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