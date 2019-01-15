"Eric D. Stevens: CS 562: Homework 1: Part 1"

import re
import os
import sys
import gzip
import requests
import bs4
from lxml import etree


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

def main():
    ''' When calling 'part1.py', the main function manages whether
    to download the files or to output the text from the paragraph
    elements within the files that are already downloaded. If you
    want to download the files use the 'python part1.py -d'. To
    extract the text form paragraph elements use 'python part1.py
    file_1.xml.gz file_2.xml.gz ...' '''

    # if -d tag is found run the download command
    # usage: "python part1.py -d"
    if sys.argv[1] == '-d':
        download_files()

    # otherwise takes list of gzipped xml file names
    # and outputs the text from within the paragraph
    # elements in those files.
    else:
        for arg in sys.argv[1:]:
            with gzip.open(arg) as gzipped_f:
                tree = etree.parse(gzipped_f).getroot()
                for doc in tree.findall('DOC'):
                    text_attr = doc.find('TEXT')
                    for par in text_attr.findall('P'):
                        print(par.text)


if __name__ == "__main__":
    main()
