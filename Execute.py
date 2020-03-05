import numpy
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import json
import pickle
import os
import random
from firebase import firebase
import Train

model = Train.training()
firebase = firebase.FirebaseApplication('https://parkinglotbot-djokap.firebaseio.com/', None)

with open("intents.json") as file:
  data = json.load(file)

with open("data.pickle", "rb") as f:
  words, labels, training, output = pickle.load(f)

model.load("model/model.tflearn")

def bag_of_words(s, words):
  bag = [0 for _ in range(len(words))]
  s_words = nltk.word_tokenize(s)
  s_words = [stemmer.stem(word.lower()) for word in s_words]
  for se in s_words:
    for i, w in enumerate(words):
      if w == se:
        bag[i] = 1         
  return numpy.array(bag)

def get_name(inp):
  if len(inp) != 0:
    value = firebase.get('Details/', inp)
    return ("Hello "+ inp +", currently you have " + str(value) + " parking lots.")

def get_cluster(inp):
  if len(inp) != 0:
    return ("Your Cluster is "+ inp)

def chat(inp):
  context_set = ""
  results = model.predict([bag_of_words(inp, words)])
  results_index = numpy.argmax(results)
  tag = labels[results_index]
  for tg in data["intents"]:
    if tg['tag'] == tag:
      responses = tg['responses']
      response = (random.choice(responses))
      if len(tg['context_set']) != 0:
        context_set = tg['context_set']

  return str(response), context_set