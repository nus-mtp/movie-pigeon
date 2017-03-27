from public_data import controller
from apscheduler.schedulers.blocking import BlockingScheduler


def run(con):
    scheduler = BlockingScheduler()

    # cron for movie rating
    movie_ids_without_rating = con.loader.get_movie_id_list_without_rating()
    total_length = len(movie_ids_without_rating)
    split = int(total_length / 4)
    scheduler.add_job(con.update_movie_rating, args=[movie_ids_without_rating[:split]])
    scheduler.add_job(con.update_movie_rating, args=[movie_ids_without_rating[split:split * 2]])
    scheduler.add_job(con.update_movie_rating, args=[movie_ids_without_rating[split * 2:split * 3]])
    scheduler.add_job(con.update_movie_rating, args=[movie_ids_without_rating[split * 3:]])

    scheduler.start()

if __name__ == '__main__':
    con = controller.ETLController()
    run(con)
