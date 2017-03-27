from public_data import controller
from apscheduler.schedulers.blocking import BlockingScheduler


def run(con):
    scheduler = BlockingScheduler()
    movie_ids = con.loader.get_movie_id_list()

    # cron for movie data
    scheduler.add_job(con.update_movie_data, args=[1, 2000000, movie_ids])
    scheduler.add_job(con.update_movie_data, args=[2000000, 4000000, movie_ids])
    scheduler.add_job(con.update_movie_data, args=[4000000, 6000000, movie_ids])
    scheduler.add_job(con.update_movie_data, args=[6000000, 8000000, movie_ids])

    scheduler.start()

if __name__ == '__main__':
    con = controller.ETLController()
    run(con)
