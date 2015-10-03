import os
from enum import Enum
from decimal import *

#limpa tela
clear = lambda: os.system('cls') #to clear screen during use of console in windows

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
		self.totalPositive = 0
		self.totalNegative = 0
		self.dataPositive = []
		self.dataNegative = []
		self.dataPositiveTest = []
		self.dataNegativeTest = []

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
				# 	# self.totalNegative +=1
				# elif acc == ClassEnum.positive.name:
				# 	# self.totalPositive +=1
				# else:
				# 	raise ValueError('Ops! Some class name is not correct in the data input.')
			else:
				features.append(FeatureEnum[acc].value) # salva a categoria comseu identificador de acordo com a classe enum
				acc = ''#reseta
		print(str(features)+" "+str(classId))
		return (features,classId)

	def readData(self, path):
		with open(path) as f:
			for line in f:
				processedLine = self.preProcess(line, separator=',')
				if processedLine[1] == ClassEnum.positive.value:# and self.totalPositive < 332:
					self.dataPositive.append(processedLine)
					# self.totalPositive +=1
				elif processedLine[1] == ClassEnum.negative.value:
					self.dataNegative.append(processedLine)
					# self.totalNegative +=1

		#separar parte de aprendizado de parte de testes.

		#70% para aprendizado #30% para testes
		percentTest = 0.15
		positives = len(self.dataPositive)
		negatives = len(self.dataNegative)

		cond1 = True
		cond2 = True
		
		while(cond1 or cond2):

			cond1= len(self.dataPositiveTest) < int(positives*percentTest)
			cond2 = len(self.dataNegativeTest) < int(negatives*percentTest)

			if cond1:
				self.dataPositiveTest.append(self.dataPositive.pop())
			if cond2:
				self.dataNegativeTest.append(self.dataNegative.pop())

			

		self.totalPositive = len(self.dataPositive)
		self.totalNegative = len(self.dataNegative)


	def priori(self, classId):
		if classId == ClassEnum.negative.value:
			return float(self.totalNegative)/float(self.totalNegative+self.totalPositive)
		elif classId == ClassEnum.positive.value:
			return float(self.totalPositive)/float(self.totalNegative+self.totalPositive)

	def posteriori(self, classId, features):
		#Parte superior da fração
		dividend = float(self.conditionalDensity(features,classId))*float(self.priori(classId))

		#Divisor
		sumAcc = float(self.conditionalDensity(features,0))*float(self.priori(0))
		sumAcc += float(self.conditionalDensity(features,1))*float(self.priori(1))

		return dividend/sumAcc
		

	def conditionalDensity(self, features, classId):
		dataSource = None
		if classId == ClassEnum.negative.value:
			dataSource = self.dataNegative
		elif classId == ClassEnum.positive.value:
			dataSource = self.dataPositive

		#TODO(Adailson): CALCULAR PRODUTÓRIO AQUI! (acho que é possivel otimizar os laços calculando pij,qij e rij em um unico laço visto que o j é igual para ambos toda vez que este produtorio rodar um laço)
		productAcc = float(1)
		i = 0;
		for xi in features:
			productAcc *= self.pij(i,classId)**float(xi*(xi +1)/2)
			productAcc *= self.qij(i,classId)**float(1-(xi**2))
			productAcc *= self.rij(i,classId)**float(xi*(xi -1)/2)
			i +=1

		return productAcc


	#probabilidade condicional  pij = P(xi = 1|ωj ) -> 'x'
	def pij(self, i, classId):
		dataSource = None
		totalDatasource = None
		if classId == ClassEnum.negative.value:
			dataSource = self.dataNegative
			totalDatasource = self.totalNegative

		elif classId == ClassEnum.positive.value:
			dataSource = self.dataPositive
			totalDatasource = self.totalPositive

		sumAcc = float(0) #acumulador de soma
		for example in dataSource:
			xi = example[0][i]
			sumAcc += float(xi*(xi+1))/float(2)

		sumAcc *= float(1)/float(totalDatasource) #equivale a 1/nj da formula desta questao
		return sumAcc

	#probabilidade condicional  qij = P(xi = 0|ωj ) -> 'o'
	def qij(self, i, classId):
		dataSource = None
		totalDatasource = None
		if classId == ClassEnum.negative.value:
			dataSource = self.dataNegative
			totalDatasource = self.totalNegative

		elif classId == ClassEnum.positive.value:
			dataSource = self.dataPositive
			totalDatasource = self.totalPositive

		sumAcc = float(0) #acumulador de soma
		for example in dataSource:
			xi = example[0][i]
			sumAcc += float(1-xi**2)
		
		sumAcc *= float(1)/float(totalDatasource) #equivale a 1/nj da formula desta questao

		return sumAcc

	#probabilidade condicional  qij = P(xi = -1|ωj ) -> 'b'
	def rij(self, i, classId):
		dataSource = None
		totalDatasource = None
		if classId == ClassEnum.negative.value:
			dataSource = self.dataNegative
			totalDatasource = self.totalNegative
		elif classId == ClassEnum.positive.value:
			dataSource = self.dataPositive
			totalDatasource = self.totalPositive

		sumAcc = float(0) #acumulador de soma
		for example in dataSource:
			xi = example[0][i]
			sumAcc += float(xi*(xi-1))/float(2)

		sumAcc *= (float(1)/float(totalDatasource)) #equivale a 1/nj da formula desta questao

		return sumAcc

	def classify(self, features):
		p = self.posteriori(ClassEnum.positive.value, features)
		# print("Probability a posteriori POSITIVE of "+str(p))

		n = self.posteriori(ClassEnum.negative.value, features)
		# print("Probability a posteriori NEGATIVE of "+str(n))

		#response = features_as_string+" was recognized as example of the class"

		if p >= n:
			ClassEnum.positive.value
		else:
			ClassEnum.negative.value


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

	def runTests(self):
		errorsPositive = 0

		for p in self.dataPositiveTest:
			answer = self.classify(p[0])
			if answer != p[1]:
				errorsPositive += 1

		errorsNegative = 0
		for n in self.dataNegativeTest:
			answer = self.classify(n[0])
			if answer != n[1]:
				errorsNegative += 1

		totalOk = (len(self.dataPositiveTest)-errorsPositive+len(self.dataNegativeTest)-errorsNegative)/(len(self.dataPositiveTest)+len(self.dataNegativeTest))
		totalError = (errorsPositive+errorsNegative)/(len(self.dataPositiveTest)+len(self.dataNegativeTest))

		print("------------------")
		print("----- REPORT -----")
		print("------------------")
		print()
		print(" Total correct : "+str(totalOk*100)+"%")
		print(" -> Correct answers (Positive examples): "+str((len(self.dataPositiveTest)-errorsPositive)))
		print(" -> Correct answers (negative examples): "+str((len(self.dataNegativeTest)-errorsNegative)))
		print()
		print(" Total worng : "+str(totalError*100)+"%")
		print(" -> wrong answers (Positive examples): "+str(errorsPositive))
		print(" -> wrong answers (negative examples): "+str(errorsNegative))



	def runForestRun(self):
		self.readData('../tic-tac-toe.data')

if __name__ == "__main__":

	bayes = Bayes() #Cria instancia da casse Bayes
	bayes.runForestRun()
	print("total de exemplos positivos " + str(bayes.totalPositive))
	print("total de exemplos negativos " + str(bayes.totalNegative))
	print("total de exemplos: " + str(bayes.totalNegative + bayes.totalPositive))
	print()
	bayes.runTests()


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
