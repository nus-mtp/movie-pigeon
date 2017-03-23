from public_data import controller
from apscheduler.schedulers.blocking import BlockingScheduler


def run(connection):
    scheduler = BlockingScheduler()

    # cron for cinema rating, run at 0:00 everyday
    scheduler.add_job(connection.update_cinema_schedule, trigger='cron', hour=0, minute=0, second=0)
    scheduler.start()

if __name__ == '__main__':
    con = controller.ETLController()
    con.update_cinema_schedule()
