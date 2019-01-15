'''Eric D. Stevens: CS 563: Homework 1: Part 2'''

import sys
import os
import string
import nltk.tokenize

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


if __name__ == "__main__":
    main()



