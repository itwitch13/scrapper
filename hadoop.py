import os


class Hadoop:
    def __init__(self):
        self.hadoop_path = '~/input'
        self.filename = 'flat_info.csv'

    def hadoop_mkdir(self):
        os.system(f"hadoop fs -mkdir -p {self.hadoop_path}")

    def add_file_to_hdfs(self, date):
        self.filename = 'flat_info_{}.csv'.format(date)
        os.system(f"hadoop fs -put ./{self.filename} {self.hadoop_path}")
