from apscheduler.schedulers.background import BackgroundScheduler

from clients.appointment_scheduler.main import main


def start():
    scheduler = BackgroundScheduler(timezone='Europe/Kiev')
    scheduler.add_job(main, 'cron', hour='5', minute='50')
    scheduler.start()
