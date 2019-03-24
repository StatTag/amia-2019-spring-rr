# This example is derived in part from:
# https://towardsdatascience.com/introduction-to-clinical-natural-language-processing-predicting-hospital-readmission-with-1736d52bc709

import sys
import fileinput
import os
import csv
import nltk
from nltk import word_tokenize

if (len(sys.argv) < 3):
  print "Usage: nltk-freq-dist input-dir/ output-dir/"
  sys.exit(1)

print "Input dir : ", sys.argv[1]

input_dir = os.path.join("/tmp", sys.argv[1])
output_dir = os.path.join("/tmp", sys.argv[2])
print "Input from : ", input_dir
print "Output to : ", output_dir

# Load our custom stopwords (they aren't great, it's just to prove a point...)
stop_words_file = open("./config/stop_words.txt", "r")
stop_words = stop_words_file.read().splitlines()
stop_words_file.close()

with open(os.path.join(output_dir, 'results.csv'), 'wb') as csvfile:
  results_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
  for filename in os.listdir(input_dir):
    if not filename.endswith(".txt"):
      continue

    record_id = filename.replace(".txt", "")
    input_file_path = os.path.join(input_dir, filename)
    text_file = open(input_file_path)
    print "Processing... ", input_file_path
    # Read in the file contents and tokenize the file
    word_tokens = word_tokenize(text_file.read().lower())
    text_file.close()
    # Filter out stopwords and short (1 character) tokens
    words = [word for word in word_tokens if ((not word in stop_words) and (len(word) > 1))]
    # Calculate frequency distribution and write to output CSV
    fdist = nltk.FreqDist(words)
    for word, frequency in fdist.most_common(50):
      results_writer.writerow([record_id, word, frequency])
