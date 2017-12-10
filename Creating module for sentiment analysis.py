import nltk
import random
import pickle
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

# import nltk gives me access to the nltk libraries of data and programs for data analysis
# import random will be used to shuffle my training and testing dataset of short movie reviews
# to make the classifier accurate and reliable when processing live tweets
# My dataset has already been labelled as positive and negative, making it possible to train and test with
# import pickle will insert my previously saved and serialised file of my naive bayes classifier and most common 5000 words
# word_tokenize will tokenizes the dataset, separating each word from the body of text as tokens
# I imported mode, this will choose the most popular classifier vote (this code was used when I had more classifiers in the code)
# Line classifierI is the classifier being used on the data

# The class below is for my classifier
# The classifier is called VoteClassifier and is inherting ClassifierI
# The classifiers well in this case the naive bayes classifier is programmed to pass through the class to self.classifier
# In the second function 'def classify' I define my classify process, so I can call on it later on.
# The functions below are passing through the classifier and classifying by features
# The classification is being processed as a vote (was more effective when I had more classifiers)
# Finally the class returns the the mode(vote), the most popular classifier (again better when you have more classifiers)


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

# confidence function is simply counting up the votes for each classifiers (again working better when you use more classifiers)

# See the user guide for instructions on how to download the positive and negative.txt files for training and testing classifier.
# 2 two lines below open the text files and reads the text data contained within.
short_pos = open("positive.txt", "r").read()
short_neg = open("negative.txt", "r").read()

all_words = []
documents = []
# all_words equals empty list
# documents equals empty list

#  j is adjective, r is adverb, and v is verb
# allowed_word_types = ["J","R","V"]
allowed_word_types = ["J"]

# I am only looking for adjectives in the dataset

for p in short_pos.split('\n'):
    documents.append((p, "pos"))
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())
# The above if statement is saying if the word is an adjective I want to append that word

for p in short_neg.split('\n'):
    documents.append((p, "neg"))
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

# The above if statement is saying if the word is an adjective I want to append that word
# Below I am saving the words in a pickle file

save_documents = open("documents.pickle", "wb")
pickle.dump(documents, save_documents)
save_documents.close()
# The above 3 lines of code saved and stored the results of my code in a pickle file, to be accessed at any point in the future.

all_words = nltk.FreqDist(all_words)
# The line of code above will form a list of the most common words in the text files.

word_features = list(all_words.keys())[:5000]
# The above line of code records the most common 5000 words from both text files.

save_word_features = open("word_features5k.pickle", "wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()

# The above 3 lines of code saved and stored the results of my code in a pickle file, to be accessed at any point in the future.

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

print(len(featuresets))
# The line of code above prints the length of the dataset (total number of positive and negative datasets)

# dataset I will test classifier against
testing_set = featuresets[10000:]

# dataset I will train classifier with
training_set = featuresets[:10000]


classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(15)

# The above lines of code will print the percentage accuracy of the naive bayes classifier and the 15 most common words

save_classifier = open("originalnaivebayes5k.pickle", "wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

# The above 3 lines of code saved and stored the results of my code in a pickle file, to be accessed at any point in the future.
# 'open' create a new pickle file
# 'wb' means write in bytes
# I used pickle.dump() to dump the data.
# The first parameter to pickle.dump() is what are you dumping.
# The second parameter is where are you dumping it.
# Close the file and now I have a pickle file saved.

# Reference for code used: https://pythonprogramming.net/sentiment-analysis-module-nltk-tutorial/