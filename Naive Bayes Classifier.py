import nltk
import random
import pickle
from nltk.tokenize import word_tokenize
# I will be using the NLTK to assist me in building my naive bayes classifier
# import random will be used to shuffle my training and testing dataset of short movie reviews
# to make the classifier accurate and reliable when processing live tweets
# My dataset has already been labelled as positive and negative, making it possible to train and test with

# See the user guide for instructions on how to download the positive and negative.txt files for training and testing classifier.
# 2 two lines below open the text files and reads the text data contained within.
short_pos = open("positive.txt", "r").read()
short_neg = open("negative.txt", "r").read()

documents = []
# documents equals empty list

# r equals review, so for every review split them with a new line
for r in short_pos.split('\n'):
    documents.append((r, "pos"))

for r in short_neg.split('\n'):
    documents.append((r, "neg"))
random.shuffle(documents)

#This will mix up the positive and negative documents

all_words = []

#all words equals empty list
# The code below will tokenize the words in the positive and negative text files.

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)

for w in short_pos_words:
    all_words.append(w.lower())

for w in short_neg_words:
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)
# The line of code above will form a list of the most common words in the text files.

word_features = list(all_words.keys())[:5000]
# The above line of code records the most common 5000 words from both text files.

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

# The line of code below does this to all documents, saving the feature existence booleans and the positive or negative categories
featuresets = [(find_features(rev), category) for (rev, category) in documents]

random.shuffle(featuresets)
#This mixes up the positive and negative featuresets
# The below code follows the process of the supervised classification flow diagram that can be found on page ? of the user guide

# dataset I will train classifier with
training_set = featuresets[:10000]

# dataset I will test classifier against
testing_set = featuresets[10000:]

# The below code defines and trains my naive bayes classifier

classifier = nltk.NaiveBayesClassifier.train(training_set)

# The 3 lines of code below open the previously saved pickle file to run in the code
#classifier_f = open("naivebayes.pickle", "rb")
#classifier = pickle.load(classifier_f)
#classifier_f.close()

print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

# The 2 lines of code above give me a list of the 15 most informative words when the code is run and the accuracy of test data
# The code below allows me to save the naive bayes classifier process of running through the dataset
# By inserting import pickle at the top of the code, I can serialize the classifier and load it into my code, this saves time.

save_classifier = open("naivebayes.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

# The above 3 lines of code saved and stored the results of my code in a pickle file, to be accessed at any point in the future.
# Then I commented off the above code with the ‘#’ to allow me to carry out my next lines of code.
# which involved me uploading the saved data from the pickle file straight back into my code, See below for how it works.
# This opens up a pickle file, preparing to write in bytes some data.
# I used pickle.dump() to dump the data.
# The first parameter to pickle.dump() is what are you dumping.
# The second parameter is where are you dumping it.
# Close the file and now I have a pickle file saved.

# Reference for the code: https://pythonprogramming.net/naive-bayes-classifier-nltk-tutorial/