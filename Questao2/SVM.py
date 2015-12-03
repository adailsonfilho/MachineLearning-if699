import matplotlib.pyplot as plt
import numpy as np
import warnings
from enum import  Enum
from sklearn import svm
from random import randint
from ticTacToe import *


class SupportVectorMachine():
    def __init__(self):

        self.total_positive = 0
        self.total_negative = 0

        #All data readed from files after pre-processed
        self.data_positive = []
        self.data_negative = []

        #data for learning after
        self.data_positive_learn = []
        self.data_negative_learn = []





    def readData(self, path):
            with open(path) as f:
                for line in f:
                    processedLine = self.pre_process(line, separator=',')
                    if processedLine[0] == ClassEnum.positive.value:
                        self.data_positive.append(processedLine)

                    elif processedLine[0] == ClassEnum.negative.value:
                        self.data_negative.append(processedLine)
                        


            #print(self.data_positive)
            #print(self.data_negative)


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

        warnings.simplefilter('ignore', DeprecationWarning)

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

        	#Starting here i must change it to according the SVM
        	#cria lista de dados para aprendizagem com os sub-conjuntos que não sao de test


        	for i in range(0,k):
        		if i != index_test:
        			self.data_positive_learn += positive_sets[i]
        			self.data_negative_learn += negative_sets[i]
        	
        	
        	all_data = self.data_positive_learn + self.data_negative_learn

        	x = []
        	y = []

        	for z in all_data:
        		x.append(z[1])
        		y.append(z[0])

        	clf = svm.SVC(decision_function_shape='ovr')
        	print("Starting SVM classification")
        	clf.fit(x, y)
        	
        	samples_p = 0
        	for p in data_positive_test:
        		answer = clf.predict(p[1])
        		if answer != ClassEnum.positive.value:
        			errors_positive += 1
        		samples_p += 1

        	print(" -> Correct: "+str(((samples_p-errors_positive)/samples_p)*100)+"%")
        	print()

        	print("Negative Set "+str(index_test)+", size: "+str(len(data_negative_test)))
        	samples_n = 0

        	for n in data_negative_test:
        		answer = clf.predict(n[1])
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

        correctness = Decimal(all_corrects)/Decimal(all_wrongs+all_corrects)
        

    def runForestRun(self):
            self.readData('../tic-tac-toe.data')

   

    

    #SVM part, using scikit learn
if __name__ == "__main__":

    support = SupportVectorMachine()

    support.runForestRun()

    repeat = 10

    suport_history = []
    for i in range(repeat):
        correctness = support.run_KFold_Cross_Validation(10)
        suport_history.append(correctness)

