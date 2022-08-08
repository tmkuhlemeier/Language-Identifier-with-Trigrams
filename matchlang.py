#!/usr/bin/env python
# coding: utf-8

"""
The language recognizer. This is a general-purpose program with command-line arguments and options. It can also be imported as a module, allowing the recognizer to be used by another program.
"""

import os, langdetect, write_profiles, sys, optparse
from langdetect import read_trigrams, trigram_table, cosine_similarity

class LangMatcher :
    """ 
    This is a class for calculating the best language matches to a given text.
      
    Attributes: 
        path (string): The path to the folder with the saved trigramtables
    """
    
    def __init__(self, path) :
        """ 
        The constructor for LangMatcher class. 
  
        Parameters: 
            path (string): The path to the folder with the saved trigramtables
        """
        
        self.langprofiles = dict()
            
        # make dictionary of dictionaries (languages as keys for all files, 
        # trigramtables(dictionaries) as values of those languages)
        for filename in os.listdir(path) : 
            if not filename.startswith(".") : # hidden files start with "."
                fname_parts = filename.split(".")
                language = fname_parts[0]
                trigramtable = read_trigrams( path + "/" + filename)
                self.langprofiles[language] = trigramtable # add to the dictionary
            
    def score(self, text, n = 1, ngrams = 200) :
        """ 
        The function to determine the best language matches for a specified text. 
  
        Parameters: 
            text (string): The text to be matched.
            n (int): The number of bestmatches to be returned.
            ngrams (int): The (maximum) length of the trigram table of the text.
          
        Returns: 
            list: A list of tuples (language, cosine similarity) 
        """
        
        ngramtable = trigram_table(text, ngrams)
        cosines = dict()
        
        # make a dictionary of cosines with all languages
        for key in self.langprofiles.keys() :
            cosines[key] = cosine_similarity(self.langprofiles[key], ngramtable)
            
        cosines_copy = cosines.copy() # make copy so the original stays intact
        bestmatches = []
        
        # make a list of the n languages with the highest cosines
        for num in range(n) :
            bestmatch = max(cosines_copy, key = lambda x : cosines_copy[x])
            bestmatches.append((bestmatch, cosines_copy.pop(bestmatch, None)))          
            # every time a bestmatch (language) is found append the language and value 
            # (use pop so the bestmatch gets deleted from the cosines dictionary and a new bestmatch can be assigned)
            
        return bestmatches

    def recognize(self, filename, file_encoding = "utf-8", ngrams = 200) :
        """Opens the specified file and returns tuple of the best match."""
        
        conn = open(filename, encoding = file_encoding)
        alltext = conn.read()
        conn.close()
        match = self.score(alltext, 1, ngrams)[0]
        return match
    
if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-e", action = "store", type = "string", dest = "f_encoding", default = "utf-8",
              help = "specify encoding for test files")
    
    (options, args) = parser.parse_args()
    
    if len(args) < 1: # print an error message if no files are given as an argument
        sys.stderr.write("Syntax: python matchlang.py requires filename [...]\n")
        sys.exit(2)  # Exit with error status 2
        
    path = "./datafiles/trigram-models"
    
    if not os.path.exists(path) : # if the path does not yet exist write profiles
            write_profiles.make_profiles("./training", path , 200)
            
    files = args[0:]
    matcher = LangMatcher(path)
    
    for fname in files : # recognize all files that are given and print information
        langmatch = matcher.recognize(fname, options.f_encoding)
        print("Language:", langmatch[0] + ", cosine similarity:", langmatch[1])
        