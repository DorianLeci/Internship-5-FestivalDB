
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta


def membership_card_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM membership_card")

    if(cur.fetchone()[0]==0):
        
        cur.execute("""SELECT o.visitor_id
                    FROM order_item oi
                    JOIN ticket t on t.ticket_id=oi.ticket_id
                    JOIN orders o ON o.order_id=oi.order_id
                    GROUP BY o.visitor_id
                    HAVING SUM(oi.price*oi.quantity)>=600 AND
                    COUNT(DISTINCT t.festival_id)>3
					""")
        
        cur.execute()
        eligible_users=cur.fecthall()

        batch_insert=[(user,datetime.now()) for user in eligible_users]
                     
        cur.executemany("INSERT INTO ")