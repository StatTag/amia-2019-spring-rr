# This example is derived in part from:
# https://towardsdatascience.com/introduction-to-clinical-natural-language-processing-predicting-hospital-readmission-with-1736d52bc709
# This includes parts of the code, as well as the list of stop words chosen

import nltk
from nltk import word_tokenize

stop_words_file = open("./config/stop_words.txt", "r")
stop_words = stop_words_file.read().splitlines()
stop_words_file.close()

word_tokens = word_tokenize('Patient presents with shortness of breath and an elevated blood pressure of 190/100.')
filtered_sentence = [word for word in word_tokens if not word in stop_words]

print filtered_sentence