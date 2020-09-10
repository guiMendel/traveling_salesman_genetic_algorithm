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
        mid_cities = random.sample(self.city_list, len(self.city_list))
        return ["BSB"] + mid_cities + ["BSB"]

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

    # Implementação do Padrão de Projeto Observer
    observers = []

    def subscribe(self, observer_function):
        self.observers.append(observer_function)

    def notifyAll(self, message):
        # print(f'Notifying {len(self.observers)} observers...')
        for observer_function in self.observers:
            observer_function(message)

    def getPopultaion(self):
        return self.population

    def __getRouteCost(self, route:list):
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

    def getFitness(self):
        """
        Calcula, armazena e retorna o valor de adequação de cada indivíduo da população
        
        Returns
        -------
        Uma lista de custos por indivíduo na mesma ordem da população recebida
        """
        fitness_scores = []

        for individual in self.population:
            fitness_scores.append(self.__getRouteCost(individual))

        self.fitness_scores = fitness_scores
        return fitness_scores

    def getFittest(self, indices:list = []):
        """
        Retorna o índice do indivíduo com maior valor de adequação (menor fitness score) da população atual

        Returns
        -------
        O índice associado ao indivíduo de menor fitness score
        """

        # Obtém os fitness scores dos indivíduos selecionados e fica com o índice de menor resultado
        if not indices:
            indices = range(len(self.population))
        
        _, index = min((self.fitness_scores[index], index) for index in indices)
        return index

    def __samplePopulation(self, population_indices:list, sample_size:int, exclude:int):
        """
        Um função simples que pega alguns índices da população

        Params
        ------
        population_indices : list
            Lista da qual se fará uma amostra
        sample_size : int
            Tamanho da amostra pretendida
        exclude : int
            Indica quais índices não devem estar inclusos na amostra

        Return
        ------
        Uma lista: a amostra da população
        """

        return [x for x in random.sample(population_indices, sample_size) if x not in exclude]

    def selectMatingPool(self, arena_size:int, pool_size:int):
        """
        Gera uma lista de casais da população, selecionados com base em
        seus valores de adequação

        Utiliza o método de torneio para selecionar os casais.

        Params
        ------
        arena_size : int
            O número de indivíduos por batch de seleção. Quanto maior,
            menos aleatório é o resultado. Deve ser maior do que 1

        pool_size : int
            Quantos casais deve gerar

        Returns
        -------
        Uma lista de tuplas com 2 inteiros: os índices dos indivíduos
        da população
        """

        assert hasattr(self, 'fitness_scores'), 'ERRO: impossível selecionar casais antes de realizar o cálculo de adequação'
        assert arena_size > 1, 'ERRO: parâmetro "arenaSize" deve ser maior do que 1'
        # Pega os índices da população
        population_indices = range(len(self.population))
        
        # Um função simples que pega alguns índices da população e os alimenta para a função getFittest
        # O parâmetro especifica um índice que não deve ser selecionado
        # Retorna um índice da população
        selectParent = lambda exclude : self.getFittest(self.__samplePopulation(population_indices, arena_size, [exclude]))

        couples = []
        for _ in range(pool_size):
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
            # print(length)
            # pprint(indA)
            # pprint(indB)

            # Definimos o início e o fim da parcela de cromossomos que
            # vai ser transmitida do indivíduo A para o B
            geneA, geneB = [random.randint(0, length), random.randint(0, length)]
            # Garantimos que haverá algum cruzamento
            # print(geneA, geneB)
            while geneB == geneA or abs(geneB-geneA) == 9:
                geneB = random.randint(0, length)
            # Ordenamos de fato o começo e fim
            start, end = sorted((geneA, geneB))
            # print(start, end)

            # # Insere a sequência no gene B
            # raw_genes = indB[:start] + indA[start:end] + indB[start:]
            # # Remove os cromossomos duplicados
            # genes = [cromossome for step, cromossome in enumerate(raw_genes) if cromossome not in raw_genes[:step]]

            genes_slice = indA[start:end]
            genes = genes_slice + [gene for gene in indB if gene not in genes_slice]

            return ["BSB"] + genes + ["BSB"]

    def breed(self, couples:list):
        """
        Realiza a operação genética de cruzamento com os casais
        fornecidos. Retorna a população gerada.

        O melhor indivíduo da geração passada permanece nesta.

        Params
        ------
        couples : list ( tuple (int))
        
        Returns
        -------
        Uma lista de lista de string: a nova população gerada pelos
        cruzamentos.
        """


        return list(map(self.__crossover, couples))

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
        # print(individual)

        for geneA in range(len(individual)):
            # Aplicamos a chance
            if random.random() < rate:
                # Encontramos outro índice, diferente do atual
                while True:
                    geneB = random.randint(0, len(individual)-1)
                    if geneB != geneA: break
                # Realizamos a troca
                individual[geneA], individual[geneB] = individual[geneB], individual[geneA]
        
        # Inserimos BSBs de volta
        # print(individual)
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

    def __advanceGeneration(self, arena_size:int, mutation_rate:float, leak_alfa:bool):
        """
        Realiza uma iteração do algoritmo genético

        Realiza: avaliação de adequação, seleção de casais, cruzamento e mutação. Armazena e retorna a população resultado.

        Returns
        -------
        Uma lista de string: a nova população.
        """

        # Etapa de avaliação
        self.getFitness()

        # Vazamento do melhor indivíduo
        if leak_alfa:
            alfa = self.population[self.getFittest()]

        # Etapa de seleção de casais
        couples = self.selectMatingPool(arena_size, len(self.population) - int(leak_alfa))

        # Etapa de cruzamento
        self.population = self.breed(couples)

        # Etapa de mutação
        self.mutatePopulationWithChance(mutation_rate)
        
        # Insere novamente o alfa
        if leak_alfa:
            self.population.append(alfa)
        
        return self.population

    def geneticAlgorithm(self, population_size:int, city_list:int, generations:int, arena_size:int, mutation_rate:float, leak_alfa:bool):
        """
        Executa o algoritmo genético sobre a população do modelo interno com um número fornecido de gerações

        Params
        ------
        generations : int
            Define quantas gerações devem ser executadas
        
        Returns
        -------
        Uma lista de string: o melhor indivíduo obtido
        """


        # Uma função simples que notifica os observadores do progresso de cada geração
        reportProgress = lambda gen : self.notifyAll({ "generation": gen, "best_cost": self.fitness_scores[self.getFittest()], "best_route": self.population[self.getFittest()]})

        self.getFitness()
        reportProgress(0)
        for generation in range(generations):
            self.__advanceGeneration(arena_size, mutation_rate, leak_alfa)
            self.getFitness()
            reportProgress(generation+1)
            
        the_fittest = self.population[self.getFittest()]

        return the_fittest
            
    def testAdvanceGeneration(self, arena_size:int, mutation_rate:float, leak_alfa:bool):
        return self.__advanceGeneration(arena_size, mutation_rate, leak_alfa)            
    def testCrossover(self, couple:tuple):
        return self.__crossover(couple)
    def testMutateWithChance(self, index:int, rate:float):
        return self.__mutateWithChance(index, rate)
    def testGetRouteCost(self, route:list):
        return self.__getRouteCost(route)
    def testSamplePopulation(self, population:list, sample_size:int, exclude:int):
        return self.__samplePopulation(population, sample_size, exclude)
