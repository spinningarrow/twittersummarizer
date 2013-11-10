import re, math, collections, itertools, os, sys, pickle
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.collocations import BigramCollocationFinder

RT_POLARITY_POS_FILE = 'positive.txt'
RT_POLARITY_NEG_FILE = 'negative.txt'
TWEETS_FILE = 'SampleSet3.txt'

def create_word_scores():
	#creates lists of all positive and negative words
	positiveWords = []
	negativeWords = []
	with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
		for i in posSentences:
			positiveWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			positiveWords.append(positiveWord)
	with open(RT_POLARITY_NEG_FILE, 'r') as negSentences:
		for i in negSentences:
			negativeWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			negativeWords.append(negativeWord)
	positiveWords = list(itertools.chain( * positiveWords))
	negativeWords = list(itertools.chain( * negativeWords))

	#build frequency distibution of all words and then frequency distributions of words within positive and negative labels
	word_frequency_distribution = FreqDist()
	cond_word_frequency_distribution = ConditionalFreqDist()
	for word in positiveWords:
		word_frequency_distribution.inc(word.lower())
		cond_word_frequency_distribution['pos'].inc(word.lower())
	for word in negativeWords:
		word_frequency_distribution.inc(word.lower())
		cond_word_frequency_distribution['neg'].inc(word.lower())

	#finds the number of positive and negative words, as well as the total number of words
	positive_word_count = cond_word_frequency_distribution['pos'].N()
	negative_word_count = cond_word_frequency_distribution['neg'].N()
	total_word_count = positive_word_count + negative_word_count

	#builds dictionary of word scores based on chi-squared test
	word_scores = {}
	for word, frequency in word_frequency_distribution.iteritems():
		positive_score = BigramAssocMeasures.chi_sq(cond_word_frequency_distribution['pos'][word], (frequency, positive_word_count), total_word_count)
		negative_score = BigramAssocMeasures.chi_sq(cond_word_frequency_distribution['neg'][word], (frequency, negative_word_count), total_word_count)
		word_scores[word] = positive_score + negative_score

	return word_scores

#finds word scores


#finds the best 'number' words based on word scores
def find_best_words(word_scores):
	best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)
	best_words = set([w for w, s in best_vals])
	return best_words

#creates feature selection mechanism that only uses best words
def best_word_features(words):
	return dict([(word, True) for word in words if word in best_words])


def best_bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    d = dict([(bigram, True) for bigram in bigrams])
    d.update(best_word_features(words))
    return d

def buildTrainingSet():
	posFeatures = []
	negFeatures = []
	#http://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation
	#breaks up the sentences into lists of individual words (as selected by the input mechanism) and appends 'pos' or 'neg' after each list
	with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
		for line in posSentences:
			i = line.lower()
			positiveWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			positiveWords = [feature_select(positiveWords), 'positive']
			posFeatures.append(positiveWords)
	with open(RT_POLARITY_NEG_FILE, 'r') as negSentences:
		for line in negSentences:
			i = line.lower()
			negativeWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			negativeWords = [feature_select(negativeWords), 'negative']
			negFeatures.append(negativeWords)

	#selects 3/4 of the features to be used for training and 1/4 to be used for testing
	trainFeatures = posFeatures + negFeatures
	return trainFeatures


def classifyTweet (classifier, feature_select, tweet):
	tweet = tweet.lower()
	words = re.findall(r"[\w']+|[.,!?;]", tweet.rstrip())
	words = feature_select(words)
	return classifier.classify(words)

word_scores = 0
feature_select = 0
best_words = 0
train_features = 0
classifier = 0
def getClassifiedDictionary (sentences):
	global word_scores, feature_select, best_words, train_features, classifier
	word_scores = create_word_scores()
	feature_select = best_bigram_word_feats
	best_words = find_best_words(word_scores)
	train_features = buildTrainingSet()
	classifier = nltk.NaiveBayesClassifier.train(train_features)
	classified_dict = {}
	negative = []
	positive = []
	classified_dict["negative"] = negative
	classified_dict["positive"] = positive
	for line in sentences:
		tweet = line.lower()
		words = re.findall(r"[\w']+|[.,!?;]", tweet.rstrip())
		words = feature_select(words)
		classified_dict[classifier.classify(words)].append(line)

	return classified_dict

def serializeClassifier ():
	global classifier
	w = open('classifier','w')
	w.write(pickle.dumps(classifier))
	return "done"

def deserializeClassifier ():
	global word_scores, feature_select, best_words, train_features, classifier
	word_scores = create_word_scores()
	feature_select = best_bigram_word_feats
	best_words = find_best_words(word_scores)
	train_features = buildTrainingSet()
	with open('classifier', 'r') as file:
		content = file.read()
		classifier = pickle.loads(content)
		sentence = "i am sad"
		words = re.findall(r"[\w']+|[.,!?;]", sentence.rstrip())
		words = feature_select(words)
		print classifier.classify(words)

def classify (sentences):
	global word_scores, feature_select, best_words, train_features, classifier
	word_scores = create_word_scores()
	feature_select = best_bigram_word_feats
	best_words = find_best_words(word_scores)
	train_features = buildTrainingSet()
	classified_dict = {}
	negative = []
	positive = []
	with open('classifier', 'r') as file:
		content = file.read()
		classifier = pickle.loads(content)
		classified_dict["negative"] = negative
		classified_dict["positive"] = positive
		for line in sentences:
			tweet = line.lower()
			words = re.findall(r"[\w']+|[.,!?;]", sentences.rstrip())
			words = feature_select(words)
			classified_dict[classifier.classify(words)].append(line)

	return classified_dict

# if sys.argv[1]:
# 	print(classifyTweet(classifier, feature_select, str(sys.argv[1]).lower()))

# with open(TWEETS_FILE, 'r') as tweets:
# 	sentences = []
# 	for line in tweets:
# 		sentences.append(line)

# print getClassifiedDictionary(["this is lame", "This is brilliant"])