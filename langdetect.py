#!/usr/bin/env python
# coding: utf-8

"""
Core functionality module. This module defines some important core functions, and useful helper functions.
"""

import re, math, collections

def prepare(text):
    """
    Takes a string, replaces the characters ",.?!<>() with spaces and returns the resulting list of words.
    """
    
    newstring = re.sub('[!?",.()<>]'," ", text) # make a clean string by substituting
    wordlist = newstring.split()
    return wordlist

def trigrams(seq):
    """Takes any sequence (e.g., a string) and returns a list of its trigrams."""
    
    trigrams = []
    n = 0
    while n < len(seq) - 2: # while there are at leat 3 symbols left in the sequence
        trigrams.append(seq[n:n+3]) # append sequence of 3 symbols to the list
        n = n + 1 # move to the next symbol
    return trigrams

def trigram_table(text, limit = 0): 
    """
    Creates a table of trigram frequencies as a dictionary.
    
    Parameters:
    arg1 (string): Text
    arg2 (int): Optional argument which specifies the maximum length of the table. Default value 0 returns the whole dict.
    
    Returns:
    dictionary: Table of trigrams whose keys are ngrams and the values are frequencies (ngram counts).
    
    """
    
    trigramlist = []
    tokenlist = prepare(text)
    for word in tokenlist: # add brackets and extend the trigramlist with the trigrams in that word
        word_new = "<" + word + ">"
        trigramlist.extend(trigrams(word_new))
    frequencies = collections.Counter(trigramlist) #count the frequency of every trigram in the list
    if limit == 0:
        return dict(frequencies) # cast to dictionary
    else:
        return dict(frequencies.most_common(limit)) # return a list of (limit) most common frequencies

def write_trigrams(table, filename) :
    """Opens (or creates) a file and writes the ngrams from a table to that file in utf8 encoding."""
    
    outfile = open(filename, "w", encoding= "utf-8")
    # take the keys and values of the dictionary items sorted by the values, from high frequency to low
    for key, value in sorted(table.items(), key = lambda x : x[1], reverse = True) :
        outfile.write(str(value) + " " + key + "\n") 
    outfile.close()

def read_trigrams(filename) :
    """
    Reads the file created by write_trigrams and converts the contents to dictionary with integers as values and returns this.
    
    """
    
    conn = open(filename, encoding = "utf-8")
    alltext = conn.read()
    conn.close() 
    words = alltext.split() # make a list of words
    frequencies = dict()
    n = 0
    while n < len(words) - 1 :
        # words with uneven indices to keys (trigrams), 
        # words with even indices to values (frequencies)
        frequencies[words[n + 1]] = int(words[n]) 
        n = n + 2 # move to next "line"
    return frequencies

def even_dictionary(dict1, dict2) :
    """ 
    Help function to add missing keys(trigrams) of a dictionary (cf. another dictionary) with value 0(zero frequency). This way
    the trigram tables can 'become even' in regards to the trigrams they contain, which makes it possible to compare them later.
    """
    
    dict1_copy = dict1.copy() # make a copy so the original stays intact
    for key in dict2.keys() : # if it is not in the first dictionary, add the key with value 0
        if not key in dict1_copy :
            dict1_copy[key] = 0
    return dict1_copy #return the modified copy

def make_vector(dict1) :
    """Help function to make a vector. It converts the trigramtables to a sorted list and returns this."""
    
    vector = []
    #  make a list of frequencies 
    # (sorted on the keys/ trigrams(alphabetically))
    for key in sorted(dict1.keys()) :
        value = dict1[key]
        vector.append(value)
    return vector

def calc_magnitude(some_vector) :
    """Help function to calculate and return magnitude for vector."""
    
    magsum = 0
    for num in some_vector : # magsum is the sum of all elements squared of the vector
        magsum += float(num ** 2)
    magnitude = float(math.sqrt(magsum)) # magnitude is the square root of the magnitude
    return magnitude

def cosine_similarity(known, unknown) : 
    """
    Calculates and returns cosine similarity between trigram tables of a known language and a yet unknown language.
    """
    
    table1 = even_dictionary(known, unknown) # table 1 is the modified known dictionary
    table2 = even_dictionary(unknown, known) # table 2 is the modified unknown dictionary
    vector1 = make_vector(table1)
    vector2 = make_vector(table2)
    dotproduct = 0
    
    # multiply value of indices of both vectors and summarize to get the dotproduct
    for num in range(len(vector1) - 1) :
        dotproduct += float(vector1[num] * vector2[num])
    cosine_sim = float(dotproduct / (calc_magnitude(vector1) * calc_magnitude(vector2)))
    
    return cosine_sim



