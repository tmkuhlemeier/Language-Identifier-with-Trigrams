#!/usr/bin/env python
# coding: utf-8

"""
Reads a directory of multilingual files and saves trigram frequency tables for later use.
"""

import os
from langdetect import trigram_table, write_trigrams

def make_profiles(datafolder, profilefolder, size) :
    """
    Void function which makes trigram tables of text in files in the provided datafolder and writes these tables to files in the
    provided profilefolder. 
    It opens the files to read in the correct encoding and calls the function write_trigrams from the module langdetect which 
    writes the trigrams in utf8 encoding.
    """
    
    if not os.path.exists(profilefolder) : # make directory if folder does not yet exist
        os.makedirs(profilefolder)
        
    for filename in os.listdir(datafolder) :
        if not filename.startswith(".") : # this way only correct files will be opened (hidden files start with ".")
            fname_parts = filename.split("-")
            language = fname_parts[0]
            f_encoding = fname_parts[1]
            
            conn = open(datafolder + "/" + filename, encoding = f_encoding) # open file in folder
            alltext = conn.read()
            conn.close()
            
            trigramtable = trigram_table(alltext, size) # make trigrams for this text
            profile_n = language + "." + str(size) # make filename for the profile           
            write_trigrams(trigramtable, profilefolder + "/" + profile_n) # write trigrams to the file

if __name__ == "__main__" : # conditional for stand alone program
    make_profiles("./datafiles/training", "./datafiles/trigram-models", 200)
