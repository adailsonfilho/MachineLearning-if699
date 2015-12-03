from bayes import *
from postKnnEstimation import *

class SumRule(Classifier):

	#Initialization of classifiers pre-determined
	def __init__(self, p_data, n_data, bayes_weigh=Decimal(0.5), knn_weigh=Decimal(0.5)):
		self.data_positive = p_data
		self.data_negative = n_data

		''' Setting up weights for sum'''
		self.bayes_weigh = bayes_weigh
		self.knn_weigh = knn_weigh

		'''
		###############################
		Bayes Classifier Initialization
		###############################
		'''
		self.bayes = Bayes()

		'''
		#######################################
		Knn Estimator Classifier Initialization
		#######################################
		'''
		self.knn = PostKnnEstimation()		

	def classify(self,x):
		# BAYES POTERIORIs
		bayes_positive_posteriori = self.bayes.posteriori(ClassEnum.positive.value, x)
		bayes_negative_posteriori  = self.bayes.posteriori(ClassEnum.negative.value, x)

		#Posteriori via KNN Estimation
		knn_answer = self.knn.posteriori_estimation(x)
		
		#sum rule in action


		p_priori = Decimal(self.knn.p_learn_size)/Decimal(self.knn.p_learn_size+self.knn.n_learn_size)
		n_priori = Decimal(self.knn.n_learn_size)/Decimal(self.knn.p_learn_size+self.knn.n_learn_size)
		final_prob_negative = n_priori*((knn_answer['negative']*self.knn_weigh) + (bayes_negative_posteriori*self.bayes_weigh))
		final_prob_pegative = p_priori*((knn_answer['positive']*self.knn_weigh) + (bayes_positive_posteriori*self.bayes_weigh))
		
		if final_prob_negative > final_prob_pegative:
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

		# print("> Cross K-Fold Validation")
		# print()
		# print(">> K = "+str(k))

		next_range_positive = 0
		max_length_positive = len(self.data_positive)

		next_range_negative = 0
		max_length_negative = len(self.data_negative)

		set_size_positive = int(max_length_positive/k)
		set_size_negative = int(max_length_negative/k)
		# print("Positive set size = "+str(set_size_positive))
		# print("Negative set size = "+str(set_size_negative))
		# print()

		# print("Positive max end value = "+str(max_length_positive))
		# print("Negative max end value = "+str(max_length_negative))
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
		for set_index in range(k):

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
		for index_test in range(0,k):

			#write in the same line
			sys.stdout.write("\r>> Testing Progress: "+str(((index_test/k)*100))+"%")
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

			data_positive_learn = []
			data_negative_learn = []

			for i in range(k):
				if i != index_test:
					data_positive_learn += positive_sets[i]
					data_negative_learn += negative_sets[i]
			
			self.bayes.set_data(data_positive_learn, data_negative_learn, learn_data=True);
			self.knn.set_data(data_positive_learn+data_negative_learn,learn_data=True)

			samples_p = 0
			samples_n = 0

			i_max = max(len(data_positive_test), len(data_negative_test))
			for i in range(i_max):
				if i < len(data_positive_test):
					answer = self.classify(data_positive_test[i][0])
					if answer != ClassEnum.positive.value:
						errors_positive += 1
					samples_p += 1
				if i < len(data_negative_test):
					answer = self.classify(data_negative_test[i][0])
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

		sys.stdout.write("\r>> Testing Progress: COMPLETED")
		sys.stdout.flush()

		correctness = Decimal(all_corrects)/Decimal(all_wrongs+all_corrects)

		print()
		print()
		print("FINAL REPORT")
		print("Avarage of correct answers: "+str((correctness*100))+"%")
		print("-----------------------------------------------")

		return correctness