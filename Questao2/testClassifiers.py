from bayes import *
from postKnnEstimation import *
from functools import reduce
# import ipdb

data_positive = []	
data_negative = []

def read_data(path):
	with open(path) as f:
		for line in f:
			processedLine = pre_process(line, separator=',')
			if processedLine[1] == ClassEnum.positive.value: #and len(self.data_positive) < 332:
				data_positive.append(processedLine)
			elif processedLine[1] == ClassEnum.negative.value:
				data_negative.append(processedLine)

if __name__ == "__main__":

	read_data('../tic-tac-toe.data')								#Read data into local vars

	repeatTest = 30
	
	# print("##############################################")
	# print("### Baysian Decision                       ###")
	# print("##############################################")

	# bayes = Bayes() 												#New Bayes Classifier instance
	# bayes.set_data(data_positive, data_negative);					#Give the learn data pre-processed

	# p = len(bayes.data_positive)
	# n = len(bayes.data_negative)

	# print("Total data")
	# print("> Positive samples" + str(p))
	# print("> Negative samples" + str(n))
	# print("> Total samples: " + str(p+n))
	# print()

	# bayes_correctness_history = []
	# for test in range(repeatTest):
	# 	print(">>> "+str(test)+" of "+str(repeatTest)+": Repetitions of K-fold Cross Validation")
	# 	bayes_correctness_history.append(bayes.kFold_Cross_Validation(10))

	print("##############################################")
	print("### Posteriori Prob. Estim. via Knn        ###")
	print("##############################################")

	knn = PostKnnEstimation() 												#New Bayes Classifier instance
	knn.set_data(data_positive+data_negative)					#Give the learn data pre-processed
	knn.k = 17

	knn_correctness_history = []
	for test in range(repeatTest):
		print(">>> "+str(test)+" of "+str(repeatTest)+": Repetitions of K-fold Cross Validation")
		knn_correctness_history.append(knn.kFold_Cross_Validation(10))

	print("###############################################################")
	print("### Sum Rule - With Weighs Based on classifiers correctness   ###")
	print("###############################################################")

	# l = bayes_correctness_history
	# bayes_correctness_avg = Decimal(reduce(lambda x, y: x + y, l)) / Decimal(len(l))

	l = knn_correctness_history
	knn_correctness_avg = Decimal(reduce(lambda x, y: x + y, l)) / Decimal(len(l))


	# print(bayes_correctness_avg)
	print(knn_correctness_avg)
	# ipdb.set_trace()
	# #TODO: SUM RULE ACTION	