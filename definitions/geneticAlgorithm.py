import random
from pprint import pprint
class PopulationGenerator:
    """
    Utilizada para gerar novas populações para iniciar o algoritmo genético.
    """
    
    def __init__(self, size, city_list):
        self.city_list = list(city_list)
        # Começamos e terminamos em BSB, logo as cidades do meio não podem incluir BSB
        self.city_list.remove("BSB")
        self.size = size

    def __generateRoute(self):
        midCities = random.sample(self.city_list, len(self.city_list))
        return ["BSB"] + midCities + ["BSB"]

    def generatePopulation(self):

        population = []
        for _ in range(self.size):
            population.append(self.__generateRoute())
        
        return population

class NaturalSelection:
    """
    Realiza todos os processos que pertencem à fase de evolução de uma população
    """

    def __init__(self, distance, population):
        """
        Parameters
        ----------
        distance : dict (dict (str=>int))
            Um dicionário que associa cada par de cromossomo à um custo (a distância entre as cidades)
        """
        self.distance = distance
        self.population = population

    def __getRouteCost(self, route):
        """
        Calcula o valor de adequação de um único indivíduo
        """
        cost = 0
        # Itera pela lista em pares
        for cityA, cityB in zip(route, route[1:]):
            # Ordena para poder acessar "distance" adequadamente
            (cityA, cityB) = sorted([cityA, cityB])
            cost += self.distance[cityA][cityB]
        return cost

    def fitness(self):
        """
        Calcula, armazena e retorna o valor de adequação de cada indivíduo da população
        
        Returns
        -------
        Uma lista de custos por indivíduo na mesma ordem da população recebida
        """
        fitnessScores = []

        for individual in self.population:
            fitnessScores.append(self.__getRouteCost(individual))

        self.fitnessScores = fitnessScores
        return fitnessScores

    def getFittest(self, indices):
        """
        Retorna o índice do indivíduo com maior valor de adequação (menor fitness score) da população atual

        Returns
        -------
        O índice associado ao indivíduo de menor fitness score
        """

        # Obtém os fitness scores dos indivíduos selecionados e fica com o índice de menor resultado
        _, index = min((self.fitnessScores[index], index) for index in indices)
        return index

    def selectMatingPool(self, arenaSize):
        """
        Gera uma lista de casais da população, selecionados com base em seus valores de adequação

        Utiliza o método de torneio para selecionar os casais.

        Params
        ------
        arenaSize : int
            O número de indivíduos por batch de seleção. Quanto maior,
            menos aleatório é o resultado. Deve ser maior do que 1

        Returns
        -------
        Uma lista de tuplas com 2 indivíduos da população
        """

        if (not hasattr(self, 'fitnessScores')):
            print('ERRO: impossível selecionar casais antes de realizar o cálculo de adequação')
            return
        if (arenaSize < 2):
            print('ERRO: arenaSize deve ser maior do que 1')
            
        # Pega os índices da população
        populationIndices = range(len(self.population))
        
        # Um função simples que pega alguns índices da população e os alimenta para a função getFittest
        # O parâmetro especifica um índice que não deve ser selecionado
        # Retorna um índice da população
        selectParent = lambda exclude : self.getFittest(x for x in random.sample(populationIndices, arenaSize) if x!= exclude)

        couples = []
        for _ in populationIndices:
            parentA = selectParent(None)
            parentB = selectParent(parentA)
                
            couples.append((parentA, parentB))
        return couples