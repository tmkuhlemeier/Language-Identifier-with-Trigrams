When matching.py is called in the command we make trigram-models folder if it does not yet exist with the profiles in it.
For the rest, write_profiles must be run before running anything else (like evaluate).

Also, we were not sure about the number of correct guesses in evaluate, we got 21 correct for europarl-10 whilst friends of us got 22 correct. (For one exception all the cosines are the same.)

Also the location of training and test-clean and trigram-profiles was not completely clear. In one part of the assignment it said in datafiles and in the other in the current file. We have followed the example of write_profiles and put them in datafiles.

Final Grade: 10 out of 10