import os
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

		#for use in tests k-fold
		# self.positive_test_range = None
		# self.negative_test_range= None

	def read_data(self, path):
		with open(path) as f:
			for line in f:
				processedLine = pre_process(line, separator=',')
				if processedLine[1] == ClassEnum.positive.value: #and len(self.data_positive) < 332:
					self.data_positive.append(processedLine)
				elif processedLine[1] == ClassEnum.negative.value:
					self.data_negative.append(processedLine)


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
		productAcc = Decimal(1)
		i = 0;
		for xi in features:

			p = Decimal(self.pij(i,classId))**(Decimal(xi*(xi +1))/Decimal(2))
			if p == 0:
				p = 1

			q = Decimal(self.qij(i,classId))**(Decimal(1)-Decimal(xi**2))
			if q == 0:
				q = 1

			r_exp = Decimal(xi*(xi -1))/Decimal(2)
			r = getcontext().power(Decimal(self.rij(i,classId)),r_exp)
			if r == 0:
				r = 1
			productAcc *= p
			productAcc *= q
			productAcc *= r
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
		# print(str(features))
		# print("Probability a posteriori for POSITIVE of "+str(p))

		n = self.posteriori(ClassEnum.negative.value, features)
		# print("Probability a posteriori for NEGATIVE of "+str(n))

		#response = features_as_string+" was recognized as example of the class"

		if p > n:
			return ClassEnum.positive.value
		else:
			return ClassEnum.negative.value


	# def classify(self, string features_as_string):
	# 	features = features_as_string.split(',')
	# 	try:
	# 		features = list(map(lambda x: FeatureEnum[x].value, features))
	# 	except valueError:
	# 		print("Ops! An error occoured. Please verify the input format")


	# 	if len(features) != 9:
	# 		raise ValueError ("Features for classification in wrong length")

	# 	p = self.posteriori(ClassEnum.positive.value, features)
	# 	print("Probability a posteriori POSITIVE of "+str(p))

	# 	n = self.posteriori(ClassEnum.negative.value, features)
	# 	print("Probability a posteriori NEGATIVE of "+str(n))

	# 	response = features_as_string+" was recognized as example of the class "

	# 	if p >= n:
	# 		return response+ClassEnum.positive.name
	# 	else:
	# 		return response+ClassEnum.negative.name


	def calculateRange(self,next_range, set_size, max_length, is_last_set):
		#calculate test positive range
			start = next_range
			end = next_range + set_size

			#if passed of the end of examples, correct
			if end >= max_length or is_last_set:
				end = max_length

			return {"begin":start,"end":end}


	def run_KFold_Cross_Validation(self, k):

		print("###############################")
		print("### Cross K-Fold Validation ###")
		print("###############################")
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

		for set_index in range(0,k):

			print("creating positive set index "+str(set_index))
			
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

			print("Created: "+str(len(positive_sets[set_index]))+" samples")
			
			print("creating negative set index "+str(set_index))
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

			print("Created: "+str(len(positive_sets[set_index]))+" samples")

			#copy lists
			temp_data_positive = self.data_positive[:]
			temp_data_negative = self.data_negative[:]

			#end for: creating sets

		all_corrects = 0
		all_wrongs = 0

		#test loop
		for index_test in range(0,k):
			errors_positive = 0
			errors_negative = 0

			#zera apontador de listas de aprendizado
			self.data_positive_learn = []
			self.data_negative_learn = []

			#a quantidade de conjuntos de classe eh igual apesar da diferença existir
			data_positive_test = positive_sets[index_test]
			data_negative_test = negative_sets[index_test]

			print("-----------------------------------------------")
			print(">> TESTING:")
			print("Positive Set "+str(index_test)+", size: "+str(len(data_positive_test)))

			#cria lista de dados para aprendizagem com os sub-conjuntos que não sao de test
			for i in range(0,k):
				if i != index_test:
					self.data_positive_learn += positive_sets[i]
					self.data_negative_learn += negative_sets[i]

			samples_p = 0
			for p in data_positive_test:
				answer = self.classify(p[0])
				if answer != ClassEnum.positive.value:
					errors_positive += 1
				samples_p += 1

			print(" -> Correct: "+str(((samples_p-errors_positive)/samples_p)*100)+"%")
			print()

			print("Negative Set "+str(index_test)+", size: "+str(len(data_negative_test)))
			samples_n = 0

			for n in data_negative_test:
				answer = self.classify(n[0])
				if answer != ClassEnum.negative.value:
					errors_negative += 1
				samples_n += 1

			print(" -> Correct: "+str(((samples_n-errors_negative)/samples_n)*100)+"%")


			all_corrects += (samples_p-errors_positive) + (samples_n-errors_negative)
			all_wrongs += errors_positive + errors_negative
			print()
			print("Correct for all classes in test "+str(index_test)+" : "+str(((samples_n-errors_negative+samples_p-errors_positive)/(samples_n+samples_p))*100)+"%")
			print("-----------------------------------------------")
			#fim do for
		print()
		print("FINAL REPORT")
		print("Avarage of correct answers: "+str((all_corrects)/(all_wrongs+all_corrects)*100)+"%")
		print("-----------------------------------------------")

	def runForestRun(self):
		self.read_data('../tic-tac-toe.data')

if __name__ == "__main__":

	bayes = Bayes() #Cria instancia da casse Bayes
	bayes.runForestRun()
	p = len(bayes.data_positive)
	n = len(bayes.data_negative)

	print("total de exemplos positivos " + str(p))
	print("total de exemplos negativos " + str(n))
	print("total de exemplos: " + str(p+n))
	print()

	bayes.run_KFold_Cross_Validation(10)

	# the greatest naive test
	# response = bayes.classify("x,o,b,x,o,o,x,b,b") #Deveria dar positivo
	# print(response)
	# print()

	# response = bayes.classify("x,o,b,o,o,b,x,o,b") #Deveria dar negativo
	# print(response)
	# print()

	# response = bayes.classify("x,o,b,x,o,o,x,b,b") #Deveria dar positivo
	# print(response)
	# print()

	# response = bayes.classify("o,o,x,o,x,b,o,o,b") #Deveria dar negativo
	# print(response)
	# print()

