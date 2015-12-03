from bayes import *
from postKnnEstimation import *
from sumRule import *
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

	repeatTest = 10
	
	print("##############################################")
	print("### Baysian Decision                       ###")
	print("##############################################")

	bayes = Bayes() 												#New Bayes Classifier instance
	bayes.set_data(data_positive, data_negative);					#Give the learn data pre-processed

	p = len(bayes.data_positive)
	n = len(bayes.data_negative)

	print("Total data")
	print("> Positive samples" + str(p))
	print("> Negative samples" + str(n))
	print("> Total samples: " + str(p+n))
	print()

	bayes_correctness_history = []
	for test in range(repeatTest):
		print(">>> "+str(1+test)+" of "+str(repeatTest)+": Repetitions of K-fold Cross Validation")
		bayes_correctness_history.append(bayes.kFold_Cross_Validation(10))

	print("##############################################")
	print("### Posteriori Prob. Estim. via Knn        ###")
	print("##############################################")

	knn = PostKnnEstimation()									#New Bayes Classifier instance
	knn.set_data(data_positive+data_negative)					#Give the learn data pre-processed
	knn.k = 15

	knn_correctness_history = []
	for test in range(repeatTest):
		print(">>> "+str(1+test)+" of "+str(repeatTest)+": Repetitions of K-fold Cross Validation")
		knn_correctness_history.append(knn.kFold_Cross_Validation(10))

	print("###############################################################")
	print("### Sum Rule - With Weighs Based on classifiers correctness   ###")
	print("###############################################################")

	l = bayes_correctness_history
	bayes_correctness_avg = Decimal(reduce(lambda x, y: x + y, l)) / Decimal(len(l))

	l = knn_correctness_history
	knn_correctness_avg = Decimal(reduce(lambda x, y: x + y, l)) / Decimal(len(l))


	print("Bayes Correctness AVG: "+str(bayes_correctness_avg))
	print("Prob. Posteriori Estimation via Knn Correctness AVG: "+str(knn_correctness_avg))

	bayes_weigh = bayes_correctness_avg/(bayes_correctness_avg+knn_correctness_avg)
	knn_weigh = knn_correctness_avg/(bayes_correctness_avg+knn_correctness_avg)

	# p_data, n_data, bayes_weigh, knn_weigh):
	sum_rule = SumRule(data_positive, data_negative, bayes_weigh, knn_weigh)

	sum_rule_correctness_history = []
	for test in range(repeatTest):
		print(">>> "+str(1+test)+" of "+str(repeatTest)+": Repetitions of K-fold Cross Validation")
		sum_rule_correctness_history.append(sum_rule.kFold_Cross_Validation(10))


	# ipdb.set_trace()
	# #TODO: SUM RULE ACTION	