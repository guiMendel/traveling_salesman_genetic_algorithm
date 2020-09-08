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
        """
        Gera uma nova população, com tamanho determinado pelo atributo de classe

        Returns
        -------
        Uma lista de lista de string, cada string identificando uma cidade
        """

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

    def getFittest(self, indices:list):
        """
        Retorna o índice do indivíduo com maior valor de adequação (menor fitness score) da população atual

        Returns
        -------
        O índice associado ao indivíduo de menor fitness score
        """

        # Obtém os fitness scores dos indivíduos selecionados e fica com o índice de menor resultado
        _, index = min((self.fitnessScores[index], index) for index in indices)
        return index

    def selectMatingPool(self, arenaSize:int):
        """
        Gera uma lista de casais da população, selecionados com base em
        seus valores de adequação

        Utiliza o método de torneio para selecionar os casais.

        Params
        ------
        arenaSize : int
            O número de indivíduos por batch de seleção. Quanto maior,
            menos aleatório é o resultado. Deve ser maior do que 1

        Returns
        -------
        Uma lista de tuplas com 2 inteiros: os índices dos indivíduos
        da população
        """

        assert hasattr(self, 'fitnessScores'), 'ERRO: impossível selecionar casais antes de realizar o cálculo de adequação'
        assert arenaSize > 1, 'ERRO: parâmetro "arenaSize" deve ser maior do que 1'
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

    def __crossover(self, couple:tuple):
            """
            Realiza cruzamento com o casal fornecido.

            Params
            ------
            couple : tuple (int)
                Uma tupla de tamanho 2 com os índices do indivíduos a
                serem cruzados
            
            Returns
            -------
            Uma lista de string: o novo indivíduo
            """

            # As rotas todas começam e terminam com BSB. Sendo assim, vamos retirar os BSBs dos pais e recolocar no filho.
            indA, indB = tuple(map(lambda idx : self.population[idx][1:-1], couple))
            length = len(indA)

            # Definimos o início e o fim da parcela de cromossomos que
            # vai ser transmitida do indivíduo A para o B
            geneA, geneB = [random.randint(0, length), random.randint(0, length)]
            # Garantimos que haverá algum cruzamento
            while (geneB == geneA or abs(geneB-geneA) == 9):
                geneB = random.randint(0, length)
            # Ordenamos de fato o começo e fim
            start, end = sorted((geneA, geneB))

            # Insere a sequência no gene B
            rawGenes = indB[:start] + indA[start:end] + indB[start:]
            # Remove os cromossomos duplicados
            genes = [cromossome for step, cromossome in enumerate(rawGenes) if cromossome not in rawGenes[:step]]
            return ["BSB"] + genes + ["BSB"]


    def nextGeneration(self, couples:list):
        """
        Realiza a operação genética de cruzamento com os casais
        fornecidos. Retorna e armazena a população gerada.

        Params
        ------
        couples : list ( tuple (int))
        
        Returns
        -------
        Uma lista de lista de string: a nova população gerada pelos
        cruzamentos.
        """

        self.population = list(map(self.__crossover, couples))
        return self.population

    def __mutateWithChance(self, index:int, rate:float):
        """
        Realiza mutações no indivíduo associado com o índice fornecido, com uma chance

        Retorna o resultado e atualiza o indivíduo no modelo interno.

        Params
        ------
        index : int
            Aponta para o indivíduo a ser sujeito a mutações
        rate : float
            A chance de cada cromossomo desse indivíduo ser mutado

        Returns
        -------
        Uma lista de string: o indivíduo após a mutação
        """

        # Ignoramos as cidades BSB no início e no final
        individual = self.population[index][1:-1]

        for geneA in range(len(individual)):
            # Aplicamos a chance
            if random.random() <= rate:
                # Encontramos outro índice, diferente do atual
                while True:
                    geneB = random.randint(0, len(individual)-1)
                    if geneB != geneA: break
                # Realizamos a troca
                individual[geneA], individual[geneB] = individual[geneB], individual[geneA]
        
        # Inserimos BSBs de volta
        individual = ["BSB"] + individual + ["BSB"]
        
        # Atualiza no modelo interno
        self.population[index] = individual
        return individual

    def mutatePopulationWithChance(self, rate:int):
        """
        Realiza mutações nos indivíduos da população com uma chance fornecida, retorna e armazena o resultado

        Params
        ------
        rate : int
            A probabilidade de cada cromossomo sofrer mutação
        
        Returns
        -------
        Uma lista de string: a nova população
        """

        return [self.__mutateWithChance(idx, rate) for idx in range(len(self.population))]
            
    def testCrossover(self, couple:tuple):
        return self.__crossover(couple)
    def testMutateWithChance(self, index:int, rate:float):
        return self.__mutateWithChance(index, rate)