# freq-dist.py
#
# Developer: Luke Rasmussen
# Purpose: Given an input directory containing txt files, calculate the
#          word frequency distribution and write out a CSV containing
#          the file, word, and count for the top 50 results.
#
# Parts of this example are derived from:
# https://towardsdatascience.com/introduction-to-clinical-natural-language-processing-predicting-hospital-readmission-with-1736d52bc709
import sys
import fileinput
import os
import csv
import nltk
from nltk import word_tokenize
from datetime import datetime

if (len(sys.argv) < 3):
  print "Usage: nltk-freq-dist input-dir output-dir"
  sys.exit(1)

print "Input dir : ", sys.argv[1]

# This is code adapted to our Docker image.
# The parameters we get are relative directories.  When the container is run,
# it will have /tmp mapped to the root folder where the input and output
# folders live on the user's machine.
input_dir = os.path.join("/tmp", sys.argv[1])
output_dir = os.path.join("/tmp", sys.argv[2])
print "Input from : ", input_dir
print "Output to : ", output_dir

# Load our custom stopwords.  They really aren't magical, but we'll pretend
# that they are for this example.  Note that we've built the stop words into
# the image because we always want it to be the same list.  That avoids the
# chance someone changes the list.  Maybe we want to update the list in the
# future - if so, we can always create a new version of our image.
stop_words_file = open("./config/stop_words.txt", "r")
stop_words = stop_words_file.read().splitlines()
stop_words_file.close()

with open(os.path.join(output_dir, 'results.csv'), 'wb') as csvfile:
  results_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
  for filename in os.listdir(input_dir):
    if not filename.endswith(".txt"):
      continue

    # The file ID is the name of the file minus the extension
    file_id = filename.replace(".txt", "")

    input_file_path = os.path.join(input_dir, filename)
    print "Processing... ", input_file_path

    # Read in the file contents and tokenize the file
    text_file = open(input_file_path)
    word_tokens = word_tokenize(text_file.read().lower())
    text_file.close()

    # Filter out stopwords and short (1 character) tokens
    words = [word for word in word_tokens if ((not word in stop_words) and (len(word) > 1))]

    # Calculate frequency distribution and write to output CSV
    fdist = nltk.FreqDist(words)
    for word, frequency in fdist.most_common(50):
      results_writer.writerow([file_id, word, frequency])
