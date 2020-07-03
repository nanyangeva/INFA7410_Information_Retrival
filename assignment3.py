__author__ = 'Nan Yang'

import csv
import sys
import json
import os
import re
import math
import numpy
from collections import Counter


def remove_field_name(str):
    """Remove all the special field title of the input."""
    str = re.sub('<[^>]*>', ' ', str)
    return str


def split_to_obtain_token(str):
    """Split the str with special characters."""
    str = re.split('[^a-z0-9]', str)
    str = [x for x in str if x != '']
    return str


def read_file():
    """Read each file name and file content, saved in a dictionary.
       Output(Dictionary): file_content
    """
    # https://blog.csdn.net/lzgs_4/article/details/50371030

    path = input("Please input the path of the dataset (e.g. ...\cranfieldDocs) : ")
    # path = r"C:\Users\15451\PycharmProjects\Nan\dataset\cranfieldDocs"  # the path of all the files

    files = os.listdir(path)  # obtain all the file names in the file folder
    file_content = {}
    for file in files:  # file is the file name
        f = open(path + "/" + file)
        iter_f = iter(f)
        str = ""
        for line in iter_f:
            line = line.strip()
            line = line.lower()
            str = str + " " + line
        str = remove_field_name(str)
        str = split_to_obtain_token(str)
        file_content[file] = str  # str is the contect of the file choosen
    return file_content


def read_common_words():
    """Read the common_words from text file to a list."""
    path = r"C:\Users\15451\PycharmProjects\Nan\dataset"  # the path of the common word list
    # path = input("Please input the path of the common words list: ")
    file = "common_words.txt"
    f = open(path + "/" + file)
    iter_f = iter(f)
    list = []
    i = 0
    for line in iter_f:
        line = line.strip()
        line = line.lower()
        list.append(line)
    return list


def remove_common_words(check_list, common_words):
    """check the elements of check_list, and remove elements belong to common_words list.
    check_list : a dictionary
    common_words: a list"""
    for value in check_list.values():  # value: list
        i = 0
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
    return (top_50)


def output_question1_token():
    """Output the result of question 1 after token."""
    document = open('Task1.txt', 'w')
    print("Total Number : ", total_number(), file=document)
    print("Vacabulary Size : ", vacabulary_size(), file=document)
    print("Top 50 : ", file=document)
    list = top_50()
    for i in range(len(list)):
        print(list[i][0], list[i][1], file=document)
    document.close()


def stopping():
    """This is an independent process to do stopping."""
    file_content = read_file()  # file_content:   Dictionary
    common_words_list = read_common_words()  # common_words_list: List
    file_content_with_stopping = remove_common_words(file_content, common_words_list)
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
    document = open('Task2.txt', 'w')
    print("Total Number : ", total_number, file=document)
    print("Vacabulary Size : ", vacabulary_size, file=document)
    print("Top 50 : ", file=document)
    for i in range(len(top_50)):
        print(top_50[i][0], top_50[i][1], file=document)
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
    content = remove_common_words(file_read, common_words)  # content = stopping()

    # generate direction to save result
    inverted_index = {}
    for item in vacabulary_list:
        inverted_index[item] = {}

    for file_id in content.keys():
        frequency = Counter(
            content[file_id])  # the frequency of words in a file : {'slipstream': 5, 'lift': 4, 'wing': 3}
        for word in frequency.keys():
            inverted_index[word][file_id] = frequency[word]

    inverted_index = sorted(inverted_index.items(), key=lambda d: d[0], reverse=False)
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
        x = inverted_index[key_word]  # X(dictionary):  {'cranfield0117': 1, 'cranfield0302': 1}
        sum_result = sum_result + Counter(x)

    top_10 = sum_result.most_common(10)

    return top_10


def vector_space_model():
    """Task 1: Generate dictionary to indicate the show condition of word in file.
    output: {"experiment" : [1 0 1 0  ....] }"""
    # path : C:\Users\15451\PycharmProjects\Nan\dataset\cranfieldDocs
    file_read = read_file()
    word_list = []
    word_dic = []
    common_words = read_common_words()
    tf = {}

    # step 1 : word_dic
    content = remove_common_words(file_read, common_words)     # content: {"cranfield0001": ["a","b"]}

    for key in content.keys():
        word_list.extend(content[key])
    top_1000 = Counter(word_list).most_common(1000)
    word_dic = [item[0] for item in top_1000]

    # step 2 : tf dictionary
    # change content to frequency dictionary
    for key in content.keys():                                # content: {"cranfield0001": {"1":6}}
        value = Counter(content[key])
        content[key] = value

    for file_name in content.keys():
        vector = []
        for word in word_dic:
            vector.append(content[file_name][word])
        tf[file_name] = vector

    # step 3 : IDF
    N = len(tf)
    nk = Counter({})
    IDF_Top1000words = []
    Cosine = {}

    frequency = content
    for file_name in frequency.keys():
        for word in frequency[file_name]:
            frequency[file_name][word] = 1
    for file_name in frequency.keys():
        x = frequency[file_name]
        nk = nk + Counter(x)
    for word in word_dic:
        IDF_Top1000words.append(math.log(N/nk[word]))

    # step 4 : TF-IDF
    TF_IDF ={}
    for file_name in tf:
        TF_IDF[file_name] = numpy.multiply(numpy.array(tf[file_name]),numpy.array(IDF_Top1000words))   # doc multiple

    # Task 2
    # input the query
    # test1 : Query = “method”
    # test2 : Query = “transfer equations”
    # test3 : Query = “free problem case”
    query = input("Please input the query words with space as seperator: ")
    query = query.split(" ")
    Q = [0 for i in range(1000)]
    for word in query:
        index = word_dic.index(word)
        Q[index] = IDF_Top1000words[index]

    # Cosine
    if sum(map(lambda x: x * x, Q)) == 0:
        print("These keywords are not involved in the high frequency word list of corpus!")
    else:
        for file_name in TF_IDF.keys():
            if math.sqrt(sum(numpy.array(TF_IDF[file_name]) * numpy.array(TF_IDF[file_name])))!=0:
                cosine_single_file = sum(numpy.array(TF_IDF[file_name]) * numpy.array(Q))\
                                 /math.sqrt(sum(numpy.array(TF_IDF[file_name]) * numpy.array(TF_IDF[file_name]))\
                                            * sum(numpy.array(Q) * numpy.array(Q)))
            else:
                cosine_single_file = 0
            Cosine[file_name] = cosine_single_file
    Cosine = sorted(Cosine.items(), key=lambda d: d[1], reverse=True)
    Cosine_Top10 = [k[0] for k in Cosine[:10]]
    return(Cosine_Top10)

def speed_up():
    inverted_index = build_inverted_index()

    query = input("Please input the query words with space as seperator: ")
    query = query.split(" ")
    dict = Counter({})
    for word in query:
        dict = dict + Counter(inverted_index[word])
    files_with_query_word = dict.keys()

    file_read = read_file()
    word_list = []
    word_dic = []
    common_words = read_common_words()
    tf = {}
    content = {}

    # step 1 : word_dic
    content = remove_common_words(file_read, common_words)     # content: {"cranfield0001": ["a","b"]}
    for key in content.keys():
        word_list.extend(content[key])
    top_1000 = Counter(word_list).most_common(1000)
    word_dic = [item[0] for item in top_1000]

    # step 2 : tf dictionary
    # change content to frequency dictionary
    for key in content.keys():                                # content: {"cranfield0001": {"1":6}}
        value = Counter(content[key])
        content[key] = value

    for file_name in content.keys():
        vector = []
        for word in word_dic:
            vector.append(content[file_name][word])
        tf[file_name] = vector

    # step 3 : IDF
    N = len(tf)
    nk = Counter({})
    IDF_Top1000words = []
    Cosine = {}

    frequency = content
    for file_name in frequency.keys():
        for word in frequency[file_name]:
            frequency[file_name][word] = 1
    for file_name in frequency.keys():
        x = frequency[file_name]
        nk = nk + Counter(x)
    for word in word_dic:
        IDF_Top1000words.append(math.log(N/nk[word]))

    # step 4 : TF-IDF                                                       here is different
    TF_IDF ={}
    for file_name in files_with_query_word:
        TF_IDF[file_name] = numpy.multiply(numpy.array(tf[file_name]),numpy.array(IDF_Top1000words))   # doc multiple

    # Task 2
    Q = [0 for i in range(1000)]
    for word in query:
        index = word_dic.index(word)
        Q[index] = IDF_Top1000words[index]

    # Cosine
    if sum(map(lambda x: x * x, Q)) == 0:
        print("These keywords are not involved in the high frequency word list of corpus!")
    else:
        for file_name in TF_IDF.keys():
            cosine_single_file = sum(numpy.array(TF_IDF[file_name]) * numpy.array(Q)) \
                                     / math.sqrt(sum(numpy.array(TF_IDF[file_name]) * numpy.array(TF_IDF[file_name])) \
                                                 * sum(numpy.array(Q) * numpy.array(Q)))
            Cosine[file_name] = cosine_single_file
    Cosine = sorted(Cosine.items(), key=lambda d: d[1], reverse=True)
    Cosine_Top10 = [k[0] for k in Cosine[:10]]
    return (Cosine_Top10)


def main():
    file_read = read_file()


if __name__ == "__main__":
    main()