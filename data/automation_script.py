from public_data import controller
from apscheduler.schedulers.blocking import BlockingScheduler


def run(con):
    scheduler = BlockingScheduler()
    movie_ids = con.loader.get_movie_id_list()

    # cron for movie data
    # scheduler.add_job(con.update_movie_data, args=[1500000, 2000000, movie_ids])
    # scheduler.add_job(con.update_movie_data, args=[2000000, 4000000, movie_ids])
    # scheduler.add_job(con.update_movie_data, args=[4000000, 6000000, movie_ids])
    # scheduler.add_job(con.update_movie_data, args=[6000000, 8000000, movie_ids])

    # cron for movie rating
    # movie_ids_without_rating = con.loader.get_movie_id_list_without_rating()
    # total_length = len(movie_ids_without_rating)
    # split = int(total_length / 4)
    # scheduler.add_job(con.update_movie_rating, args=[movie_ids_without_rating[:split]])
    # scheduler.add_job(con.update_movie_rating, args=[movie_ids_without_rating[split:split * 2]])
    # scheduler.add_job(con.update_movie_rating, args=[movie_ids_without_rating[split * 2:split * 3]])
    # scheduler.add_job(con.update_movie_rating, args=[movie_ids_without_rating[split * 3:]])

    # cron for cinema rating, run at 0:00 everyday
    scheduler.add_job(con.update_cinema_schedule)
    scheduler.start()

if __name__ == '__main__':
    con = controller.ETLController()
    con.update_cinema_schedule()


