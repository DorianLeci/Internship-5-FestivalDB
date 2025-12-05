
import psycopg2

import country
import city
import festival
import visitor
import band
import performer
import festival_performer
import stage
import performance
import ticket
import order
import staff
import festival_staff
import workshop

def get_data(cur,count=1000):   
    country.country_insert(cur)
    city.city_insert(cur)
    visitor.visitor_insert(cur)
    festival.festival_insert(cur)
    band.band_insert(cur)
    performer.performer_insert(cur)
    festival_performer.festival_performer_insert(cur)
    stage.stage_insert(cur)
    performance.performance_insert(cur)
    ticket.ticket_insert(cur)
    order.order_insert(cur)
    staff.staff_insert(cur)
    festival_staff.festival_staff_insert(cur)
    workshop.workshop_insert(cur)


conn=psycopg2.connect(host="localhost",dbname="Internship-5-FestivalDB",user="postgres",password="postgres")
cur=conn.cursor()

get_data(cur)
conn.commit()

cur.close()
conn.close()



