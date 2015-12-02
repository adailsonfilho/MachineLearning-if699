import sys
from ticTacToe import *
from enum import Enum
from classifier import *
from random import randint
import ipdb
import numpy as np

##################
#### METHODS #####
##################

class PostKnnEstimation(Classifier):

	def __init__(self):
		##################
		#####  VARS ######
		##################
		self.p_learn_size = 0
		self.n_learn_size = 0
		self.data = [] 			#pre-processed data
		self.data_positive = [] 	#data splited for cross k-fold validation
		self.data_negative = []  #data splited for cross k-fold validation
		self.learn_data = []		#data var for lear sets of cross k-fold validation
		self.k = None			#"k" neighbors parameter

	def set_data(self, data):
			self.data = data

	#return the "k" nearest neighbors of the given "x"
	def k_neighbors(self, k,x):		

		distances = []
		for i,sample in enumerate(self.learn_data):
			d = dissimilarity(x, sample[0])
			# d = np.linalg.norm(np.array(x),np.array(sample[0]))
			distances.append({'index': i, 'distance': d})

		distances = sorted(distances, key=lambda e:e['distance'])

		return [e['index'] for e in distances[0:k]]

	def classify(self,sample):
		# sample = pre_process(sample, separator=',')
		kn = self.k_neighbors(self.k,sample)
		positive_votes = 0
		negative_votes = 0
		for i in kn:
			if self.learn_data[i][1] == ClassEnum.positive.value:
				positive_votes+=1
			elif self.learn_data[i][1] == ClassEnum.negative.value:
				negative_votes += 1
			else:
				raise "Ops!Some some problem to classify in the correct class"

		n_estimation = (negative_votes/self.n_learn_size)*(self.n_learn_size/len(self.learn_data))
		p_estimation = (positive_votes/self.p_learn_size)*(self.p_learn_size/len(self.learn_data))
		if n_estimation > p_estimation:
			return ClassEnum.negative.value
		else:
			return ClassEnum.positive.value

	def calculateRange(self,next_range, set_size, max_length, is_last_set):
		#calculate test positive range
			start = next_range
			end = next_range + set_size

			#if passed of the end of examples, correct
			if end >= max_length or is_last_set:
				end = max_length

			return {"begin":start,"end":end}

	def kFold_Cross_Validation(self, k):

		for sample in self.data:
			if sample[1] == ClassEnum.positive.value:
				self.data_positive.append(sample)
			elif sample[1] == ClassEnum.negative.value:
				self.data_negative.append(sample)

		print("> Cross K-Fold Validation")
		print()
		print("K = "+str(k))

		next_range_positive = 0
		max_length_positive = len(self.data_positive)

		next_range_negative = 0
		max_length_negative = len(self.data_negative)

		set_size_positive = int(max_length_positive/k)
		set_size_negative = int(max_length_negative/k)
		print("Positive set size = "+str(set_size_positive))
		print("Negative set size = "+str(set_size_negative))
		print()

		print("Positive max end value = "+str(max_length_positive))
		print("Negative max end value = "+str(max_length_negative))
		print()

		#separete sets
		positive_sets = []
		negative_sets = []

		#Begin Cross K-Fold Validation
		results = [] #tuplas (int corrects,int errors)

		#copy lists
		temp_data_positive = self.data_positive[:]
		temp_data_negative = self.data_negative[:]

		#criating data sub sets for cross k-fold validation
		for set_index in range(0,k):

			# print("creating positive set index "+str(set_index))
			
			#initiate list
			positive_sets.append([])

			#calculate range to 
			positive_range = self.calculateRange(next_range_positive, set_size_positive, max_length_positive, set_index == k-1)

			#save set
			for i in range(positive_range['begin'],positive_range['end']):
				# print("-- "+str(positive_range))
				nextItem = randint(0,len(temp_data_positive)-1)
				positive_sets[set_index].append(temp_data_positive[nextItem])
				#Remove element from index "nextItem"
				del temp_data_positive[nextItem]
				#update new range begin
				next_range_positive = positive_range['end']

			# print("Created: "+str(len(positive_sets[set_index]))+" samples")
			
			# print("creating negative set index "+str(set_index))
			#initiate list
			negative_sets.append([])

			#calculate range
			negative_range = self.calculateRange(next_range_negative, set_size_negative,max_length_negative, set_index == k-1)
			#save set
			for i in range(negative_range['begin'],negative_range['end']):
				# print("-- "+str(negative_range))
				nextItem = randint(0,len(temp_data_negative)-1)
				negative_sets[set_index].append(temp_data_negative[nextItem])
				#Remove element from index "nextItem"
				del temp_data_negative[nextItem]
				#update new range begin
				next_range_negative = negative_range['end']

			# print("Created: "+str(len(positive_sets[set_index]))+" samples")

			#copy lists
			temp_data_positive = self.data_positive[:]
			temp_data_negative = self.data_negative[:]

			#end for: creating sets

		all_corrects = 0
		all_wrongs = 0

		#test loop
		for index_test in range(0,k):

			#write in the same line
			sys.stdout.write("\rTesting Progress: "+str(((index_test/k)*100))+"%")
			sys.stdout.flush()

			errors_positive = 0
			errors_negative = 0

			#zera apontador de listas de aprendizado
			self.learn_data = []

			#a quantidade de conjuntos de classe eh igual apesar da diferença existir
			data_positive_test = positive_sets[index_test]
			data_negative_test = negative_sets[index_test]

			# print("-----------------------------------------------")
			# print(">> TESTING:")
			# print("Positive Set "+str(index_test)+", size: "+str(len(data_positive_test)))

			#cria lista de dados para aprendizagem com os sub-conjuntos que não sao de test
			self.p_learn_size = 0
			self.n_learn_size = 0
			for i in range(0,k):
				if i != index_test:
					self.learn_data += positive_sets[i]
					self.p_learn_size += len(positive_sets[i])

					self.learn_data += negative_sets[i]
					self.n_learn_size += len(negative_sets[i])

			samples_p = 0
			for p in data_positive_test:
				answer = self.classify(p[0])
				if answer != ClassEnum.positive.value:
					errors_positive += 1
				samples_p += 1

			# print(" -> Correct: "+str(((samples_p-errors_positive)/samples_p)*100)+"%")
			# print()

			# print("Negative Set "+str(index_test)+", size: "+str(len(data_negative_test)))
			samples_n = 0

			for n in data_negative_test:
				answer = self.classify(n[0])
				if answer != ClassEnum.negative.value:
					errors_negative += 1
				samples_n += 1

			# print(" -> Correct: "+str(((samples_n-errors_negative)/samples_n)*100)+"%")


			all_corrects += (samples_p-errors_positive) + (samples_n-errors_negative)
			all_wrongs += errors_positive + errors_negative
			# print()
			# print("Correct for all classes in test "+str(index_test)+" : "+str(((samples_n-errors_negative+samples_p-errors_positive)/(samples_n+samples_p))*100)+"%")
			# print("-----------------------------------------------")

			#fim do for

		sys.stdout.write("\rTesting Progress"+str(((index_test/k)*100))+"%")
		sys.stdout.flush()

		print()
		print()
		print("FINAL REPORT")
		print("Avarage of correct answers: "+str((all_corrects)/(all_wrongs+all_corrects)*100)+"%")
		print("-----------------------------------------------")