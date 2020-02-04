from pyspark import SparkContext, SparkConf
from operator import add
import re
from collections import Counter
import pickle

if __name__ == "__main__":

	# setup spark
	conf = SparkConf()
	conf.setMaster('yarn-client')
	conf.setAppName('estevens_q3') 
	sc = SparkContext(conf=conf)
	sc.setLogLevel("ERROR")

	# mapping funciton
	def get_doi_prefix(line):
		fail = line
		try:
			line = line.split('\t')[1] # only look at first column
			line = re.match('\d+\.\d+/',line).group(0)[:-1]
		except:
			print('fail')
			line = False # for filtering later
		return line
	 
	# load data into rdd
	#rdd = sc.textFile('hdfs:///data/scihub/nov2015.tab.bz2')
	rdd = sc.textFile('hdfs:///data/scihub')


	print('hello spark')
	print(rdd.first())
	print(type(rdd.first()))

	print('MAPPING >>>>')
	rdd = rdd.map(get_doi_prefix)
	print('MAPPED>>>>')


	print('COUNTING >>>>')
	count_dict = rdd.countByValue()
	#rdd = rdd.combineByKey(int, add, add)
	print('COUNTED>>>>')
	print('COUNTDICT TYPE', type(count_dict))

	print('SORTING >>>>')
	counter = Counter(count_dict)
	most_common = counter.most_common(10)
	print('SORTED >>>>')
	print(most_common)
	

	with open('publisher_count.pkl', 'w') as f:
		pickle.dump(most_common, f)
