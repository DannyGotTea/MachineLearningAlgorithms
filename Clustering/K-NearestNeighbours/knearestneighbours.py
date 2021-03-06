from theano import function
from collections import Counter
import theano.tensor as T
import numpy as np
import theano
import operator

rand_gen = np.random

def calc_distances(step, inputs, neighbours, k): #CURRENTLY DEPENDS ON NUMBERS

	nb_feat = neighbours[step][:4] #everything but last feature
	target = neighbours[-1] #last feature

	distance = T.sqrt(T.sum((inputs - nb_feat) ** 2)) #Euclidean distances

	return distance

input_var = T.matrix('input')
nb = T.matrix('neighbours')

k = T.iscalar('k_value')

step_count = T.iscalar('steps')

seq = T.arange(step_count)

output_model = T.as_tensor_variable(np.asarray(0, step_count.dtype))

scan_result, scan_updates = theano.scan(fn=calc_distances, outputs_info=None, sequences=seq, non_sequences=[input_var, nb, k])

distances = theano.function(inputs=[input_var, nb, k, step_count], outputs=scan_result)


def k_nearest_neighbours(inputs, nb, k, steps):

	distance_output = distances(input=inputs, neighbours=nb, k_value=k, steps=steps)

	dict_out = dict(enumerate(distance_output))

	knn_index = (sorted(dict_out.items(), key=operator.itemgetter(1)))[:k+1] #Gets the k smallest (closest) value indexes

	k_nearest_matrix = np.array([neighbours[x[0]] for x in knn_index])

	return k_nearest_matrix

def predict_knn(nrst_nbrs, class_index):

	predictions = []

	classes = nrst_nbrs[:, class_index]

	modes = Counter(classes)

	print modes

	prediction = max(modes.items())

	predictions.append(prediction[0])

	return predictions

def knn_accuracy(predictions, true_values):

	if len(predictions) != len(true_values):
		raise ValueError

	equality = 0.0

	equality = [equality+1 for x in range(len(true_values)) if predictions[x] == true_values[x]]

	accuracy = sum(equality) / len(true_values)

	return accuracy


#Create samples for testing

input_features = np.array([[6.3,2.7,4.9,1.8]])


neighbours = np.array([ # 0 = Iris-setosa, 1 = Iris-versicolor, 2 = Iris-virginica
[5.1,3.5,1.4,0.3,0],[5.7,3.8,1.7,0.3,0],[5.1,3.5,1.4,0.2,0],
[5.4,3.4,1.7,0.2,0],[5.1,3.7,1.5,0.4,0],[4.6,3.6,1.0,0.2,0],
[5.1,3.3,1.7,0.5,0],[4.8,3.4,1.9,0.2,0],[5.0,3.0,1.6,0.2,0],
[5.0,3.4,1.6,0.4,0],[6.0,3.4,4.5,1.6,1],[6.7,3.1,4.7,1.5,1],
[6.3,2.3,4.4,1.3,1],[5.6,3.0,4.1,1.3,1],[5.5,2.5,4.0,1.3,1],
[5.5,2.6,4.4,1.2,1],[6.1,3.0,4.6,1.4,1],[5.8,2.6,4.0,1.2,1],
[5.0,2.3,3.3,1.0,1],[5.6,2.7,4.2,1.3,1],[6.9,3.2,5.7,2.3,2],
[5.6,2.8,4.9,2.0,2],[7.7,2.8,6.7,2.0,2],[6.3,2.7,4.9,1.8,2],
[6.7,3.3,5.7,2.1,2],[7.2,3.2,6.0,1.8,2],[6.2,2.8,4.8,1.8,2],
[6.1,3.0,4.9,1.8,2],[6.4,2.8,5.6,2.1,2],[7.2,3.0,5.8,1.6,2]])

k = 5
steps = len(neighbours)
target_index = 4 #the index that the class is at in neighbours

knn = k_nearest_neighbours(input_features, neighbours, k, steps)

predictions = predict_knn(knn, target_index)

print predictions






