import utils
import math
from neuralNetwork import NeuralNetwork

class Car(object):
	
	def __init__(self, (x, y)):
		self.neuralNet = NeuralNetwork(7, 2, 1, 5)
		self.neuralNet.create()
		
		self.fitness = 0
		self.frontWidth = 20
		self.sideWidth = 40
		self.position = (x, y)
		self.direction = 0
		self.edgesPoints = 	[[self.position[0] - self.sideWidth//2, self.position[1] - self.frontWidth//2],
							[self.position[0] - self.sideWidth//2, self.position[1] + self.frontWidth//2],
							[self.position[0] + self.sideWidth//2, self.position[1] + self.frontWidth//2],
							[self.position[0] + self.sideWidth//2, self.position[1] - self.frontWidth//2],
							[self.position[0] - self.sideWidth//2, self.position[1] - self.frontWidth//2]]
		self.edgesPointsAprox = self.edgesPoints
		self.speed = 10
		self.isAlive = True
		self.rayPoints = [[], [], [], [], [], [], []]
		self.inputs = [0, 0, 0, 0, 0, 0, 0]
		self.lastsCookies = []
		self.cookie = 0
		
	def __getattr__(self, name):
		if name == 'frontPoint':
			return utils.midpoint(self.edgesPoints[0], self.edgesPoints[1])
		elif name == 'leftPoint':
			return utils.midpoint(self.edgesPoints[1], self.edgesPoints[2])
		elif name == 'backPoint':
			return utils.midpoint(self.edgesPoints[2], self.edgesPoints[3])
		elif name == 'rightPoint':
			return utils.midpoint(self.edgesPoints[3], self.edgesPoints[0])
		elif name == 'frontRightPoint':
			return self.edgesPoints[0]
		elif name == 'frontLeftPoint':
			return self.edgesPoints[1]
		elif name == 'frontRight2Point':
			return utils.midpoint(self.edgesPoints[0], self.rightPoint)
		elif name == 'frontLeft2Point':
			return utils.midpoint(self.edgesPoints[1], self.leftPoint)
		elif name == 'isGoingForward':
			if self.speed > 0:
				return True
			else:
				return False
	
	def reset(self, (x, y)):
		self.fitness = 0
		self.position = (x, y)
		self.direction = 0
		self.edgesPoints = 	[[self.position[0] - self.sideWidth//2, self.position[1] - self.frontWidth//2],
							[self.position[0] - self.sideWidth//2, self.position[1] + self.frontWidth//2],
							[self.position[0] + self.sideWidth//2, self.position[1] + self.frontWidth//2],
							[self.position[0] + self.sideWidth//2, self.position[1] - self.frontWidth//2],
							[self.position[0] - self.sideWidth//2, self.position[1] - self.frontWidth//2]]
		self.edgesPointsAprox = self.edgesPoints
		self.speed = 8
		self.isAlive = True
		self.rayPoints = [[], [], [], [], [], [], []]
		self.inputs = [0, 0, 0, 0, 0, 0, 0]
		self.lastsCookies = []
		self.cookie = 0
	
	def update(self):
		if self.isAlive is False:
			return
		
		outputs = self.neuralNet.update(self.inputs)
		
		self.direction += (outputs[0] - 0.5) * 20
		self.speed = outputs[1] * 10
		
		rad = math.radians(self.direction - 90)
		x, y = self.position
		x += self.speed*math.sin(rad)
		y += self.speed*math.cos(rad)
		self.position = (x, y)

		self.edgesPoints = 	[[self.position[0] - self.sideWidth//2, self.position[1] - self.frontWidth//2],
							[self.position[0] - self.sideWidth//2, self.position[1] + self.frontWidth//2],
							[self.position[0] + self.sideWidth//2, self.position[1] + self.frontWidth//2],
							[self.position[0] + self.sideWidth//2, self.position[1] - self.frontWidth//2],
							[self.position[0] - self.sideWidth//2, self.position[1] - self.frontWidth//2]]

		aux = 0
		for p in self.edgesPoints:
			self.edgesPoints[aux] = utils.rotate(self.position, p, -self.direction)
			self.edgesPointsAprox[aux] = int(round(self.edgesPoints[aux][0])), int(round(self.edgesPoints[aux][1]))
			aux += 1
	
	def incrementFitness(self):
		self.cookie += 1
		self.fitness += self.cookie + (self.cookie*self.speed/10)
