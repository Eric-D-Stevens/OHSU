from pyspark import SparkContext, SparkConf
from operator import add
import re
from collections import Counter
import pickle

if __name__ == "__main__":

	# setup spark
	#conf.setMaster('local[4]')
	conf = SparkConf()
	conf.setMaster('yarn-client')
	conf.setAppName('estevens_q2') 
	sc = SparkContext(conf=conf)
	sc.setLogLevel("ERROR")

	# mapping funciton
	def get_doi_only(line):
		fail = line
		try:
			line = line.split('\t')[1] # only look at first column
		except:
			print(fail)
			line = False # for filtering later
		return line
	 
	# load data into rdd
	#rdd = sc.textFile('hdfs:///data/scihub/nov2015.tab.bz2')
	rdd = sc.textFile('hdfs:///data/scihub')

	# get doi string
	rdd = rdd.map(get_doi_only)

	print('hello spark')
	print(rdd.first())
	print(type(rdd.first()))

	print('COUNTING >>>>')
	count_dict = rdd.countByValue()
	print('COUNTED>>>>')
	print('SORTING >>>>')
	counter = Counter(count_dict)
	most_common = counter.most_common(10)
	print(most_common)
		
	

	with open('downloads_per_doi.pkl', 'w') as f:
		pickle.dump(most_common, f)
