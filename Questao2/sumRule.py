from bayes import *
from postKnnEstimation import *

class SumRule(Classifier):



	#Initialization of classifiers pre-determined
	def __init__(self, p_data, n_data, bayes_weigh, knn_weigh):
		''' Setting up weights for sum'''
		self.bayes_weigh = bayes_weigh
		self.knn_weigh = knn_weigh

		'''
		###############################
		Bayes Classifier Initialization
		###############################
		'''
		self.bayes = Bayes()
		self.bayes.set_data(p_data, n_data);

		'''
		###############################
		Knn Estimator Classifier Initialization
		###############################
		'''
		self.knn = PostKnnEstimation()
		self.knn.set_data(p_data+n_data)
		

	def classify(self,x):
		# BAYES POTERIORIs
		bayes_positive_posteriori = self.bayes.posteriori(ClassEnum.positive.value, x)
		bayes_negative_posteriori  = self.bayes.posteriori(ClassEnum.negative.value, x)

		#Posteriori via KNN Estimation
		knn_answer = self.riori_estimation(x)
		
		#sum rule in action

		final_prob_negative = (knn_answer['negative']*self.knn_weigh) + (bayes_negative_posteriori*self.bayes_weigh)
		final_prob_pegative = (knn_answer['positive']*self.knn_weigh) + (bayes_positive_posteriori*self.bayes_weigh)
		
		if final_prob_negative > final_prob_pegative:
			return ClassEnum.negative.value
		else:
			return ClassEnum.positive.value
