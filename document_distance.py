# 6.0001 Spring 2022

import string
import math

from pyparsing import countedArray



def load_file(filename):
    """
    Args:
        filename: string, name of file to read
    Returns:
        string, contains file contents
    """
    # print("Loading file %s" % filename)
    inFile = open(filename, 'r')
    line = inFile.read().strip()
    for char in string.punctuation:
        line = line.replace(char, "")
    inFile.close()
    return line.lower()

# helper function to combine frequencies of letters or words into one dictionary so that there are no repeats and each original dictionary isn't altered
def combine(dict1, dict2):

    dict = {}
    for i in dict1:
        dict[i] = dict1[i]

    for i in dict2:
        if i in dict:
            dict[i] += dict2[i]
        else:
            dict[i] = dict2[i]

    return dict



# turns string of text into list of words
def prep_data(input_text):
    """
    Args:
        input_text: string representation of text from file,
                    assume the string is made of lowercase characters
    Returns:
        list representation of input_text, where each word is a different element in the list
    """
    return input_text.split()



# turns list of words or letters into a dictionary with number of occurrences of each word as a value
def get_frequencies(word_list):
    """
    Args:
        word_list: list of strings, all are made of lowercase characters
    Returns:
        dictionary that maps string:int where each string
        is a letter or word in l and the corresponding int
        is the frequency of the letter or word in l
    """
    word_dictionary = {}

    # loops through all the words in a list, creates a dictionary and counts number of times each word occurs in the list 
    for i in word_list:
        if i in word_dictionary:
            word_dictionary[i] += 1
        else:
            word_dictionary[i] = 1

    return word_dictionary



# turns a word into a list of characters, creates dictionary showing how many times each letter appears in the word
def get_letter_frequencies(word):
    """
    Args:
        word: word as a string
    Returns:
        dictionary that maps string:int where each string
        is a letter in word and the corresponding int
        is the frequency of the letter in word
    """
    word_letters = list(word)
    letter_frequencies = get_frequencies(word_letters)

    return letter_frequencies


def calculate_similarity_score(dict1, dict2):
    """

    Args:
        dict1: frequency dictionary of letters of word1 or words of text1
        dict2: frequency dictionary of letters of word2 or words of text2
    Returns:
        float, a number between 0 and 1, inclusive
        representing how similar the words/texts are to each other
    """
    DIFF = 0
    ALL = 0
    combined_dictionary = combine(dict1, dict2) # takes two dictionaries, returns a combined version with no repeats

    for key in combined_dictionary:
        ALL += combined_dictionary[key] # sums all the frequencies in both dictionaries
        # if a word in the combined dictionary is in both dict1 and dict2, adds the difference of their frequencies to DIFF
        if key in dict1 and key in dict2:
            DIFF += abs(dict1[key] - dict2[key])
        # checks if a word is just in dict1, adds that frequency to DIFF
        elif key not in dict2:
            DIFF += dict1[key]
        # checks if a word is just in dict2, adds that frequency to DIFF
        else:
            DIFF += dict2[key]
    # similarity score
    return round((1 - DIFF / ALL), 2)


def get_most_frequent_words(dict1, dict2):
    """
    Args:
        dict1: frequency dictionary for one text
        dict2: frequency dictionary for another text
    Returns:
        list of the most frequent word(s) in the input dictionaries
    """
    combined_word_dict = combine(dict1, dict2)

    max_freq = max(combined_word_dict.values()) 

    # checks every word in the combined dictionary, checks if its freq is the highest, appends the word to most_freq_word list and returns that (sorted if necessary)
    most_freq_word = []
    for word in combined_word_dict:
      if combined_word_dict[word] == max_freq:
        most_freq_word.append(word)

    return sorted(most_freq_word) 




def get_tf(text_file):
    """
    Args:
        text_file: name of file in the form of a string
    Returns:
        a dictionary mapping each word to its TF

    * TF(i) = (number times word *i* appears in the document) / (total number of words in the document)
    """
    # loads file and preps data
    text = load_file(text_file)
    word_list = prep_data(text)
    word_frequencies = get_frequencies(word_list) # creates a frequency dictionary from the word list

    #creates a dictionary with each word being the key and each value being the TF
    dict = {}
    for word in word_frequencies:
        dict[word] = word_frequencies[word] / len(word_list)
    
    return dict
    


def get_idf(text_files):
    """
    Args:
        text_files: list of names of files, where each file name is a string
    Returns:
       a dictionary mapping each word to its IDF

    * IDF(i) = log_10(total number of documents / number of documents with word *i* in it)

    """
    word_lists = [] # list of word lists (files)
    for file_name in text_files:
        words = (load_file(file_name))
        word_lists.append(prep_data(words)) # adds a list of words for each file to word_lists for each iteration

    big_list = [] # one list of unique words rather than a list of lists of words
    for word_list in word_lists:
        for word in word_list:
            if word not in big_list:
                big_list.append(word)
    
    # counts how many times a unique word is in the big unique words list (this is the number of documents with the unique word in it) and creates dict mapping word to IDF
    idf_dict = {}
    for unique_word in big_list:
        word_counter = 0
        for word_list in word_lists:
            if unique_word in word_list:
                word_counter += 1
        idf_dict[unique_word] = math.log10((len(text_files)) / (word_counter))

    return idf_dict


def get_tfidf(text_file, text_files):
    """
        Args:
            text_file: name of file in the form of a string (used to calculate TF)
            text_files: list of names of files, where each file name is a string
            (used to calculate IDF)
        Returns:
           a sorted list of tuples (in increasing TF-IDF score), where each tuple is
           of the form (word, TF-IDF). 

        * TF-IDF(i) = TF(i) * IDF(i)
        """
    tf_dict = get_tf(text_file)
    idf_dict = get_idf(text_files)

    # creates list of tuples (word, TF-IDF)
    tfidf_list = []
    for word in tf_dict:
        tf_idf = (word, tf_dict[word] * idf_dict[word])
        tfidf_list.append(tf_idf)

    tfidf_list.sort # sorts the tuples alphabetically (by the word)
    tfidf_list.sort(key = lambda x:x[1]) # sorts the alphabetically sorted tuple list by the second value (tfidf)

    return tfidf_list


if __name__ == "__main__":
    pass

    test_directory = "tests/student_tests/"
    hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    world, friend = prep_data(hello_world), prep_data(hello_friend)
    print(world) 
    print(friend) 

    world_word_freq = get_frequencies(world)
    friend_word_freq = get_frequencies(friend)
    print(world_word_freq) 
    print(friend_word_freq) 

    freq1 = get_letter_frequencies('hello')
    freq2 = get_letter_frequencies('that')
    print(freq1) 
    print(freq2) 

    word1_freq = get_letter_frequencies('toes')
    word2_freq = get_letter_frequencies('that')
    word3_freq = get_frequencies('nah')
    word_similarity1 = calculate_similarity_score(word1_freq, word1_freq)
    word_similarity2 = calculate_similarity_score(word1_freq, word2_freq)
    word_similarity3 = calculate_similarity_score(word1_freq, word3_freq)
    word_similarity4 = calculate_similarity_score(world_word_freq, friend_word_freq)
    print(word_similarity1) 
    print(word_similarity2) 
    print(word_similarity3) 
    print(word_similarity4) 

    freq1, freq2 = {"hello":5, "world":1}, {"hello":1, "world":5}
    most_frequent = get_most_frequent_words(freq1, freq2)
    print(most_frequent) 

    text_file = 'tests/student_tests/hello_world.txt'
    text_files = ['tests/student_tests/hello_world.txt', 'tests/student_tests/hello_friends.txt']
    tf = get_tf(text_file)
    idf = get_idf(text_files)
    tf_idf = get_tfidf(text_file, text_files)
    print(tf) 
    print(idf) 
    print(tf_idf) 