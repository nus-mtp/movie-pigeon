import etl.etlprocessor as processor
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    processor = processor.ETLProcessor()
    scheduler.add_job(processor.update_movie_data, args=[1, 1000000, 0])
    scheduler.add_job(processor.update_movie_data, args=[1000000, 2000000, 5])
    scheduler.add_job(processor.update_movie_data, args=[2000000, 3000000, 10])
    scheduler.add_job(processor.update_movie_data, args=[3000000, 4000000, 15])
    # scheduler.add_job(processor.update_movie_data, args=[4000000, 5000000, 20])
    # scheduler.add_job(processor.update_movie_data, args=[5000000, 6000000, 25])
    # scheduler.add_job(processor.update_movie_data, args=[6000000, 7000000, 30])
    scheduler.start()
