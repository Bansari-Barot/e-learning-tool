import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import gensim
from gensim import corpora
from nltk.tokenize import word_tokenize
from decimal import Decimal

class SentenceSimilarityHandler():
    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
    embed = hub.Module(module_url)
    similarityValue =0.00
    percentCorrectness = 0.00
    plotSimilarityValue = 0.00
    def validate(messages):
        similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
        similarity_message_encodings = SentenceSimilarityHandler.embed(similarity_input_placeholder)
        with tf.Session() as session:
                session.run(tf.global_variables_initializer())
                session.run(tf.tables_initializer())
                percentCorrectness = SentenceSimilarityHandler.run_and_plot(session, similarity_input_placeholder, messages,
                        similarity_message_encodings)
                print("plotSimilarityValue",SentenceSimilarityHandler.plotSimilarityValue)
        comparisonResult = SentenceSimilarityHandler.gensimImpl(messages)
        print('Value from gensim & nltk', comparisonResult)
        sentenceSimilarityValue = (((0.33333) *percentCorrectness) + ((0.66666)*(comparisonResult)))
        SentenceSimilarityHandler.similarityValue = (round(sentenceSimilarityValue,2))
        print('The similarity value between the sentences are', SentenceSimilarityHandler.similarityValue)
        return SentenceSimilarityHandler.similarityValue

    def plot_similarity(labels, features, rotation):
        print("Plotting similarity matrix")
        corr = np.inner(features, features)
        sns.set(font_scale=1.2)
        g = sns.heatmap(
        corr,
        xticklabels=labels,
        yticklabels=labels,
        vmin=0,
        vmax=1,
        cmap="YlOrRd")
        g.set_xticklabels(labels, rotation=rotation)
        g.set_title("Semantic Textual Similarity")
        SentenceSimilarityHandler.percentCorrectness = corr[0][1]
        print('Value from tensorflow', SentenceSimilarityHandler.percentCorrectness)
        return SentenceSimilarityHandler.percentCorrectness

    def gensimImpl(messages):
        raw_documents = [messages[0],"Process is a series of actions or steps taken in order to achieve a particular end.","A process is a series of steps undertaken to achieve a desired outcome or goal.","Series of actions in specific order is called process"]
        gen_docs = [[w.lower() for w in word_tokenize(text)]
            for text in raw_documents]
        dictionary = gensim.corpora.Dictionary(gen_docs)
        corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
        tf_idf = gensim.models.TfidfModel(corpus)
        s = 0
        for i in corpus:
                s += len(i)
        sims = gensim.similarities.Similarity('/Users/onlinecampus/Documents/Karthik/SemanticEncoder/USC/Similarity/sims',tf_idf[corpus],
                                                num_features=len(dictionary))

        query_doc = [w.lower() for w in word_tokenize(messages[1])]
        query_doc_bow = dictionary.doc2bow(query_doc)
        query_doc_tf_idf = tf_idf[query_doc_bow]
        comparisonResult = sims[query_doc_tf_idf][0]
        #print('Comparison result', comparisonResult)
        return comparisonResult
    def run_and_plot(session_, input_tensor_, messages_, encoding_tensor):
        message_embeddings_ = session_.run(
        encoding_tensor, feed_dict={input_tensor_: messages_})
        plotSimilarityValue = SentenceSimilarityHandler.plot_similarity(messages_, message_embeddings_, 90)
        return plotSimilarityValue
