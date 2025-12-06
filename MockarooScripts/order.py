import auto_directory
import json
import random
import helper
from datetime import date

def order_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM orders")

    if(cur.fetchone()[0]==0):
        
        cur.execute("SELECT visitor_id from visitor")
        visitor_id_list=cur.fetchall()

        
        with open(auto_directory.csv_data_path("order.json"), "r") as f:
            order_data = json.load(f)


        for order in order_data:

            cur.execute("SELECT ticket_id from ticket")
            ticket_id_list=cur.fetchall()

            ticket_id=random.choice(ticket_id_list)
            visitor_id=random.choice(visitor_id_list)

            fest_start,fest_end=get_festival_period(cur,ticket_id)
            purchase_time=helper.generate_purchase_time(fest_start,fest_end)

            if(purchase_time.date()>date.today()):
                purchase_time=date.today()

            cur.execute("INSERT INTO public.orders (order_id,time_of_purchase,visitor_id) VALUES (%s,%s,%s)",
                        (order["order_id"],purchase_time,visitor_id))
            
            cur.execute("""SELECT ticket_id FROM ticket WHERE festival_id=
                        (SELECT festival_id FROM ticket where ticket_id= %s )""",(ticket_id))
            
            tickets_for_order=cur.fetchall()
            
            num_items=random.randint(1,20)
            for _ in range(num_items):
                price=round(random.uniform(10,200),2)
                quantity=random.randint(1,5)

                ticket_for_item=random.choice(tickets_for_order)

                cur.execute("INSERT INTO order_item (price,quantity,order_id,ticket_id) VALUES (%s,%s,%s,%s)",
                            (price,quantity,order["order_id"],ticket_for_item))

            


def get_festival_period(cur,ticket_id):
    
    cur.execute("""SELECT f.start_date,f.end_date FROM festival f
                JOIN ticket t on t.festival_id=f.festival_id
                WHERE ticket_id= %s""",(ticket_id))
    
    return cur.fetchone()