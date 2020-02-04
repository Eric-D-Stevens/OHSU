from pyspark import SparkContext, SparkConf
from operator import add
import re
from collections import Counter
import pickle
from heapq import nlargest


if __name__ == "__main__":

	# filter oregon
	def get_oregon(line):
		cord = line.split('\t')[5].split(',')
		if float(cord[1]) < -100:
			return True
		return False

	# filter maine
	def get_maine(line):
		cord = line.split('\t')[5].split(',')
		if float(cord[1]) > -100:
			return True
		return False
	
	def get_paper(line):
		try:
			doi = line.split('\t')[1]
			return doi
		except:
			return 'bad'

	# setup spark
	conf = SparkConf()
	conf.setMaster('yarn-client')
	conf.setAppName('estevens_q3') 
	sc = SparkContext(conf=conf)
	sc.setLogLevel("ERROR")


	# load data into rdd
	#rdd = sc.textFile('hdfs:///data/scihub/nov2015.tab.bz2')
	rdd = sc.textFile('hdfs:///data/scihub')

	print('hello spark')
	print(rdd.first())
	print(type(rdd.first()))

	print('FILTERING portland >>>>')
	rdd = rdd.filter(lambda line: \
			re.search('United States', line) and \
			re.search('Portland', line))
	print('FILTERED >>>>')

	print('FILTERING city >>>>')
	maine = rdd.filter(get_maine)
	oregon = rdd.filter(get_oregon)
	print('FILTERED >>>>')


	print('OREGON:',oregon.first())
	print('MAINE:',maine.first())

	print('MAPPING >>>>')
	rdd = rdd.map(get_oregon)
	print('MAPPED>>>>')


	print('COUNTING >>>>')
	oregon_d = oregon.countByValue()
	maine_d = maine.countByValue()
	print('COUNTED>>>>')
	

	print('SORTING >>>>')
	oregon_cnt = Counter(oregon_d)
	maine_cnt = Counter(maine_d)
	print('SORTED >>>>')
	
	print('OREGON:')
	oregon_most_common = oregon_cnt.most_common(10)
	for o in oregon_most_common: print(o)
	print('MAINE:')
	maine_most_common = maine_cnt.most_common(10)
	for m in maine_most_common: print(m)
	
	print('SAVING >>>>')
	with open('oregon_top.pkl', 'w') as f:
		pickle.dump(oregon_most_common, f)
	with open('maine_top.pkl', 'w') as f:
		pickle.dump(maine_most_common, f)
	print('SAVED >>>>')

