# CS 562: Homework 1
### Eric D. Stevens
### January 15, 2019


## Part 1 

### 1. My Program

My program for this section, `part_1.py`, has two modes of operation. First is a file download utility, 
second is a program to remove the text from the files and write it to an output file.

#### The download utility

The download utility uses the provided directory url and scrapes that directory using the beautiful soup
library. After pulling all the links from the `*.gz` files it downloads them to a folder named `cna_eng`.

This is done from the terminal like so: `python part_1.py -d`

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

#### Text Extraction

Th text extraction is all done in the main function. The `lxml.etree` utility is used to extract only the
paragraph elements from within the `TEXT` tags. this is done as follows:

```python
for arg in sys.argv[1:]:
    with gzip.open(arg) as gzipped_f:
        tree = etree.parse(gzipped_f).getroot()
        for doc in tree.findall('DOC'):
            text_attr = doc.find('TEXT')
            for par in text_attr.findall('P'):
                print(par.text)
```
Every time a paragraph is found it is written to standard out. Therefore, the output can be written to a 
file with an output redirect.

The usage for this operation is as stated in the assignment. Since our download operation put all of the 
gzipped files in a directory named `cna_eng`, we can write all of them to a file called `deserialized.txt` 
as follows:

`python part_1.py cna_eng/*.gz > deserialized.txt`

### 2. Sample Output
`head -n 100 deserialized.txt `

```
Mainland Chinese Foreign Minister Qian Qichen
was highly skeptical of Tokyo's explanations of the content of the
newly published US-Japan guidelines for defense cooperation when he
met Monday in Beijing with representatives of Japan's press.
Qian also said the time is not ripe yet for a trilateral official
dialogue among Washington, Beijing and Tokyo on defense, adding that
"scholarly discussion" would be appropriate at the present.
Qian's remarks indicate that despite explanations of the new
guidelines by Japanese Prime Minister Ryutaro Hashimoto and Foreign
Minister Keizo Obuchi, Beijing is still very worried about whether
Taiwan falls within the sphere of the bilateral defense agreement.
According to reports in the Japanese media, among Qian's concerns
are:
-- If the defense pact is a matter between Washington and Tokyo,
it should be unnecessary to renew it, hence putting its content into
doubt.
-- Although the new guidelines do not specifically mention
geographic criteria, there is still speculation that they cover
Taiwan.
-- Some have argued for raising the transparency of the bilateral
agreement, while others advocate keeping it ambiguous and opaque.
The American Chamber of Commerce (AmCham) in
Taipei on Wednesday appealed for an early conclusion of trade
consultations between the United States and the Republic of China on
terms for Taiwan to join the World Trade Organization (WTO).
AmCham President Jeffrey R. Williams told a news conference that
all AmCham members hope bilateral ROC-US WTO talks will be concluded
as soon as possible to facilitate Taiwan's entry to the Geneva-based
world trade regulatory body.
According to Williams, most American business people with
interests in Taiwan are convinced that they will benefit from
Taiwan's WTO accession because Taiwan would be required to further
open its market and better protect intellectual property rights.
Williams, who just returned from a "doorknocking" visit to
Washington, D.C. at the head of a 12-member AmCham delegation, said
the US executive branch agreed with AmCham that Taiwan's WTO
accession should not be linked to mainland China's membership
application.
"We agree that Taiwan's WTO entry should be considered completely
on the basis of its own economic conditions," Williams said, adding
that Taiwan is likely to conclude WTO-related trade consultations
with the United States before the end of bilateral WTO talks between
Washington and Beijing.
During its stay in the United States, the AmCham delegation met
with many Clinton administration officials and Congress members to
exchange views on ways to help American corporations upgrade their
overseas competitiveness.
Williams said the AmCham mission had urged various US federal
agencies to allow their senior officials to make frequent visits to
Taiwan to help boost bilateral trade and economic cooperation for
mutual benefits.
Even though the Clinton administration was busy preparing for
mainland Chinese President Jiang Zemin's planned visit to the United
States late this month, Williams said, many federal government
officials still showed keen interest in listening to AmCham's
suggestions and opinions about reinforcing Taipei-Washington trade
and economic ties.
As to the AmCham 1997-98 Taiwan White Paper, which he formally
unveiled at a news conference held in Washington, D.C. last Thursday,
Williams said the annual report mainly analyzed Taiwan's current
economic and investment climate as a reference for American companies
intending to invest in Taiwan, adding that the White Paper was not
aimed at criticizing any party.
The White Paper said Taiwan's restrictions on trade and
investment across the Taiwan Strait have not only hindered the
development of its own industries but have also discouraged
multinational business groups from setting up a foothold on the
island. It further claimed that the ROC government's master plan to
develop Taiwan into an Asia-Pacific operations center would remain a
pipe dream if Taiwan companies are not allowed to enter the vast
mainland market directly and obtain access to its resources.
Williams said AmCham's analysis was made purely from a commercial
viewpoint, adding that AmCham members believe Taiwan must establish
direct communications and transport links with mainland China so that
Taiwan-based companies can make successful inroads into the world's
largest market.
Evergreen's green-colored ships and green
matchbox-like containers are the hope of the port of Gioia Tauro in
southern Italy.
Taiwan-based Evergreen Marine Corp., which operates one of the
largest container fleets in the world, is wagering on Gioia Tauro, a
newly-developed and non-urban port area, attempting to build it into
the third largest container port in the world.
Evergreen is also targeting Gioia Tauro as a gateway to all
Mediterranean-rim states and the Black Sea to the north, said a
company spokesman.
The Italian government has put up nearly US$180 million since
1975 to develop the quiet backwater fishing port into a commercial
harbor. With most parts of the development already finished, the
harbor accommodated some 1,270 ships in the first six months of this
year. The harbor bureau there estimated that its transshipment
capacity may reach 1.4 million TEUs this year.
Although the port is fully operational, its peripheral facilities
are still in dire need of help, Aldo Alessio, mayor of Gioia Tauro,
lamented. He noted that many support works have been left unfinished
due to budget constraints, with highways in the vicinity only four
meters wide and the nearby hinterland remaining undeveloped and
blanketed by weeds.
Taipei's representative office in Rome, which has generally been
reluctant to beckon Taiwan investors to Italy for fear that the
```

### 3. Summary

I thought that the functionized downlad utility was an elegant solution. Giving the user of the code the
ability to downlad the files from the program itself.

The xml files themselves were not very structurally complex. This made it easy to parse them. If more
complicated files needed parsing I would want to step up the complexity of the xml parser.

## Part 2 

In this section the program takes an input of the form of the output file from Part 1 and outputs a file
of tokens. This operation is done in two parts, the sentence tokenizer and the word tokenizer, both of
which utilize the `nltk` library.

#### Sentence Tokenizer

The sentence tokenizer reads in the output of Part 1, replacing all newline characters with spaces.
This results in a single, contiguous string. From there the `nltk.sent_tokenize` function is used to 
split the string into sentences, one sentence per list element. Then each list element is written to a temp
file that will be used by the word tokenizer. 

The code for the sentence tokenizer is as follows:

```python
def nltk_sentence_tokenizer(input_file = "deserialized.txt",
                            output_file = "nltk_tokenized_sentences.txt"):

    ''' This function takes input of the form of the output of part 1 and
    writes a new file where each sentence is contained in a single line as
    parsed by nlte.sent_tokenizer'''

    with open('temp.txt', 'w') as output_stream:
        with open(input_file, 'r') as input_stream:
            single_line = input_stream.readline()
            while single_line:
                output_stream.write(single_line[:-1]+' ')
                single_line = input_stream.readline()

    single_line_file_stream = open('temp.txt', 'r')
    single_line_file = single_line_file_stream.read()
    single_line_file_stream.close()
    os.system('rm temp.txt')

    tokenized_sentences = nltk.tokenize.sent_tokenize(single_line_file)
    with open(output_file, 'w') as output_stream:
        for token_sentence in tokenized_sentences:
            output_stream.write(token_sentence+'\n')
```

#### Word Tokenizer

The word token reads in, line by line,  the file that was output by the sentence tokenizer and breaks 
appart the words in each sentence into tokens using the `nltk.word_tokenize` function. After it does 
this it combs through the tokens and removes tokens that are punctuations in pythons punctuation list.
After each line is operated on it is written to a file. The default output file name is `nltk_tokenized.txt`.

The code for the word tokenizer is as follows:

```python
def nltk_word_tokenizer(input_file = "nltk_tokenized_sentences.txt",
                        output_file = "nltk_tokenized.txt"):

    '''This function takes the file output from the sentence tokenizer
    and uses it to tokenize words as parsed by nltk.word_tokenizer.'''

    with open(output_file, 'w') as output_stream:
        with open(input_file, 'r') as input_stream:
            single_line = input_stream.readline()
            punct_set = set(string.punctuation)
            while single_line:
                tokienized_line = nltk.tokenize.word_tokenize(single_line)
                output_stream.write(' '.join([tkn.upper() for tkn in tokienized_line
                                              if tkn not in punct_set])+'\n')
                single_line = input_stream.readline()
```

#### Main Function and Final Number of sentences:

The main function runs these operations. 

Here is the main code:

```python
def main():
    if len(sys.argv)==1:
        nltk_sentence_tokenizer()
        nltk_word_tokenizer()

    elif len(sys.argv)==3:
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]
        nltk_sentence_tokenizer(input_file=input_file_name)
        nltk_word_tokenizer(output_file=output_file_name)

    else:
        print("ERROR: incorrect usage")
        exit()

    os.system('rm -f nltk_tokenized_sentences.txt')
```


Here is a sample of the output after running main:

`head -n 20 nltk_tokenized.txt`

```
MAINLAND CHINESE FOREIGN MINISTER QIAN QICHEN WAS HIGHLY SKEPTICAL OF TOKYO 'S EXPLANATIONS OF THE CONTENT OF THE NEWLY PUBLISHED US-JAPAN GUIDELINES FOR DEFENSE COOPERATION WHEN HE MET MONDAY IN BEIJING WITH REPRESENTATIVES OF JAPAN 'S PRESS
QIAN ALSO SAID THE TIME IS NOT RIPE YET FOR A TRILATERAL OFFICIAL DIALOGUE AMONG WASHINGTON BEIJING AND TOKYO ON DEFENSE ADDING THAT `` SCHOLARLY DISCUSSION '' WOULD BE APPROPRIATE AT THE PRESENT
QIAN 'S REMARKS INDICATE THAT DESPITE EXPLANATIONS OF THE NEW GUIDELINES BY JAPANESE PRIME MINISTER RYUTARO HASHIMOTO AND FOREIGN MINISTER KEIZO OBUCHI BEIJING IS STILL VERY WORRIED ABOUT WHETHER TAIWAN FALLS WITHIN THE SPHERE OF THE BILATERAL DEFENSE AGREEMENT
ACCORDING TO REPORTS IN THE JAPANESE MEDIA AMONG QIAN 'S CONCERNS ARE -- IF THE DEFENSE PACT IS A MATTER BETWEEN WASHINGTON AND TOKYO IT SHOULD BE UNNECESSARY TO RENEW IT HENCE PUTTING ITS CONTENT INTO DOUBT
-- ALTHOUGH THE NEW GUIDELINES DO NOT SPECIFICALLY MENTION GEOGRAPHIC CRITERIA THERE IS STILL SPECULATION THAT THEY COVER TAIWAN
-- SOME HAVE ARGUED FOR RAISING THE TRANSPARENCY OF THE BILATERAL AGREEMENT WHILE OTHERS ADVOCATE KEEPING IT AMBIGUOUS AND OPAQUE
THE AMERICAN CHAMBER OF COMMERCE AMCHAM IN TAIPEI ON WEDNESDAY APPEALED FOR AN EARLY CONCLUSION OF TRADE CONSULTATIONS BETWEEN THE UNITED STATES AND THE REPUBLIC OF CHINA ON TERMS FOR TAIWAN TO JOIN THE WORLD TRADE ORGANIZATION WTO
AMCHAM PRESIDENT JEFFREY R. WILLIAMS TOLD A NEWS CONFERENCE THAT ALL AMCHAM MEMBERS HOPE BILATERAL ROC-US WTO TALKS WILL BE CONCLUDED AS SOON AS POSSIBLE TO FACILITATE TAIWAN 'S ENTRY TO THE GENEVA-BASED WORLD TRADE REGULATORY BODY
ACCORDING TO WILLIAMS MOST AMERICAN BUSINESS PEOPLE WITH INTERESTS IN TAIWAN ARE CONVINCED THAT THEY WILL BENEFIT FROM TAIWAN 'S WTO ACCESSION BECAUSE TAIWAN WOULD BE REQUIRED TO FURTHER OPEN ITS MARKET AND BETTER PROTECT INTELLECTUAL PROPERTY RIGHTS
WILLIAMS WHO JUST RETURNED FROM A `` DOORKNOCKING '' VISIT TO WASHINGTON D.C. AT THE HEAD OF A 12-MEMBER AMCHAM DELEGATION SAID THE US EXECUTIVE BRANCH AGREED WITH AMCHAM THAT TAIWAN 'S WTO ACCESSION SHOULD NOT BE LINKED TO MAINLAND CHINA 'S MEMBERSHIP APPLICATION
`` WE AGREE THAT TAIWAN 'S WTO ENTRY SHOULD BE CONSIDERED COMPLETELY ON THE BASIS OF ITS OWN ECONOMIC CONDITIONS '' WILLIAMS SAID ADDING THAT TAIWAN IS LIKELY TO CONCLUDE WTO-RELATED TRADE CONSULTATIONS WITH THE UNITED STATES BEFORE THE END OF BILATERAL WTO TALKS BETWEEN WASHINGTON AND BEIJING
DURING ITS STAY IN THE UNITED STATES THE AMCHAM DELEGATION MET WITH MANY CLINTON ADMINISTRATION OFFICIALS AND CONGRESS MEMBERS TO EXCHANGE VIEWS ON WAYS TO HELP AMERICAN CORPORATIONS UPGRADE THEIR OVERSEAS COMPETITIVENESS
WILLIAMS SAID THE AMCHAM MISSION HAD URGED VARIOUS US FEDERAL AGENCIES TO ALLOW THEIR SENIOR OFFICIALS TO MAKE FREQUENT VISITS TO TAIWAN TO HELP BOOST BILATERAL TRADE AND ECONOMIC COOPERATION FOR MUTUAL BENEFITS
EVEN THOUGH THE CLINTON ADMINISTRATION WAS BUSY PREPARING FOR MAINLAND CHINESE PRESIDENT JIANG ZEMIN 'S PLANNED VISIT TO THE UNITED STATES LATE THIS MONTH WILLIAMS SAID MANY FEDERAL GOVERNMENT OFFICIALS STILL SHOWED KEEN INTEREST IN LISTENING TO AMCHAM 'S SUGGESTIONS AND OPINIONS ABOUT REINFORCING TAIPEI-WASHINGTON TRADE AND ECONOMIC TIES
AS TO THE AMCHAM 1997-98 TAIWAN WHITE PAPER WHICH HE FORMALLY UNVEILED AT A NEWS CONFERENCE HELD IN WASHINGTON D.C. LAST THURSDAY WILLIAMS SAID THE ANNUAL REPORT MAINLY ANALYZED TAIWAN 'S CURRENT ECONOMIC AND INVESTMENT CLIMATE AS A REFERENCE FOR AMERICAN COMPANIES INTENDING TO INVEST IN TAIWAN ADDING THAT THE WHITE PAPER WAS NOT AIMED AT CRITICIZING ANY PARTY
THE WHITE PAPER SAID TAIWAN 'S RESTRICTIONS ON TRADE AND INVESTMENT ACROSS THE TAIWAN STRAIT HAVE NOT ONLY HINDERED THE DEVELOPMENT OF ITS OWN INDUSTRIES BUT HAVE ALSO DISCOURAGED MULTINATIONAL BUSINESS GROUPS FROM SETTING UP A FOOTHOLD ON THE ISLAND
IT FURTHER CLAIMED THAT THE ROC GOVERNMENT 'S MASTER PLAN TO DEVELOP TAIWAN INTO AN ASIA-PACIFIC OPERATIONS CENTER WOULD REMAIN A PIPE DREAM IF TAIWAN COMPANIES ARE NOT ALLOWED TO ENTER THE VAST MAINLAND MARKET DIRECTLY AND OBTAIN ACCESS TO ITS RESOURCES
WILLIAMS SAID AMCHAM 'S ANALYSIS WAS MADE PURELY FROM A COMMERCIAL VIEWPOINT ADDING THAT AMCHAM MEMBERS BELIEVE TAIWAN MUST ESTABLISH DIRECT COMMUNICATIONS AND TRANSPORT LINKS WITH MAINLAND CHINA SO THAT TAIWAN-BASED COMPANIES CAN MAKE SUCCESSFUL INROADS INTO THE WORLD 'S LARGEST MARKET
EVERGREEN 'S GREEN-COLORED SHIPS AND GREEN MATCHBOX-LIKE CONTAINERS ARE THE HOPE OF THE PORT OF GIOIA TAURO IN SOUTHERN ITALY
TAIWAN-BASED EVERGREEN MARINE CORP. WHICH OPERATES ONE OF THE LARGEST CONTAINER FLEETS IN THE WORLD IS WAGERING ON GIOIA TAURO A NEWLY-DEVELOPED AND NON-URBAN PORT AREA ATTEMPTING TO BUILD IT INTO THE THIRD LARGEST CONTAINER PORT IN THE WORLD
```

#### Number of sentences in corpus: 588,701

## Part 3
