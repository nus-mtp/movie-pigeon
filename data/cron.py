import etl.etlprocessor as processor
import time
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    processor = processor.ETLProcessor()
    scheduler.add_job(processor.update_movie_data, args=[1, 1000000])
    scheduler.add_job(processor.update_movie_data, args=[1000000, 2000000])
    scheduler.start()
