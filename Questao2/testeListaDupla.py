
l1 = ['a','b','c','d','e','f','g','h','i','j']
l2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

i_max = max(len(l1),len(l2))

for i in range(i_max):
	if(i < len(l1)):
		print(l1[i])
	if(i< len(l2)):
		print(l2[i])
	print('-------------')