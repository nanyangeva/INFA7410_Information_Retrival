__author__ = 'Nan Yang'

import csv
import sys
import json
import os
import re
from collections import Counter

def remove_field_name(str):
    """Remove all the special field title of the input."""
    str = re.sub('<[^>]*>', ' ', str)
    return str

def split_to_obtain_token(str):
    """Split the str with special characters."""
    str = re.split('[^a-z0-9]',str)
    str = [x for x in str if x != '']
    return str

def read_file():
    """Read each file name and file content, saved in a dictionary.
       Output(Dictionary): file_content
    """
    # https://blog.csdn.net/lzgs_4/article/details/50371030

    path = input("Please input the path of the dataset (e.g. ...\cranfieldDocs) : ")
    # path = r"C:\Users\15451\PycharmProjects\Nan\dataset\cranfieldDocs"  # the path of all the files
    
    files = os.listdir(path)                     # obtain all the file names in the file folder
    file_content = {}
    for file in files:                          # file is the file name
        f = open(path+"/"+file)
        iter_f = iter(f)
        str = ""
        for line in iter_f:
            line = line.strip()
            line = line.lower()
            str = str + " " + line
        str = remove_field_name(str)
        str = split_to_obtain_token(str)
        file_content[file] = str                 # str is the contect of the file choosen
    return file_content

def read_common_words():
    """Read the common_words from text file to a list."""
    path = r"C:\Users\15451\PycharmProjects\Nan\dataset"   # the path of the common word list
    # path = input("Please input the path of the common words list: ")
    file = "common_words.txt"
    f = open(path+"/"+file)
    iter_f = iter(f)
    list = []
    i=0
    for line in iter_f:
        line = line.strip()
        line = line.lower()
        list.append(line)
    return list

def remove_common_words(check_list,common_words):
    """check the elements of check_list, and remove elements belong to common_words list.
    check_list : a dictionary
    common_words: a list"""
    for value in check_list.values():          # value: list
        i=0
        while i < len(value):
            if value[i] in common_words:
                del value[i]
            else:
                i += 1
    return check_list

def total_number():
    """Count the total number of words."""
    total_number = 0
    file_read = read_file()
    for key in file_read:
        total_number = total_number + len(file_read[key])
    return total_number

def vacabulary_size():
    """Count the total number of unique words."""
    file_read = read_file()
    vacabulary_list = []
    for key in file_read:
        for element in file_read[key]:
            if element not in vacabulary_list:
                vacabulary_list.append(element)
    return len(vacabulary_list)

def top_50():
    """Count the times each word exist, and work out the top 50 list."""
    file_read = read_file()
    vacabulary_list = []
    for key in file_read:
        vacabulary_list.extend(file_read[key])
    top_50 = Counter(vacabulary_list).most_common(50)
    return(top_50)

def output_question1_token():
    """Output the result of question 1 after token."""
    document = open('Task1.txt','w')
    print("Total Number : ",total_number(),file=document)
    print("Vacabulary Size : ", vacabulary_size(), file=document)
    print("Top 50 : ", file=document)
    list = top_50()
    for i in range(len(list)):
        print(list[i][0],list[i][1],file=document)
    document.close()

def stopping():
    """This is an independent process to do stopping."""
    file_content = read_file()                                  # file_content:   Dictionary
    common_words_list = read_common_words()                     # common_words_list: List
    file_content_with_stopping = remove_common_words(file_content,common_words_list)
    return file_content_with_stopping

def output_question2_stopping():
    file_read = stopping()
    # total_number
    total_number = 0
    for key in file_read:
        total_number = total_number + len(file_read[key])
    # vacabulary_size
    vacabulary_list = []
    for key in file_read:
        for element in file_read[key]:
            if element not in vacabulary_list:
                vacabulary_list.append(element)
    vacabulary_size = len(vacabulary_list)
    # top_50
    vacabulary_list = []
    for key in file_read:
        vacabulary_list.extend(file_read[key])
    top_50 = Counter(vacabulary_list).most_common(50)
    # print out the result
    document = open('Task2.txt','w')
    print("Total Number : ",total_number,file=document)
    print("Vacabulary Size : ", vacabulary_size, file=document)
    print("Top 50 : ", file=document)
    for i in range(len(top_50)):
        print(top_50[i][0],top_50[i][1],file=document)
    document.close()

def build_inverted_index():
    """Generate out the inverted index."""
    # vacabulary list (with out common_words)
    file_read = read_file()
    vacabulary_list = []
    common_words = read_common_words()
    for key in file_read:
        for element in file_read[key]:
            if (element not in vacabulary_list) & (element not in common_words):
                vacabulary_list.append(element)

    # word list of each file
    content = remove_common_words(file_read, common_words)    # content = stopping()

    # generate direction to save result
    inverted_index = {}
    for item in vacabulary_list:
        inverted_index[item]={}

    for file_id in content.keys():
        frequency = Counter(content[file_id])    # the frequency of words in a file : {'slipstream': 5, 'lift': 4, 'wing': 3}
        for word in frequency.keys():
            inverted_index[word][file_id] = frequency[word]

    inverted_index = sorted(inverted_index.items(), key=lambda d:d[0], reverse = False)
    inverted_index = dict(inverted_index)
    return inverted_index

def key_word_search():
    """Return the top 10 documents with highest sum of frequency of all words in array.
    key_word_list : an list of all the key words need to consider.
    """
    # key_word_search(['0001','0005','000degree'])
    inverted_index = build_inverted_index()

    key_word_list = []
    word = ""
    while word != ";":
        word = input(r"Please input the key word (end with ;): ")
        if word != ";":
            key_word_list.append(word)

    sum_result = Counter({})

    for key_word in key_word_list:
        x = inverted_index[key_word]    # X(dictionary):  {'cranfield0117': 1, 'cranfield0302': 1}
        sum_result = sum_result + Counter(x)

    top_10 = sum_result.most_common(10)

    return top_10
    # ??????? if the key in list is not exist: warning ?????
    # ????? Allow user to enter the name of the corpus directory (assume that corpus directory is in the same directory as your executable code)


def main():
    file_read = read_file()

if __name__=="__main__":
    main()