#!/usr/bin/env python
# coding: utf-8

"""
This script will apply the recognizer to two collections of test files, and measure and report the success of the recognition process.
"""

import os
from matchlang import LangMatcher

def eval(path) :
    """
    Tries to recognize the text in every file from the specified folder path and prints the guesses (with feedback if needed).
    Each time it has a file wrong, 'Error' will be printed at the specific line followed with the correct language.
    At the end, the total correct guesses and incorrect guesses from the folder will be printed.
    """
    
    abbrev = { "da" : "Danish", "de" : "German", "el" : "Greek",
           "en" : "English", "es" : "Spanish", "fi" : "Finnish", 
           "fr" : "French", "it" : "Italian", "nl" : "Dutch",
           "pt" : "Portuguese", "sv" : "Swedish"}
    n_corr = 0
    n_incorr = 0
    matcher = LangMatcher("./datafiles/trigram-models") # corrected path
    
    for filename in os.listdir(path) :
        if not filename.startswith(".") : # hidden filenames start with "."
            fname_parts = filename.split(".")
            f_language = abbrev[fname_parts[1]]
            profile_guess = matcher.recognize(path + "/" + filename)
            lang_guess = profile_guess[0]
            
            if lang_guess == f_language : # correct guess
                print(filename, lang_guess)
                n_corr += 1
            else : # incorrect guess
                print(filename, lang_guess, "Error", f_language)
                n_incorr += 1
                
    print(path, "correct:", n_corr, "incorrect:", n_incorr)

if __name__ == "__main__" : # if run from command line evaluate the three following folders
    eval("./datafiles/test-clean/europarl-90")
    eval("./datafiles/test-clean/europarl-30")
    eval("./datafiles/test-clean/europarl-10")
    
                
