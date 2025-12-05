
import random
import json
import auto_directory

def ticket_type_insert(cur):
    cur.execute("SELECT COUNT(*) FROM ticket_type")

    if cur.fetchone()[0] == 0:

        DESCRIPTION_JEDNODNEVNA = "Ulaznica vrijedi za jedan odabrani dan festivala i omogućuje pristup svim pozornicama tijekom tog dana."

        DESCRIPTION_FESTIVALSKA ="Ulaznica vrijedi za cijelo trajanje festivala i uključuje neograničen pristup svim pozornicama i programima."

        DESCRIPTION_VIP ="VIP ulaznica uključuje prioritetni ulaz, pristup VIP zoni, posebne sadržaje i ekskluzivne pogodnosti tijekom cijelog festivala."

        DESCRIPTION_KAMP="Ulaznica omogućuje pristup kamp zoni festivala tijekom cijelog trajanja događaja."

        DESCRIPTION_PROMO = "Ograničena promotivna ulaznica s popustom. Vrijedi za jedan ulaz u festivalski prostor na dan po izboru."

        insert_many = [
            (1, "jednodnevna", DESCRIPTION_JEDNODNEVNA),
            (2, "festivalska", DESCRIPTION_FESTIVALSKA),
            (3, "VIP",          DESCRIPTION_VIP),
            (4, "kamp",         DESCRIPTION_KAMP),
            (5, "promo",        DESCRIPTION_PROMO),
        ]

        cur.executemany(
            "INSERT INTO public.ticket_type (ticket_type_id, ticket_type, description) VALUES (%s, %s, %s)",
            insert_many
        )



        
def ticket_insert(cur,count=1000):

    ticket_type_insert(cur)

    cur.execute("SELECT COUNT(*) FROM ticket")

    if(cur.fetchone()[0]==0):
       
        cur.execute("SELECT ticket_type_id FROM ticket_type")
        ticket_type_id_list=cur.fetchall()

        cur.execute("SELECT festival_id FROM festival")
        festival_id_list=cur.fetchall()

        with open(auto_directory.csv_data_path("ticket.json"), "r") as f:
            ticket_data = json.load(f)

        for t in ticket_data:
            cur.execute("INSERT INTO public.ticket (ticket_id,ticket_type_id,festival_id) VALUES (%s,%s,%s)",
                        (t["ticket_id"],random.choice(ticket_type_id_list),random.choice(festival_id_list)))
 