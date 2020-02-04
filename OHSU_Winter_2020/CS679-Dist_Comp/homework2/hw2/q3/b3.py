from pyspark import SparkContext, SparkConf
from operator import add
import re
from collections import Counter
import pickle

if __name__ == "__main__":

	# setup spark
	conf = SparkConf()
	#conf.setMaster('yarn-client')
	conf.setMaster('local[2]')
	conf.setAppName('estevens_b3') 
	sc = SparkContext(conf=conf)
	sc.setLogLevel("ERROR")

	# mapping funciton
	def filter_top_10(line):
		try:
			pub_id = re.search('\d+\.\d+',line).group(0)
			if pub_id in broad.keys():
				print("REMATCH:",pub_id)
				return True
			else:
				return False	
		except:
			return False


	def map_count_top_10(line):
		pub_id = re.search('\d+\.\d+', line).group(0)
		return '{},{}'.format(broad[pub_id], line)		

	# unpickle
	with open('/cslu/homes/stevener/hw2/q3/publisher_count.pkl') as f:
		pcnt = pickle.load(f)

	# convert to dict
	p_cnt_dict = {}
	for i in pcnt:
		p_cnt_dict[i[0]] = i[1]

	# broadcast the dict
	broad = sc.broadcast(p_cnt_dict).value

	rdd = sc.textFile("file:///l2/corpora/scihub/publisher_DOI_prefixes.csv")
	print('hello spark')
	print(rdd.take(3))

	print('FILTER >>>>')
	rdd = rdd.filter(filter_top_10)
	print('FILTERED >>>>')

	print('MAP >>>>')
	rdd = rdd.map(map_count_top_10)
	print('MAPPED >>>>')
	
	
	print('WRITE, >>>>')
	#rdd.saveAsTextFile("/cslu/homes/stevener/hw2/q3/output_count.csv")	
	with open('count_output.csv', 'w') as f:
		for i in rdd.collect(): 
			f.write('{}\n'.format(i))
