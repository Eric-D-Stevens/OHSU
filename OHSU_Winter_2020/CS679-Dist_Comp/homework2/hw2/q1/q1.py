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

	# mapping funciton
	def get_day_only(line):
		fail = line
		try:
			line = line.split('\t')[0] # only look at first column
			line = line.split()[0] # remove time
			line = line.split('-') # split date yyyy mm dd
			date(int(line[0]), int(line[1]), int(line[2]))
			line = '-'.join(line)
		except:
			print(fail)
			line = False # for filtering later
		return line
	
	# load data into rdd
	rdd = sc.textFile('hdfs:///data/scihub')

	# get datetime object
	rdd = rdd.map(get_day_only)

	# filter out non dates
	rdd = rdd.filter(lambda l: bool(l) )

	print('hello spark')
	print(rdd.first())
	print(type(rdd.first()))

	print('COUNTING >>>>')
	rdd = rdd.countByValue()

	with open('downloads_per_day.pkl', 'w') as f:
		pickle.dump(rdd, f)
