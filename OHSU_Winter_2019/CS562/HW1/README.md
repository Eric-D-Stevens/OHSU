# CS 562: Homework 1
### Eric D. Stevens
### January 15, 2019


## Part 1 

### 1. My Program

My program for this section, `part_1.py`, has two modes of operation. First is a file download utility, 
second is a program to remove the text from the files and write it to an output file.

#### The download utility

The code for the download utility is as follows:

```python
def download_files():
    ''' This function will download  all files from the hosted directory
    and save them in a subdirectory of pwd named 'cna_eng'.'''

    # directory of files to download
    url = "https://cslu.ohsu.edu/~bedricks/courses/cs662/hw/HW1/GW-cna_eng/"

    # set folder as the get request
    req = requests.get(url)

    # parse out all <a> tags
    data = bs4.BeautifulSoup(req.text, "html.parser")
    for link in data.find_all("a"):

        # if the <a> contains the string ".gz"
        if ".gz" in link["href"]:

            # pull the file into memory
            req = requests.get(url + link["href"])
            print(link["href"])
            # obtain a filename from the url
            gz_re = re.search('cna_eng_.+gz', req.url)
            filename = req.url[gz_re.start():gz_re.end()]

            # wirte the files
            folder_name = 'cna_eng'
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
            with open(folder_name+'/'+filename, 'w') as new_file:
                new_file.write(req.content)
```


## Part 2 


## Part 3
