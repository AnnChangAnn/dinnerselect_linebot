from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour='0-16', minute='*/20')
def scheduled_job():
    url = "https://line-bot-python-flask-ifw0.onrender.com"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

sched.start()
