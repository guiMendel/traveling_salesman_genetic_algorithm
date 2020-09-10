import json
import time
from pprint import pprint
from definitions.geneticAlgorithm import PopulationGenerator, NaturalSelection
# from definitions.presentation import Graphics

# Leitura de arquivos
with open("data/distances.json", "r") as read_file:
    distance = json.load(read_file)
with open("data/coordinates.json", "r") as read_file:
    coordinates = json.load(read_file)
with open("data/names.json", "r") as read_file:
    name = json.load(read_file)

# Pega lista de cidades
city_list = list(coordinates.keys())


# Definimos uma população controlada
population = [
    ['BSB', 'BA', 'CARAC'],                 # 74
    ['BSB', 'LIMA', 'BOG', 'CARAC'],        # 61
    ['BSB', 'BOG', 'SP', 'POA', 'BSB']      # 104
    # ['BSB', 'BH', 'RJ', 'SP', 'POA', 'BA', 'SANT', 'LIMA', 'BOG', 'CARAC', 'BSB']
 ]

# Inicia modelo
model = NaturalSelection(distance, population)

# Cálculo de custo de rota
# print(model.testGetRouteCost(population[0]), model.testGetRouteCost(population[1]), model.testGetRouteCost(population[2]))
cost = model.testGetRouteCost(population[0])
assert cost == 74, 'ERRO: Erro no cálculo do custo rota'
cost = model.testGetRouteCost(population[1])
assert cost == 61, 'ERRO: Erro no cálculo do custo rota'
cost = model.testGetRouteCost(population[2])
assert cost == 104, 'ERRO: Erro no cálculo do custo rota'
# print(model.testGetRouteCost(population[3]))

# Cáluclo dos custos da população
cost = model.getFitness()
# print(cost)
assert cost == [74, 61, 104], 'ERRO: Erro no cálculo dos custos da população'
assert cost == model.getFitness(), 'ERRO: Função de adequação tem resultados inconsistentes'

# Seleção de melhor indivíduo
# print(model.getFittest())
assert model.getFittest() == 1, 'ERRO: getFittest retornou resultado incorreto'
assert model.getFittest([0, 2]) == 0, 'ERRO: getFittest retornou resultado incorreto'
assert model.getFittest([2]) == 2, 'ERRO: getFittest retornou resultado incorreto'

# Amostra de população
model.population = []
for _ in range(10):
    model.population.append(['BSB'])
# print(model.population)
# print(model.testSamplePopulation(range(len(model.population)), 3, []))
sample = model.testSamplePopulation(range(len(model.population)), 3, [])
assert len(sample) == 3 and len(set(sample)) == 3, 'ERRO: Tamanho da amostra é incorreto ou possui elementos repetidos'
assert all([isinstance(element, int) for element in sample]), 'ERRO: Tipos de elementos incorretos'
sample = model.testSamplePopulation(range(len(model.population)), 10, [0])
# print(sample)
assert 0 not in sample, 'ERRO: Amostra possui elemento excluído'

# Selecionar casais
model.population = PopulationGenerator(5, city_list).generatePopulation()
model.getFitness()
# pprint(sorted((c, x) for x, c in enumerate(model.getFitness())))
couples = model.selectMatingPool(2, 5)
# print(couples)

# Cruzamento
# son = model.testCrossover((0, 1))
# pprint(model.population[0])
# pprint(model.population[1])
# pprint(son)

# Cruzamento da população
# pprint(couples[0])
# pprint(list(enumerate(model.population)))
model.breed(couples)
# print('Depois de cruzar:')
# pprint(model.population[0])

# Mutação individual
before = model.population[0]
model.testMutateWithChance(0, .1)
after = model.population[0]
print(before)
print(after)