from pyspark import SparkContext, SparkConf
from datetime import date
import pickle

if __name__ == "__main__":

	# setup spark
	conf = SparkConf()
	#conf.setMaster('yarn-client')
	conf.setMaster('local[4]')
	conf.setAppName('app1') 
	sc = SparkContext(conf=conf)
	sc.setLogLevel("ERROR")

	# load data into rdd
	rdd = sc.textFile('hdfs:///data/scihub')

	print('hello spark')
	print(rdd.first())

