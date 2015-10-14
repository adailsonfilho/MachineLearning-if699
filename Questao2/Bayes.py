import os
from enum import Enum
from decimal import *

#limpa tela
clear = lambda: os.system('cls') #to clear screen during use of console in windows

getcontext().prec += 5

#Enumera as variaveis categóricas
class FeatureEnum(Enum): #how use that shit? Categories['x']
	x = 1
	o = 0
	b = -1

#enumera as classes
class ClassEnum(Enum): #how use that shit? Class['positive']
	positive = 1
	negative = 0

class Bayes():
	def __init__(self):

		self.total_positive = 0
		self.total_negative = 0
		self.data_positive = []
		self.data_negative = []

		#for use in tests k-fold
		self.positive_test_range = None
		self.negative_test_range= None

	def preProcess(self, line, separator):
		#Adailson: Este método poderia ser feito com split(','), mas a performance ia cair um pouco (onde a gente puder ganhar em performance nesse tipo de aplicação é importante)

		features = []#ira armazenas os dados convertidos. Ex: "x,x,x,o,o,o,b,b,b,positivo" vira ([1,1,1,0,0,0,-1,-1,-1],1) (de acordo com a classe enum)
		classId = None
		acc = '' #acumulador

		#line += '$'#para servir de referencia do fim do token

		for x in line:
			if x != ',' and x != '\n':
				acc += x
			elif x == '\n':
				classId = ClassEnum[acc].value
				# if acc == ClassEnum.negative.name:
				# 	# self.total_negative +=1
				# elif acc == ClassEnum.positive.name:
				# 	# self.total_positive +=1
				# else:
				# 	raise ValueError('Ops! Some class name is not correct in the data input.')
			else:
				features.append(FeatureEnum[acc].value) # salva a categoria comseu identificador de acordo com a classe enum
				acc = ''#reseta
		# print(str(features)+" "+str(classId))
		return (features,classId)

	def readData(self, path):
		with open(path) as f:
			for line in f:
				processedLine = self.preProcess(line, separator=',')
				if processedLine[1] == ClassEnum.positive.value:
					self.data_positive.append(processedLine)
				elif processedLine[1] == ClassEnum.negative.value:
					self.data_negative.append(processedLine)

		# #separar parte de aprendizado de parte de testes.

		# #70% para aprendizado #30% para testes
		# percentTest = 0.2
		# positives = len(self.data_positive)
		# negatives = len(self.data_negative)

		# cond1 = True
		# cond2 = True
		
		# while(cond1 or cond2):

		# 	cond1= len(self.data_positive_test) < int(positives*percentTest)
		# 	cond2 = len(self.data_negative_test) < int(negatives*percentTest)

		# 	if cond1:
		# 		self.data_positive_test.append(self.data_positive.pop())
		# 	if cond2:
		# 		self.data_negative_test.append(self.data_negative.pop())


	def priori(self, classId):
		if classId == ClassEnum.negative.value:
			return Decimal(self.total_negative)/Decimal(self.total_negative+self.total_positive)
		elif classId == ClassEnum.positive.value:
			return Decimal(self.total_positive)/Decimal(self.total_negative+self.total_positive)

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
			dataSource = self.data_negative
		elif classId == ClassEnum.positive.value:
			dataSource = self.data_positive

		#TODO(Adailson): CALCULAR PRODUTÓRIO AQUI! (acho que é possivel otimizar os laços calculando pij,qij e rij em um unico laço visto que o j é igual para ambos toda vez que este produtorio rodar um laço)
		productAcc = Decimal(1)
		i = 0;
		for xi in features:
			productAcc *= self.pij(i,classId)**Decimal(xi*(xi +1)/2)
			productAcc *= self.qij(i,classId)**Decimal(1-(xi**2))
			productAcc *= self.rij(i,classId)**Decimal(xi*(xi -1)/2)
			i +=1

		return productAcc


	#probabilidade condicional  pij = P(xi = 1|ωj ) -> 'x'
	def pij(self, i, classId):
		dataSource = None
		total_datasource = None
		if classId == ClassEnum.negative.value:
			neg = self.negative_test_range
			total_datasource = self.total_negative
			dataSource = self.data_negative[0:neg['begin']] + self.data_negative[neg['end']:total_datasource]			

		elif classId == ClassEnum.positive.value:
			neg = self.positive_test_range
			total_datasource = self.total_positive
			dataSource = self.data_positive[0:neg['begin']] + self.data_positive[neg['end']:total_datasource]

		sumAcc = Decimal(0) #acumulador de soma
		for example in dataSource:
			xi = example[0][i]
			sumAcc += Decimal(xi*(xi+1))/Decimal(2)

		sumAcc *= Decimal(1)/Decimal(total_datasource) #equivale a 1/nj da formula desta questao
		return sumAcc

	#probabilidade condicional  qij = P(xi = 0|ωj ) -> 'o'
	def qij(self, i, classId):
		dataSource = None
		total_datasource = None
		if classId == ClassEnum.negative.value:
			neg = self.negative_test_range
			total_datasource = self.total_negative
			dataSource = self.data_negative[0:neg['begin']] + self.data_negative[neg['end']:total_datasource]			

		elif classId == ClassEnum.positive.value:
			neg = self.positive_test_range
			total_datasource = self.total_positive
			dataSource = self.data_positive[0:neg['begin']] + self.data_positive[neg['end']:total_datasource]

		sumAcc = Decimal(0) #acumulador de soma
		for example in dataSource:
			xi = example[0][i]
			sumAcc += Decimal(1-xi**2)
		
		sumAcc *= Decimal(1)/Decimal(total_datasource) #equivale a 1/nj da formula desta questao

		return sumAcc

	#probabilidade condicional  qij = P(xi = -1|ωj ) -> 'b'
	def rij(self, i, classId):
		dataSource = None
		total_datasource = None
		if classId == ClassEnum.negative.value:
			neg = self.negative_test_range
			total_datasource = self.total_negative
			dataSource = self.data_negative[0:neg['begin']] + self.data_negative[neg['end']:total_datasource]			

		elif classId == ClassEnum.positive.value:
			neg = self.positive_test_range
			total_datasource = self.total_positive
			dataSource = self.data_positive[0:neg['begin']] + self.data_positive[neg['end']:total_datasource]

		sumAcc = Decimal(0) #acumulador de soma
		for example in dataSource:
			xi = example[0][i]
			sumAcc += Decimal(xi*(xi-1))/Decimal(2)

		sumAcc *= (Decimal(1)/Decimal(total_datasource)) #equivale a 1/nj da formula desta questao

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


	def runCrossKFoldValidation(self, k):

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

		#Begin Cross K-Fold Validation
		results = [] #tuplas (int corrects,int errors)

		for test_set in range(0,k):

			positive_range = self.calculateRange(next_range_positive, set_size_positive,max_length_positive, test_set == k-1)
			self.data_positive_test = self.data_positive[positive_range['begin']:positive_range['end']]
			next_range_positive = positive_range['end']
			self.positive_test_range = positive_range
			
			negative_range = self.calculateRange(next_range_negative, set_size_negative, max_length_negative, test_set == k-1)
			self.data_negative_test = self.data_negative[negative_range['begin']:negative_range['end']]
			next_range_negative = negative_range['end']
			self.negative_test_range = negative_range

			errors_positive = 0
			errors_negative = 0


			#updating range test
			positive_test_size = self.positive_test_range['begin'] - self.positive_test_range['end']
			self.total_positive = len(self.data_positive) - positive_test_size

			negative_test_size = self.negative_test_range['begin'] - self.negative_test_range['end']
			self.total_negative = len(self.data_negative) - negative_test_size

			print("-----------------------------------------------")
			print(">> TESTING:")
			print("Positive Set "+str(test_set)+", range: "+str(positive_range))			

			samples_p = 0
			for p in self.data_positive_test:
				answer = self.classify(p[0])
				if answer != ClassEnum.positive.value:
					errors_positive += 1
				samples_p += 1

			print(" -> Correct: "+str(((samples_p-errors_positive)/samples_p)*100)+"%")
			print()

			print("Negative Set "+str(test_set)+", range: "+str(negative_range))
			samples_n = 0
			for n in self.data_negative_test:
				answer = self.classify(n[0])
				if answer != ClassEnum.negative.value:
					errors_negative += 1
				samples_n += 1

			print(" -> Correct: "+str(((samples_n-errors_negative)/samples_n)*100)+"%")

			print()
			print("Total Correct: "+str(((samples_n-errors_negative+samples_p-errors_positive)/(samples_n+samples_p))*100)+"%")
			print("-----------------------------------------------")
			#fim do for

		# errorsPositive = 0

		# print("Wait! Processing ...")

		# for p in self.data_positive_test:
		# 	answer = self.classify(p[0])
		# 	if answer != ClassEnum.positive.value:
		# 		errorsPositive += 1

		# errorsNegative = 0
		# for n in self.data_negative_test:
		# 	answer = self.classify(n[0])
		# 	if answer != ClassEnum.negative.value:
		# 		errorsNegative += 1

		# totalOk = (len(self.data_positive_test)-errorsPositive+len(self.data_negative_test)-errorsNegative)/(len(self.data_positive_test)+len(self.data_negative_test))
		# totalError = (errorsPositive+errorsNegative)/(len(self.data_positive_test)+len(self.data_negative_test))

		# print("------------------")
		# print("----- REPORT -----")
		# print("------------------")
		# print()
		# print(" Total correct : "+str(totalOk*100)+"%")
		# print(" -> Correct answers (Positive examples): "+str((len(self.data_positive_test)-errorsPositive)))
		# print(" -> Correct answers (negative examples): "+str((len(self.data_negative_test)-errorsNegative)))
		# print()
		# print(" Total worng : "+str(totalError*100)+"%")
		# print(" -> wrong answers (Positive examples): "+str(errorsPositive))
		# print(" -> wrong answers (negative examples): "+str(errorsNegative))



	def runForestRun(self):
		self.readData('../tic-tac-toe.data')

if __name__ == "__main__":

	bayes = Bayes() #Cria instancia da casse Bayes
	bayes.runForestRun()
	print("total de exemplos positivos " + str(bayes.total_positive))
	print("total de exemplos negativos " + str(bayes.total_negative))
	print("total de exemplos: " + str(bayes.total_negative + bayes.total_positive))
	print()
	bayes.runCrossKFoldValidation(10)


	# teste ingênuo
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
