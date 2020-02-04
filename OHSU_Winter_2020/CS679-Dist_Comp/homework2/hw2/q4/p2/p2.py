from pyspark import SparkContext, SparkConf
from operator import add
import re
from collections import Counter
import pickle
from heapq import nlargest


if __name__ == "__main__":

	# setup spark
	conf = SparkConf()
	conf.setMaster('yarn-client')
	conf.setAppName('estevens_q3') 
	sc = SparkContext(conf=conf)
	sc.setLogLevel("ERROR")

	# mapping funciton
	def get_cities(line):
		fail = line
		try:
			line = line.split('\t')[4] # only look at first column
		except:
			line = 'bad' # for filtering later
		return line
	 
	def get_pop():
		pop = {}
		with open('largest-us-cities.csv') as f:
			line = f.readline()
			line = f.readline()
			while line:
				row = line.split(';')
				pop[row[0]] = float(row[4].strip())
				line = f.readline() 
		return pop

	def rel_map(line):
		try:
			val = (line[0], line[1]/broad[line[0]])
		except:
			val = (line[0],0) 
		return val

	# load data into rdd
	rdd = sc.textFile('hdfs:///data/scihub/nov2015.tab.bz2')
	#rdd = sc.textFile('hdfs:///data/scihub')


	print('hello spark')
	print(rdd.first())
	print(type(rdd.first()))

	print('FILTERING >>>>')
	rdd = rdd.filter(lambda line: re.search('United States', line))
	print('FILTERED >>>>')
	print(rdd.first())

	print('MAPPING >>>>')
	rdd = rdd.map(get_cities)
	print('MAPPED>>>>')


	print('COUNTING >>>>')
	count_dict = rdd.countByValue()
	print('COUNTED>>>>')
	

	print('SORTING >>>>')
	counter = Counter(count_dict)
	most_common = counter.most_common(20)
	print('SORTED >>>>')
	print(most_common)
	
	
	print('SAVING RAW COUNT >>>>')
	for i in most_common: print(i)
	with open('city_cnt.pkl', 'w') as f:
		pickle.dump(most_common, f)
	print('SAVED >>>>')


	print('GET REL CNT>>>>')
	print(rdd.first())
	rdd = sc.parallelize(count_dict.items())
	print(rdd.first())
	broad = sc.broadcast(get_pop()).value
	print('BRD:', type(broad))
	rdd = rdd.map(rel_map)
	rel_cnt = rdd.collect()
	rel_largest = nlargest(20, rel_cnt, key=lambda x: x[1])
	
	print('SAVING RAW COUNT >>>>')
	for i in rel_largest: print(i)
	with open('city_pop_rel.pkl', 'w') as f:
		pickle.dump(rel_largest, f)
	print('SAVED >>>>')
	
	
