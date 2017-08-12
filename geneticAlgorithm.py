import random

class Genome(object):
	def __init__(self, genes = [], fitness = 0):
		self.fitness = fitness
		self.genes = genes
	
	def __lt__(self, genome):
		return self.fitness < genome.fitness

class GeneticAlgorithm(object):
	def __init__(self, popSize, numOfGenes):
		self.population = []
		self.popSize = popSize
		self.numOfGenes = numOfGenes
		self.totalFitness = 0
		self.bestFitness = 0
		self.worstFitness = 0
		self.avgFitness = 0
		self.fittestGenome = None
		self.mutationRate = 0.1
		self.crossoverRate = 1.0
		self.generationNum = 0
		
		for i in range(0, popSize):
			self.population.append(Genome())
			
			for j in range(0, self.numOfGenes):
				self.population[i].genes.append(random.uniform(-1.0, 1.0))
	
	def mutate(self, genome):
		for i in range(0, len(genome.genes)):
			if random.uniform(0.0, 1.0) < self.mutationRate:
				genome.genes[i] += random.uniform(-1.0, 1.0) * 0.3
				if genome.genes[i] < -1.0:
					genome.genes[i] = -1.0
				elif genome.genes[i] > 1.0:
					genome.genes[i] = 1.0
	
	def getGenomeByRoulette(self):
		r = random.uniform(0, self.totalFitness)
		
		actualTotalFitness = 0
		for i in range(0, self.popSize):
			actualTotalFitness += self.population[i].fitness
			
			if actualTotalFitness >= r:
				return self.population[i]
		
		return None
	
	def getGenomeByTournament(self):
		tournamentSize = 4;
		
		num = random.randint(0, len(self.population) - 1)
		fittest = self.population[num]
		
		for i in range(0, tournamentSize):
			num = random.randint(0, len(self.population) - 1)
			if self.population[num].fitness > fittest.fitness:
				fittest = self.population[num]
		
		return fittest;
	
	def crossover(self, parent1, parent2):
		if random.uniform(0.0, 1.0) < self.crossoverRate:
			p = random.randint(0, self.numOfGenes - 1)
			child = Genome()
			
			for i in range(0, p):
				child.genes[i] = parent1.genes[i]
			for i in range(p, self.numOfGenes):
				child.genes[i] = parent2.genes[i]
			
			return child
		else:
			if random.random() > 0.5:
				return parent1
			else:
				return parent2
	
	def calcFitness(self):
		self.totalFitness = 0
		self.bestFitness = 0
		self.worstFitness = 0
		self.avgFitness = 0
		
		self.worstFitness = self.population[0].fitness
		for i in range(0, self.popSize):
			self.totalFitness += self.population[i].fitness
			if self.population[i].fitness > self.bestFitness:
				self.bestFitness = self.population[i].fitness
				self.fittestGenome = self.population[i]
			if self.population[i].fitness < self.worstFitness:
				self.worstFitness = self.population[i].fitness
		
		self.avgFitness = self.totalFitness / self.popSize
	
	def update(self):
		self.calcFitness()
		
		newPopulation = []
		bestPopulation = self.population[:]
		bestPopulation.sort(reverse=True)
		
		n = 4
		if self.popSize < n:
			n = self.popSize
		
		for i in range(0, n): #best n elitism
			newPopulation.append(bestPopulation[i])
			newPopulation.append(bestPopulation[i])
		newPopulation.append(bestPopulation[0])
		
		while len(newPopulation) < self.popSize:
			parent1 = self.getGenomeByTournament()
			parent2 = self.getGenomeByTournament()
			
			child = self.crossover(parent1, parent2)
			
			self.mutate(child)
			
			newPopulation.append(child)
		
		self.population = newPopulation
		self.generationNum += 1
		
		for genome in self.population:
			genome.fitness = 0
	
	def update2(self):
		self.calcFitness()
		
		newPopulation = []
		bestPopulation = self.population[:]
		bestPopulation.sort(reverse=True)
		
		newPopulation.append(bestPopulation[0])
		newPopulation.append(bestPopulation[1])
		newPopulation.append(bestPopulation[2])
		
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[1]))
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[1]))
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[1]))
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[1]))
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[2]))
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[2]))
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[2]))
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[2]))
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[3]))
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[3]))
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[3]))
		newPopulation.append(self.crossover(bestPopulation[0], bestPopulation[3]))
		
		newPopulation.append(self.crossover(bestPopulation[1], bestPopulation[2]))
		newPopulation.append(self.crossover(bestPopulation[1], bestPopulation[2]))
		newPopulation.append(self.crossover(bestPopulation[1], bestPopulation[3]))
		newPopulation.append(self.crossover(bestPopulation[1], bestPopulation[3]))

		newPopulation.append(self.crossover(bestPopulation[2], bestPopulation[3]))
		newPopulation.append(self.crossover(bestPopulation[2], bestPopulation[3]))
		
		for i in range(1, len(newPopulation)):
			self.mutate(newPopulation[i])
		
		while len(newPopulation) < self.popSize:
			parent1 = self.getGenomeByTournament()
			parent2 = self.getGenomeByTournament()
			
			child = self.crossover(parent1, parent2)
			
			self.mutate(child)
			
			newPopulation.append(child)
		
		self.population = newPopulation
		self.generationNum += 1
		
		for genome in self.population:
			genome.fitness = 0
