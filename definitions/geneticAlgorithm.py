import random
class PopulationGenerator:
    """
    Utilizada para gerar novas populações para iniciar o algoritmo genético.
    """
    
    def __init__(self, size):
        self.size = size

    def generateRoute(self, city_list):
        return random.sample(city_list, len(city_list))

    def generatePopulation(self, city_list):
        population = []
        for _ in range(self.size):
            population.append(self.generateRoute(city_list))
        return population

class NaturalSelection:
    """
    Realiza todos os processos que pertencem à fase de evolução de uma população
    """

    def __init__(self, distance):
        """
        Parameters
        ----------
        distance : dict (dict (str=>int))
            Um dicionário que associa cada par de cromossomo à um custo (a distância entre as cidades)
        """
        self.distance = distance

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

    def fitness(self, population):
        """
        Calcula e retorna o valor de adequação de cada indivíduo da população

        Parameters
        ----------
        population : list (str)
            A lista da população
        
        Returns
        -------
        Uma lista de custos por indivíduo na mesma ordem da população recebida
        """
        fitnessValues = []

        for individual in population:
            fitnessValues.append(self.__getRouteCost(individual))

        return fitnessValues
