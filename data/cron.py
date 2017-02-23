import etl.etlprocessor as processor


if __name__ == '__main__':
    processor = processor.ETLProcessor()
    processor.update_cinema_list()
