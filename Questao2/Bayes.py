import os
import sys
from decimal import *
from random import randint
from ticTacToe import *
from classifier import *

#limpa tela
clear = lambda: os.system('cls') #to clear screen during use of console in windows

getcontext().prec += 10

class Bayes(Classifier):
	def __init__(self):

		self.total_positive = 0
		self.total_negative = 0

		#All data raded from files after pre-process
		self.data_positive = []
		self.data_negative = []

		#data for learning after
		self.data_positive_learn = []
		self.data_negative_learn = []

	def set_data(self, w1,w2):
		self.data_positive = w1
		self.data_negative = w2

	def priori(self, classId):
		if classId == ClassEnum.negative.value:
			return Decimal(len(self.data_negative_learn))/Decimal(len(self.data_negative_learn) + len(self.data_positive_learn))
		elif classId == ClassEnum.positive.value:
			return Decimal(len(self.data_positive_learn))/Decimal(len(self.data_negative_learn) + len(self.data_positive_learn))

	def posteriori(self, classId, features):
		#Parte superior da fração |   P(x|ωl)P(ωl)
		dividend = Decimal(self.conditionalDensity(features,classId))*Decimal(self.priori(classId))

		#Divisor
		sumAcc = Decimal(self.conditionalDensity(features, ClassEnum.positive.value))*Decimal(self.priori(ClassEnum.positive.value))
		sumAcc += Decimal(self.conditionalDensity(features, ClassEnum.negative.value))*Decimal(self.priori(ClassEnum.negative.value))

		return dividend/sumAcc		

	def conditionalDensity(self, features, classId):
		dataSource = None
		if classId == ClassEnum.negative.value:
			dataSource = self.data_negative_learn
		elif classId == ClassEnum.positive.value:
			dataSource = self.data_positive_learn

		#TODO(Adailson): CALCULAR PRODUTÓRIO AQUI! (acho que é possivel otimizar os laços calculando pij,qij e rij em um unico laço visto que o j é igual para ambos toda vez que este produtorio rodar um laço)
		productAcc = 1
		i = 0;
		for xi in features:

			if xi == 1:
				exp_p = (Decimal(xi*(xi +1))/Decimal(2))
				productAcc*= Decimal(self.pij(i,classId))**exp_p
			elif xi == 0:
				exp_q = (Decimal(1)-Decimal(xi**2))
				productAcc*= Decimal(self.qij(i,classId))**exp_q
			elif xi == -1:
				r_exp = Decimal(xi*(xi -1))/Decimal(2)
				productAcc *= Decimal(self.rij(i,classId))**r_exp				
			else:
				raise "Error in discrete pre-process."

			i +=1

		return productAcc

	#probabilidade condicional  pij = P(xi = 1|ωj ) -> 'x'
	def pij(self, i, classId):
		dataSource = None
		total_datasource = None
		if classId == ClassEnum.negative.value:
			total_datasource = len(self.data_negative_learn)
			dataSource = self.data_negative_learn

		elif classId == ClassEnum.positive.value:
			total_datasource = len(self.data_positive_learn)
			dataSource = self.data_positive_learn

		sumAcc = Decimal(0) #acumulador de soma
		for example in dataSource:
			xi = example[0][i]
			sumAcc += Decimal(xi*(xi+1))/Decimal(2)

		sumAcc *= Decimal(1)/Decimal(total_datasource) #equivale a 1/nj da formula desta questao
		# print('prod pij = '+str(sumAcc))
		return sumAcc

	#probabilidade condicional  qij = P(xi = 0|ωj ) -> 'o'
	def qij(self, i, classId):
		dataSource = None
		total_datasource = None
		if classId == ClassEnum.negative.value:
			total_datasource = len(self.data_negative_learn)
			dataSource = self.data_negative_learn

		elif classId == ClassEnum.positive.value:
			total_datasource = len(self.data_positive_learn)
			dataSource = self.data_positive_learn

		sumAcc = Decimal(0) #acumulador de soma
		for example in dataSource:
			xi = example[0][i]
			sumAcc += Decimal(1-(xi**2))
		
		sumAcc *= Decimal(1)/Decimal(total_datasource) #equivale a 1/nj da formula desta questao
		# print('prod qij = '+str(sumAcc))
		return sumAcc

	#probabilidade condicional  qij = P(xi = -1|ωj ) -> 'b'
	def rij(self, i, classId):
		dataSource = None
		total_datasource = None
		if classId == ClassEnum.negative.value:
			total_datasource = len(self.data_negative_learn)
			dataSource = self.data_negative_learn

		elif classId == ClassEnum.positive.value:
			total_datasource = len(self.data_positive_learn)
			dataSource = self.data_positive_learn

		sumAcc = Decimal(0) #acumulador de soma
		for example in dataSource:
			xi = example[0][i]
			sumAcc += Decimal(xi*(xi-1))/Decimal(2)

		sumAcc *= (Decimal(1)/Decimal(total_datasource)) #equivale a 1/nj da formula desta questao

		# print('prod rij = '+str(sumAcc))
		return sumAcc

	def classify(self, features):
		p = self.posteriori(ClassEnum.positive.value, features)
		n = self.posteriori(ClassEnum.negative.value, features)

		if p > n:
			return ClassEnum.positive.value
		else:
			return ClassEnum.negative.value


	def calculateRange(self,next_range, set_size, max_length, is_last_set):
		#calculate test positive range
			start = next_range
			end = next_range + set_size

			#if passed of the end of examples, correct
			if end >= max_length or is_last_set:
				end = max_length

			return {"begin":start,"end":end}


	def kFold_Cross_Validation(self, k):

		# print("> Cross K-Fold Validation")
		# print()
		# print(">> K = "+str(k))

		next_range_positive = 0
		max_length_positive = len(self.data_positive)

		next_range_negative = 0
		max_length_negative = len(self.data_negative)

		set_size_positive = int(max_length_positive/k)
		set_size_negative = int(max_length_negative/k)
		# print(">> Positive set size = "+str(set_size_positive))
		# print(">> Negative set size = "+str(set_size_negative))
		# print()

		# print(">> Positive max end value = "+str(max_length_positive))
		# print(">> Negative max end value = "+str(max_length_negative))
		# print()

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
			# temp_data_positive = self.data_positive[:]
			# temp_data_negative = self.data_negative[:]

			#end for: creating sets

		all_corrects = 0
		all_wrongs = 0

		#test loop
		progress = 0.0
		for index_test in range(0,k):
			progress = index_test/k
			#write in the same line
			sys.stdout.write("\r>> Testing Progress: "+str(progress*100)+"%")
			sys.stdout.flush()

			errors_positive = 0
			errors_negative = 0

			#zera apontador de listas de aprendizado
			self.data_positive_learn = []
			self.data_negative_learn = []

			#a quantidade de conjuntos de classe eh igual apesar da diferença existir
			data_positive_test = positive_sets[index_test]
			data_negative_test = negative_sets[index_test]

			# print("-----------------------------------------------")
			# print(">> TESTING:")
			# print("Positive Set "+str(index_test)+", size: "+str(len(data_positive_test)))

			#cria lista de dados para aprendizagem com os sub-conjuntos que não sao de test
			for i in range(0,k):
				if i != index_test:
					self.data_positive_learn += positive_sets[i]
					self.data_negative_learn += negative_sets[i]

			samples_p = 0
			for i,p in enumerate(data_positive_test):

				# Classifying
				answer = self.classify(p[0])
				if answer != ClassEnum.positive.value:
					errors_positive += 1
				samples_p += 1


			# print(" -> Correct: "+str(((samples_p-errors_positive)/samples_p)*100)+"%")
			# print()

			# print("Negative Set "+str(index_test)+", size: "+str(len(data_negative_test)))
			samples_n = 0

			for n in data_negative_test:

				# Classifying
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

		sys.stdout.write("\r>> Testing Progress 100 %")
		sys.stdout.flush()

		correctness = Decimal(all_corrects)/Decimal(all_wrongs+all_corrects)

		print()
		print()
		print("Correct answers AVG: "+str((correctness*100))+"%")
		print("-----------------------------------------------")

		return correctness