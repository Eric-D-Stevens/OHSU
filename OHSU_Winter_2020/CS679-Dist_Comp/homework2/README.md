# Clusters: Homework 2
### Eric D. Stevens

## 1. Trends Over Time

<img src="https://raw.githubusercontent.com/Eric-D-Stevens/OHSU/master/OHSU_Winter_2020/CS679-Dist_Comp/homework2/images/over_time.PNG">

#### Data Collection

The code for this segment can be found in `hw2/q1/q1.py`. 

The process I used to gather this data was straight forward. First and RDD was generated directly from the Hadoop directory. A `rdd.map()` was used to split each line and only collect the dates, check to see that the date could be parsed, and then write the date as a string as the only output. A try clause was used to do this so that any bad columns would be filtered out by an `rdd.filter()` method following the map stage. The code for the mapper can be seen here:

```python
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
```

After passing the data through the map and the filter, what was left was a single column of dates. I then used the `rdd.countByValue()` function to accumulate the counts by day. I then used pickle to save the dictionary returned by this function to file for image building off of the cluster.

#### Figure Replication

The code for this segment can be found in `hw2/q1/hw2q1_plot.ipynb`. 

To replicate the figure found in the paper I had to create an axis that had a value for every day between the first query date in the data and the last. To do this I created a range of dates and mapped data retrieved in spark to their place on the range, leaving all non existing days as zeros. The code is below:

```python
# date range
current = min(date_dict.keys())
stop = max(date_dict.keys())
step = timedelta(days=1)

#create range
x_day = []
y_val = []

#month range
months = []
m_split = []
while current <= stop:
    x_day.append(current)
    y_val.append(date_dict[current])
    if current.day == 15:
        months.append(current)
    if current.day == 1:
        m_split.append(current)
    current += step
```

After the values were properly mapped onto the date axis, the figure could be constructed. I will spare the english details and let the code speak:

```python
fig = plt.figure(figsize=(18,3))
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.ticklabel_format(axis='y', style='sci')

plt.suptitle('Sci-Hub activity over 6 months', x=.198, y=1.12, fontsize='xx-large', fontweight='bold')
plt.figtext(x=0.08, y=.98, s='Sci-Hubs domain switch in November 2015, forced by a lawsuit against it, ' \
                            + 'led to some missing data during the 6-month period, but usage hit ' \
                            + 'record levels in February.')


plt.fill_between(x_day, y_val, 0, facecolor='#800000')
plt.ylabel('NUMBER OF DOWNLOADS')
plt.xlim((x_day[0],x_day[-2]))
plt.ylim((0,300000))
plt.xticks(months, ['SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER','JANUARY','FEBRUARY']);

for i in m_split:
    ax.axvline(i, color='grey', linestyle='--')
for mid_month in months:
    ax.text(mid_month, 290000, 'Total: {}'.format(month_count[mid_month.month]), horizontalalignment='center')
```

## 2. Most Downloaded Papers

<img src="https://raw.githubusercontent.com/Eric-D-Stevens/OHSU/master/OHSU_Winter_2020/CS679-Dist_Comp/homework2/images/q2_table.png">

### Data Collection

code: `./hw2/q2/p2.py`

In this section, I used the exact same methodology as the last, mapping only the article DOI to a single column and then using the `rdd.countByValue()` function to complete the summing.

```python
# mapping funciton
def get_doi_only(line):
    fail = line
    try:
        line = line.split('\t')[1] # only look at first column
    except:
        print(fail)
        line = False # for filtering later
    return line
```

### API for Table Creation

code: `./hw2/q2/hw2q2_table.ipynb.py`

The `crossrefapi` library was used to generate citations for the table.

```python
from crossref.restful import Works
works = Works()

def citation_generator(doi):

    article = ''
    record = works.doi(doi)

    # Author information
    try:
        at_el = False
        for a in record['author']:
            if a['sequence'] == 'first':
                article += '{} {}, '.format(a['given'],a['family'])
            else:
                at_el = True
        article = article[:-2]
        if at_el:
            article = article + ', at el '
    except:
        pass
    
    # Date and Title
    try:
        year = record['indexed']['date-time'][:4]
        title = record['title'][0]
        article += '({}) {}. '.format(year, title)
    except:
        pass
    
    # Publication
    try:
        article += '{} ({}):'.format(record['publisher'], record['issue'])
        article += '{}'.format(record['page'])
    except:
        pass   
    return article

```



## 3. Journals & Publishers

<img src="https://raw.githubusercontent.com/Eric-D-Stevens/OHSU/master/OHSU_Winter_2020/CS679-Dist_Comp/homework2/images/q3_table.png">

code: `./hw2/q3/(q3.py, b3.py)`

For this section, a two phase approach was taken. First, a similar method to the first two problems was used. The cluster was used to split and count the publishers, this time using a regular expression to obtain only the publisher DOI prefix. The top 10 counts were extracted as in the other problems and then pickled.

```python
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
```

After this, a second python script was created to load the counts and broadcast them across the cluster. After the broadcast, the publisher prefixes of the top 10 counts were used to filter the prefix .csv file, resulting in an rdd that only contains publisher information form the journals appearing in the top ten. The results were simply combined by mapping the DOI prefixes to each other.

```python
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
```

## 4. Geography

Population Data Source: <a href="https://data.opendatasoft.com/explore/dataset/1000-largest-us-cities-by-population-with-geographic-coordinates%40public/export/?sort=-rank"> OpenDataSoft </a>

### 1) Top 20 Countries

code: `./hw2/q4/p1/p1.py`

The strategy used for the first two sections of question 4 was to download population data and put it in a local directory on the server. For this problem, a dataset was downloaded that contained the population of each of the world's countries in 2015. After using a similar method as earlier in the assignment to count the downloads per country, the population data was broadcasted into spark and used by a mapper to divide the count results by the country's populations. 

<div>
    <img src="https://raw.githubusercontent.com/Eric-D-Stevens/OHSU/master/OHSU_Winter_2020/CS679-Dist_Comp/homework2/images/country_count.png" style="float: left; margin-right: 10%">
    <img src="https://raw.githubusercontent.com/Eric-D-Stevens/OHSU/master/OHSU_Winter_2020/CS679-Dist_Comp/homework2/images/country_rel.png" style="float: left">
</div>



### 2) U.S. Cities

code: `./hw2/q4/p2/p2.py`

For this problem, a dataset was downloaded that contained the population of 1000 US cities. After using a similar method as earlier in the assignment to count the downloads per city, the population data was broadcasted into spark and used by a mapper to divide the count results by the citie's populations. 

<div>
    <img src="https://raw.githubusercontent.com/Eric-D-Stevens/OHSU/master/OHSU_Winter_2020/CS679-Dist_Comp/homework2/images/city_total.png" style="float: left; margin-right: 10%">
    <img src="https://raw.githubusercontent.com/Eric-D-Stevens/OHSU/master/OHSU_Winter_2020/CS679-Dist_Comp/homework2/images/city_capita.png" style="float: left">
</div>

### 3) The Portlands

code: `./hw2/q4/p3/p3.py`

For this final problem several filters were used in order to split the original RDD into a Portland Oregon RDD and a Portland Maine RDD. This was done by first filtering the entire dataset for strings containing “United States” and “Portland”. After obtaining all the “Portlands” of interest, the RDD was split by parsing out and filtering on geographical data in the records. 

<div>
    <img src="https://raw.githubusercontent.com/Eric-D-Stevens/OHSU/master/OHSU_Winter_2020/CS679-Dist_Comp/homework2/images/oregon.png" style="float: left; width: 40%; margin-right: 10%">
    <img src="https://raw.githubusercontent.com/Eric-D-Stevens/OHSU/master/OHSU_Winter_2020/CS679-Dist_Comp/homework2/images/maine.png" style="float: left; width: 40%">
</div>


```python

```
