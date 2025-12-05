from faker import Faker
from datetime import timedelta

def check_stage_capacity(stage_capacity,festival_capacity):
    return stage_capacity<=festival_capacity

def is_there_overlap(start1,end1,start2,end2):
    return start1 <= end2 and start2 <=end1

def is_there_overlap_performance(start1,end1,start2,end2):
    return start1 < end2 and start2 <end1

def make_random_period(start,end,min_duration=60,max_duration=240):
    fake=Faker()

    start_time=fake.date_time_between_dates(datetime_start=start,datetime_end=end-timedelta(minutes=max_duration))

    duration_minutes=fake.random_int(min=min_duration,max=max_duration)
    end_time=start_time+timedelta(minutes=duration_minutes)
    
    return start_time,end_time

def generate_purchase_time(fest_start,fest_end):
    fake=Faker()

    return fake.date_time_between_dates(datetime_start=fest_start,datetime_end=fest_end).replace(second=0,microsecond=0)

