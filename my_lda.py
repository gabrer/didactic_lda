#!/usr/bin/python

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import numpy
import string

from collections import defaultdict

from random import randint

import sys


################################################
def read_file( file_path ):

    text = ''

    with open(file_path, 'r') as myfile:
        text=myfile.read() #.replace('\n', '')

    return text
################################################




#############################
# DOCUMENTS
doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice. He is a good father."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle and blood pressure."


# compile documents
doc_complete = [doc1, doc2, doc3, doc4, doc5]



#############################
# Pre-processing
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete]   



#############################
# Build dictionary
def build_dictionary(documents):

    dictionary = set()

    for doc in documents:
        for token in doc:
            dictionary.add(token)

    # for word in dictionary:
    #     print "Word:",
    #     print word

    return dictionary
############################



############################
# List of all the words in the corpus
def list_of_all_words(documents):

    all_words = []

    for doc in documents:
        for token in doc:
            all_words.append(token)

    return all_words
############################



############################
# Counts how many times a word was assigned to a topic within the document.
def number_of_words_for_topic_in_document(meta_tokens, doc, topic):

    count = 0

     # Cycle over all the tokens in corpus
    for current_word in meta_tokens:

        # List of tokens: document and assigned topic
        tokens_of_word = meta_tokens[current_word]
        # Analyze single token
        for current_token in tokens_of_word:
            current_doc   = current_token[0]
            current_topic = current_token[1]

            if current_doc == doc and current_topic == topic:
                # print "Doc:",
                # print current_doc
                # print "Topic:",
                # print current_topic
                count += 1

    if count == 0:
        print "ERROR on counting how many times a word was assigned to a topic within the document."
        sys.exit(0)

    return count
############################



############################
# Number of times the current word have been assigned to the current topic
def count_curr_word_in_curr_topic(meta_tokens, current_word, topic):
   
    count = 0

    # List of tokens: document and assigned topic
    tokens_of_word = meta_tokens[current_word]
    # Analyze single token
    for current_token in tokens_of_word:
        current_topic = current_token[1]

        if current_topic == topic:
            print "Token in document:",
            print current_token[0], 
            print "topic:",
            print current_topic
            count += 1

    return count
############################



############################
# Number of words in each topic
def count_words_in_topic(meta_tokens):
   
    n_of_words_in_topic = [0] * n_of_topics

    for word in meta_tokens:
        # List of tokens: document and assigned topic
        tokens_of_word = meta_tokens[word]

        # Analyze single token
        for current_token in tokens_of_word:
            current_topic = current_token[1]
            n_of_words_in_topic[current_topic] += 1;

    return n_of_words_in_topic
############################





############################################################
# MAIN
############################################################
if __name__ == '__main__':


    ##############################
    # PARAMETERS
    ##############################
    n_of_topics = 3
    iterations = 2500
    alpha = [1.0/n_of_topics] * n_of_topics
    beta  = [1.0/n_of_topics] * n_of_topics

    #alpha = [50/n_of_topics] * n_of_topics
    #beta  = [0.01] * n_of_topics



    ##############################
    # INTERNAL VARIABLES
    ##############################
    # Count the number of words in each topic
    n_of_words_in_topic =  [0] * n_of_topics

    # List of all words in corpus
    words_in_corpus = []

    # Topic distribution
    topic_distribution = [0] * n_of_topics

    # Normalized topic distribution
    normalized_topic_distribution = [0] * n_of_topics


    # Build the dictionary
    dictionary = build_dictionary(doc_clean)
    dictionary_size = len(dictionary)



    ##############################
    # Random initialization of Z (i.e. assigned topics to words) and counters.
    ##############################
    meta_tokens = defaultdict(list)

    for word in dictionary:
        for doc in doc_clean:
            if word in doc:

                # Random topic choosing
                random_topic = randint(0, n_of_topics-1)

                # For each word, a list of tokens is made with the token's document and assigned topic.
                # E.g.:  [word] -> [doc1, topic3], [doc2, topic1], and so on.
                meta_tokens[word].append([doc_clean.index(doc), random_topic])

                # Increase the counter of the topic the word has been assigned to: n_k
                n_of_words_in_topic[random_topic] += 1

                print "\n\nWord: ",
                print word
                print "Topic:",
                print random_topic
                print "Document: " ,
                print doc
                print meta_tokens[word]



    # List of all the words within the corpus
    # words_in_corpus = list_of_all_words(doc_clean)

    # Print number of words in each topic after the random initialization
    for n in n_of_words_in_topic:
        print "Topic: ",
        print n


    ##############################
    # ITERATIONS
    ##############################
    for i in xrange(iterations):

        
        ##############################  
        # Cycle over all the tokens in corpus
        ##############################
        # Firste, it cycles over the dictionary words, and for eachone it analyzes the token
        for current_word in meta_tokens:
   
            # List of tokens: document and assigned topic
            tokens_of_word = meta_tokens[current_word]

            print "\n\n/////////////////////////////"
            print "Current word:",
            print current_word,
            print "\n\n/////////////////////////////"


            ##############################
            # Analyze single token
            for current_token in tokens_of_word:
                current_doc   = current_token[0]
                current_topic = current_token[1]


                print "\nCurrent document: ",
                print current_doc
                print "Current topic:",
                print current_topic



                ##############################
                # COUNTERS
                # (TODO: optimize them making a static structure instead of computing them every time)
                # Number of tokens in current document assigned to the current topic: n_(d,k)
                num_of_times_topic_in_doc           = number_of_words_for_topic_in_document(meta_tokens, current_doc, current_topic)

                # Number of times the current word was assigned to the current topic
                times_current_word_in_current_topic = count_curr_word_in_curr_topic(meta_tokens, current_word, current_topic)

                # Number of words in each topic
                n_of_words_in_topic = count_words_in_topic(meta_tokens)


                print "- Number of tokens in current document assigned to the current topic: ",
                print num_of_times_topic_in_doc

                print "- Number of times the current word have been assigned to current topic:",
                print times_current_word_in_current_topic


                # Decrement counters from the current instance
                num_of_times_topic_in_doc           -= 1
                times_current_word_in_current_topic -= 1
                n_of_words_in_topic[current_topic]  -= 1



                ##############################
                # Estimate "the probability of assigning the current word token to each topic" (Griffths p. 8)
                for t in xrange(n_of_topics):
                    
                    dt_numerator   = alpha[t] + num_of_times_topic_in_doc;
                    
                    tw_numerator   = beta[t]  + times_current_word_in_current_topic;
                    
                    tw_denominator = n_of_words_in_topic[t] + (beta[t] * dictionary_size)


                    topic_distribution[t] = dt_numerator * (tw_numerator / tw_denominator)
                    # print "Topic distribution for",
                    # print t,
                    # print "is",
                    # print topic_distribution[t]



                ##############################
                # Sample a new topic for current token
                normalized_topic_distribution = [i/sum(topic_distribution) for i in topic_distribution]
                print "Normalized topic distributions: "
                print normalized_topic_distribution

                sampled_topic = numpy.random.choice(numpy.arange(0, n_of_topics), p=normalized_topic_distribution)
                print "Sampled topic:",
                print sampled_topic 


                ##############################
                # Assigne the new topic to the token
                # Cycle the tokens for current word and update the assigned topic
                for i,t in enumerate(meta_tokens[current_word]):
                    if(t[0] == current_doc):
                        meta_tokens[current_word][i] = [current_doc, sampled_topic]


                ##############################
                # NB and TODO: use this code only with static structures for these counters.
                # Decrement counters from the current instance
                # num_of_times_topic_in_doc += 1
                # times_current_word_in_current_topic += 1
                # n_of_words_in_topic[sampled_topic] += 1


    print "\n\nEND of LDA"


    print "\nFinal normalized distrubtion: "
    print normalized_topic_distribution


    print "\n\nTopic composition:"
    for i in xrange(n_of_topics):
        print "\nCurrent topic -",
        print i
        
        # Cycle over all the tokens in corpus
        for current_word in meta_tokens:
            current_tokens = meta_tokens[current_word]
            # Analyze single token
            for token in current_tokens:
                current_doc   = token[0]
                current_topic = token[1]
                if(current_topic == i):
                    print current_word,
                    print current_doc





    # for key,values in word_dict.iteritems():
    #     print "%s: %s" % (key, values)
    #     print key



