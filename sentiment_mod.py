import random
import pickle
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

# import random will be used to shuffle my training and testing dataset of short movie reviews
# to make the classifier accurate and reliable when processing live tweets
# My dataset has already been labelled as positive and negative, making it possible to train and test with
# import pickle will insert my previously saved and serialised file of my naive bayes classifier and most common 5000 words
# word_tokenize will tokenizes the dataset, separating each word from the body of text as tokens

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

# The 3 lines of code below are simply opening the pickle file of the documents, I created in the last piece of code.

documents_f = open("documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()
# The 3 lines of code below are simply opening the pickle file of the word features, I created in the last piece of code.

word_features5k_f = open("word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

# The lines of code below are creating a function (def)  to tokenize the words contained within the document
def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

# The line of code below does this to all documents, saving the feature existence booleans and the positive or negative categories
featuresets = [(find_features(rev), category) for (rev, category) in documents]

#This mixes up the positive and negative featuresets
random.shuffle(featuresets)

print(len(featuresets))
# The line of code above prints the length of the dataset (total number of positive and negative datasets)

# dataset I will test classifier against
testing_set = featuresets[10000:]

# dataset I will train classifier with
training_set = featuresets[:10000]

# The 3 lines of code below are opening the pickle file of the naive bayes classifier
# The pickle file has saved the classifier, this reduces the run time of the program especially if being used on large dataset

open_file = open("originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()

voted_classifier = VoteClassifier(
    classifier)

# The last piece of code is the most important piece of code for the next python files
# The function called 'sentiment' is created and takes the text, analyses the features of the text using find_features and returns the sentiment (positive or negative)

def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)

# Reference for the code used: https://pythonprogramming.net/sentiment-analysis-module-nltk-tutorial/