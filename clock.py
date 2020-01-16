from apscheduler.schedulers.blocking import BlockingScheduler
import random
import re
import urllib.request

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour='6-23', minute='*/20')
def scheduled_job():
    url = "https://ann-chang-dinnereat.herokuapp.com/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

sched.start()
