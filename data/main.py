import etl.etlprocessor as processor


if __name__ == '__main__':
    processor = processor.ETLProcessor()
    processor.retrieve_movie_data()
