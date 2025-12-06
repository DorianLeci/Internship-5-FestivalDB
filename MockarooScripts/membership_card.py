
import random
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta


def membership_card_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM membership_card")

    if(cur.fetchone()[0]==0):
        
        cur.execute("""SELECT o.visitor_id,MAX(o.time_of_purchase)
                    FROM order_item oi
                    JOIN ticket t on t.ticket_id=oi.ticket_id
                    JOIN orders o ON o.order_id=oi.order_id
                    GROUP BY o.visitor_id
                    HAVING SUM(oi.price*oi.quantity)>=600 AND
                    COUNT(DISTINCT t.festival_id)>3
					""")
        
        eligible_visitors=cur.fetchall()

        if(eligible_visitors):

            for visitor_id,last_purchase in eligible_visitors:
                if(last_purchase>datetime.now() - timedelta(days=6*10)):
                    status="istekla"
                    activation_date=None
                
                else:
                    status="Aktivna"
                    activation_date=last_purchase
                            
                cur.execute("INSERT INTO public.membership_card (date_of_activation,status,visitor_id) VALUES(%s,%s,%s)",
                                (activation_date,status,visitor_id))