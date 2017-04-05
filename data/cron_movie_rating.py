from public_data import controller
from apscheduler.schedulers.blocking import BlockingScheduler


def run(con):
    scheduler = BlockingScheduler()

    # cron for movie rating
    movie_ids_without_rating = con.loader.get_movie_id_list_without_rating()
    scheduler.add_job(con.update_movie_rating, args=[movie_ids_without_rating])

    scheduler.start()

if __name__ == '__main__':
    con = controller.ETLController()
    run(con)
