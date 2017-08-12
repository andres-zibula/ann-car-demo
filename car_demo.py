from __future__ import division
import utils
import pygame
from pygame.locals import *
from car import Car
from geneticAlgorithm import GeneticAlgorithm 


class Game(object):
	
	def __init__(self, numCars):
		self.numCars = numCars
		self.cars = []
		
		self.walls = ((1256, 269), (1157, 267), (1050, 187), (862, 164), (744, 352), (614, 338), (495, 169), (318, 164), (223, 366), (12, 356), (10, 451), (291, 465), (404, 267), (566, 465), (817, 472), (942, 272), (1037, 294), (1124, 375), (1262, 380), (1256, 269))
		#self.cookies are the lines in purple, the word cookies comes from giving cookies to dogs as rewards when they behavior good (we assume that cars can eat cookies in some way xD)
		self.cookies = (((1159, 268), (1149, 373)), ((1144, 256), (1103, 358)), ((1077, 330), (1120, 239)), ((1094, 218), (1047, 303)), ((1025, 292), (1058, 192)), ((1015, 181), (998, 285)), ((964, 278), (970, 178)), ((943, 272), (906, 170)), ((857, 171), (931, 288)), ((915, 316), (829, 216)), ((806, 250), (890, 353)), ((874, 381), (784, 286)), ((766, 318), (852, 411)), ((834, 443), (751, 340)), ((806, 472), (743, 352)), ((753, 469), (719, 351)), ((701, 467), (697, 348)), ((660, 343), (664, 466)), ((631, 340), (619, 465)), ((572, 465), (612, 335)), ((537, 429), (593, 311)), ((575, 281), (501, 386)), ((469, 350), (556, 253)), ((533, 223), (444, 316)), ((426, 298), (505, 186)), ((471, 169), (413, 278)), ((420, 168), (406, 270)), ((401, 271), (364, 167)), ((398, 277), (313, 175)), ((391, 290), (293, 216)), ((277, 254), (373, 321)), ((360, 343), (262, 283)), ((248, 314), (343, 372)), ((326, 402), (234, 339)), ((306, 439), (227, 359)), ((291, 465), (223, 365)), ((243, 462), (211, 365)), ((196, 461), (197, 364)), ((159, 459), (167, 365)), ((133, 360), (130, 457)), ((97, 456), (104, 359)), ((73, 359), (69, 453)), ((43, 449), (48, 359)), ((30, 356), (27, 452)))
		
		self.time = 0
		self.maxTime = 800
		self.deadCars = 0
		self.carPos = (1200, 320)
		
		for i in range(0, numCars):
			self.cars.append(Car(self.carPos))
		
		numWeights = self.cars[0].neuralNet.getNumberWeights()
		
		self.geneticAlgorithm = GeneticAlgorithm(numCars, numWeights)
		
		for i in range(0, numCars):
			self.cars[i].neuralNet.putWeights(self.geneticAlgorithm.population[i].genes)
		
		self.textSize = 32
		self.textsToDraw = []
	
	def initialize(self):
		# Initialise screen
		pygame.init()
		self.myfont = pygame.font.SysFont("Comic Sans MS", self.textSize)
		self.screen = pygame.display.set_mode((1280, 720))
		pygame.display.set_caption('Car Demo - Zibu')
		clock = pygame.time.Clock()
	
		# Fill background
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))
		
		# Event loop
		while 1:
			clock.tick(30)
			
			for event in pygame.event.get():
				if event.type == QUIT:
					return
				if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
					self.deadCars = self.numCars
			
			self.draw()
			self.update()
	
	def canBeUpdated(self, carNumber):
		if self.time % 2 == 0:
			if carNumber % 2 == 0:
				return True
		else:
			if carNumber % 2 != 0:
				return True
		return False
	
	def handleCollisions(self):
		carNumber = 0
		for car in self.cars:
			if car.isAlive:
				car.update()
				if self.canBeUpdated(carNumber):
					rayPoints = [[], [], [], [], [], [], []]
					car.rayPoints = [[], [], [], [], [], [], []]
					
					for i in range(0, len(self.walls)-1):
						for j in range(0, len(car.edgesPointsAprox)-1):
							if utils.intersect(car.edgesPointsAprox[j], car.edgesPointsAprox[j+1], self.walls[i], self.walls[i+1]):
								if car.isAlive:
									car.isAlive = False
									self.deadCars += 1
								break
						
						points = utils.lineRayIntersectionPoint(car.position, (car.leftPoint[0] - car.position[0], car.leftPoint[1] - car.position[1]), self.walls[i], self.walls[i+1])
						if points:
							rayPoints[0] += points
						points = utils.lineRayIntersectionPoint(car.position, (car.frontLeft2Point[0] - car.position[0], car.frontLeft2Point[1] - car.position[1]), self.walls[i], self.walls[i+1])
						if points:
							rayPoints[1] += points
						points = utils.lineRayIntersectionPoint(car.position, (car.frontLeftPoint[0] - car.position[0], car.frontLeftPoint[1] - car.position[1]), self.walls[i], self.walls[i+1])
						if points:
							rayPoints[2] += points
						points = utils.lineRayIntersectionPoint(car.position, (car.frontPoint[0] - car.position[0], car.frontPoint[1] - car.position[1]), self.walls[i], self.walls[i+1])
						if points:
							rayPoints[3] += points
						points = utils.lineRayIntersectionPoint(car.position, (car.frontRightPoint[0] - car.position[0], car.frontRightPoint[1] - car.position[1]), self.walls[i], self.walls[i+1])
						if points:
							rayPoints[4] += points
						points = utils.lineRayIntersectionPoint(car.position, (car.frontRight2Point[0] - car.position[0], car.frontRight2Point[1] - car.position[1]), self.walls[i], self.walls[i+1])
						if points:
							rayPoints[5] += points
						points = utils.lineRayIntersectionPoint(car.position, (car.rightPoint[0] - car.position[0], car.rightPoint[1] - car.position[1]), self.walls[i], self.walls[i+1])
						if points:
							rayPoints[6] += points
					
					for i in range(0, len(rayPoints)):
						if rayPoints[i]:
							index = 0
							minDist = utils.distance(rayPoints[i][0], car.position)
							for j in range(0, len(rayPoints[i])):
								dist = utils.distance(rayPoints[i][j], car.position)
								if dist < minDist:
									minDist = dist;
									index = j
							car.inputs[i] = minDist
							car.rayPoints[i] = int(round(rayPoints[i][index][0])), int(round(rayPoints[i][index][1]))
						else:
							car.rayPoints[i] = (0, 0)
					
					car.inputs = [float(i)/max(car.inputs) for i in car.inputs]
					
					for i in range(0, len(self.cookies)):
						for j in range(0, len(car.edgesPointsAprox)-1):
							if utils.intersect(car.edgesPointsAprox[j], car.edgesPointsAprox[j+1], self.cookies[i][0], self.cookies[i][1]):
								f = lambda a,b: a if (a > b) else b
								maxCookie = -1
								if car.lastsCookies:
									maxCookie = reduce(f, car.lastsCookies)
								if i not in car.lastsCookies and i > maxCookie:
									car.lastsCookies.append(i)
									car.incrementFitness()
									if len(car.lastsCookies) > 5:
										car.lastsCookies.pop(0)
			carNumber += 1
	
	def draw(self):
		self.screen.blit(self.background, (0, 0))
		
		
		pygame.draw.lines(self.screen, (0, 0, 0), False, self.walls, 3)
		
		for wall in self.cookies:
			pygame.draw.lines(self.screen, (150, 150, 255), False, wall, 1)
		
		for car in self.cars:
			if car.isAlive:
				pygame.draw.lines(self.screen, (0, 255, 0), False, car.edgesPointsAprox, 2)
				
				for point in car.rayPoints:
					if point:
						pygame.draw.circle(self.screen, (150, 150, 150), point, 3)
						pygame.draw.lines(self.screen, (150, 150, 150), False, [car.position, point], 1)
			else:
				pygame.draw.lines(self.screen, (255, 0, 0), False, car.edgesPointsAprox, 2)
		
		for i in range(0, len(self.textsToDraw)):
			label = self.myfont.render(self.textsToDraw[i], 1, (0,0,0))
			self.screen.blit(label, (0, 50 + i*self.textSize))

		
		pygame.display.flip()
		
	def update(self):
		self.handleCollisions()
		
		if(self.time >= self.maxTime or self.deadCars >= self.numCars):
			self.deadCars = 0
			self.time = 0
			self.geneticAlgorithm.update2()
			for i in range(0, self.numCars):
				self.cars[i].reset(self.carPos)
				self.cars[i].neuralNet.putWeights(self.geneticAlgorithm.population[i].genes)
		
		for i in range(0, len(self.cars)):
			self.geneticAlgorithm.population[i].fitness = self.cars[i].fitness
		
		self.time += 1
		self.geneticAlgorithm.calcFitness()
		
		self.textsToDraw = []
		self.textsToDraw.append("Generation: " + str(self.geneticAlgorithm.generationNum))
		self.textsToDraw.append("Avg Fitness: " + str(int(round(self.geneticAlgorithm.avgFitness))))
		self.textsToDraw.append("Best Fitness: " + str(int(round(self.geneticAlgorithm.bestFitness))))
		self.textsToDraw.append("Game Time: " + str(self.time) + "/" + str(self.maxTime))

def main():
	game = Game(24)
	game.initialize()

if __name__ == '__main__': main()
