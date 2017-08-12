import random
import math

class Neuron(object):
	def __init__(self, numInputs):
		self.numInputs = numInputs
		self.weights = []
		for i in range(0, self.numInputs+1):
			self.weights.append(random.uniform(-1.0, 1.0))

class NeuralLayer(object):
	def __init__(self, numNeurons, numInputsPerNeuron):
		self.numNeurons = numNeurons
		self.numInputsPerNeuron = numInputsPerNeuron
		self.neurons = []
		for i in range(0, self.numNeurons):
			self.neurons.append(Neuron(numInputsPerNeuron))

class NeuralNetwork(object):
	def __init__(self, numInputs, numOutputs, numHiddenLayers, numNeuronsPerHiddenLayer):
		self.numInputs = numInputs
		self.numOutputs = numOutputs
		self.numHiddenLayers = numHiddenLayers
		self.numNeuronsPerHiddenLayer = numNeuronsPerHiddenLayer
		self.layers = []
	
	def create(self):
		if self.numHiddenLayers > 0:
			self.layers.append(NeuralLayer(self.numNeuronsPerHiddenLayer, self.numInputs))
			
			for i in range(0, self.numHiddenLayers - 1):
				self.layers.append(NeuralLayer(self.numNeuronsPerHiddenLayer, self.numNeuronsPerHiddenLayer))
			
			self.layers.append(NeuralLayer(self.numOutputs, self.numNeuronsPerHiddenLayer))
		else:
			self.layers.append(NeuralLayer(self.numOutputs, self.numInputs))
			
	def getWeights(self):
		weights = []
		
		for i in range(0, self.numHiddenLayers + 1): # + output layer
			for j in range(0, self.layers[i].numNeurons):
				for k in range(0, self.layers[i].neurons[j].numInputs):
					weights.append(self.layers[i].neurons[j].weights[k])
		return weights
	
	def putWeights(self, weights):
		aux = 0
		for i in range(0, self.numHiddenLayers + 1): # + output layer
			for j in range(0, self.layers[i].numNeurons):
				for k in range(0, self.layers[i].neurons[j].numInputs):
					self.layers[i].neurons[j].weights[k] = weights[aux]
					aux += 1
	
	def getNumberWeights(self):
		aux = 0
		for i in range(0, self.numHiddenLayers + 1): # + output layer
			for j in range(0, self.layers[i].numNeurons):
				for k in range(0, self.layers[i].neurons[j].numInputs):
					aux += 1
		return aux
	
	def update(self, inputs):
		outputs = []
		
		for i in range(0, self.numHiddenLayers + 1):
			if(i > 0):
				inputs = outputs
			
			outputs = []

			for j in range(0, self.layers[i].numNeurons):
				netInput = 0
				
				numInputs = self.layers[i].neurons[j].numInputs

				for k in range(0, numInputs):
					netInput += self.layers[i].neurons[j].weights[k]*inputs[k]
				
				netInput += self.layers[i].neurons[j].weights[numInputs]*-1
				
				outputs.append(self.sigmoid(netInput, 1))
				
		return outputs
	
	def sigmoid(self, netInput, response):
		return ( 1 / ( 1 + math.exp(-netInput / response)))
