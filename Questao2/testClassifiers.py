from bayes import *
from postKnnEstimation import *

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

	bayes.kFold_Cross_Validation(10)

	print("##############################################")
	print("### Posteriori Prob. Estim. via Knn        ###")
	print("##############################################")

	knn = PostKnnEstimation() 												#New Bayes Classifier instance
	knn.set_data(data_positive+data_negative)					#Give the learn data pre-processed
	knn.k = 17
	knn.kFold_Cross_Validation(10)