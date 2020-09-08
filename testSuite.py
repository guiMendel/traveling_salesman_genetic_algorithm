import json
import time
from pprint import pprint
from definitions.geneticAlgorithm import PopulationGenerator, NaturalSelection
from definitions.presentation import Graphics

# ETAPA 1: LER OS DADOS
print('\nETAPA 1: LEITURA')
# ---------------------
# Distâncias
# as chaves estão em ordem alfabética, e cada par aparece somente uma vez. Assim eliminamos redundância
print('Leitura de "distances"', end='...')
with open("data/distances.json", "r") as read_file:
    distance = json.load(read_file)
print('OK')

# Coordenadas (somente utilizadas na apresentação)
print('Leitura de "coordinates"', end='...')
with open("data/coordinates.json", "r") as read_file:
    coordinates = json.load(read_file)
print('OK')

# Dicionário sigla -> nome
print('Leitura de "names"', end='...')
with open("data/names.json", "r") as read_file:
    name = json.load(read_file)
print('OK')
# time.sleep(.3)

# ETAPA 2: INICIALIZAR POPULAÇÃO ALEATORIAMENTE
# ---------------------------------------------
# Configurações
print('\nETAPA 2: INICIALIZAÇÃO DE POPULAÇÃO')
population_size = 10
city_list = list(coordinates.keys())

print('Inicializando população', end='...')
population = PopulationGenerator(population_size, city_list).generatePopulation()
assert isinstance(population, list), f'ERRO: População gerada não é uma lista, e sim {type(population)}'
assert len(population)==population_size, 'ERRO: Tamanho da população não condiz com o tamanho solicitado'
print('OK')
# time.sleep(.3)

# ETAPA 3: CÁLCULO DA ADEQUAÇÃO DE CADA INDIVÍDUO
# -----------------------------------------------
# Cálculo
print('\nETAPA 3: ADEQUAÇÃO')
print('Inicializando modelo', end='...')
model = NaturalSelection(distance, population)
print('OK')

print('Calculando adequação', end='...')
fitnessScores = model.fitness()
assert len(fitnessScores)==population_size, 'ERRO: Tamanho da lista de valores de adequação não condiz com o tamanho da população'
print('OK')
# pprint(list(zip(population, fitnessScores)))
# time.sleep(.3)

# ETAPA 3.5: APRESENTAÇÃO EM TELA
# -------------------------------
print('\nETAPA 3.5: GRÁFICOS')
print('Inicializando gráficos', end='...')
graphics = Graphics(coordinates, name, 15, 8)
print('OK')

print('Adicionando nova rota', end='...')
graphics.addRoutePlot(population[0])
print('OK')

print('Gerando gráfico de custos', end='...')
graphics.generateCostPlot(fitnessScores)
print('OK')
# time.sleep(.3)

# ETAPA 4: SELEÇÃO DOS CASAIS
# ---------------------------
print('\nETAPA 4: SELEÇÃO')
print('Selecionando casais', end='...')
couples = model.selectMatingPool(2)
assert len(couples)==population_size, 'ERRO: Quantidade de casais gerados não condiz com o tamanho da população'
print('OK')
# pprint(list(zip(population,fitnessScores)))
# pprint(couples)
# time.sleep(.3)

# ETAPA 5: AVANÇAR GERAÇÃO
# ------------------------
print('\nETAPA 5: NOVA GERAÇÃO')

print('Realizando cruzamento teste', end='...')
result = model.testCrossover((0, 1))
assert sorted(result) == sorted(population[0]), f'ERRO: Cruzamento gerou indivíduo inválido.\nPais: {population[1], population[0]}\nFilho: {result}'
print('OK')

print('Gerando nova geração', end='...')
population = model.nextGeneration(couples)
assert len(population) == population_size, 'ERRO: Tamanho da nova geração está em desacordo com o configurado'
print('OK')
# time.sleep(.3)

# ETAPA 6: MUTAÇÕES
# -----------------
print('\nETAPA 6: MUTAÇÕES')
# Configuração
mutation_rate = 0.15

print('Realizando mutação teste', end='...')
genesBefore = population[0]
model.testMutateWithChance(0, 1.0)
assert sorted(genesBefore) == sorted(population[0]), f'ERRO: Mutação gerou indivíduo inválido.\nAntes: {genesBefore}\nDepois: {population[0]}'
print('OK')

print('Realizando mutação na população', end='...')
model.mutatePopulationWithChance(mutation_rate)
assert len(population) == population_size, 'ERRO: Tamanho da população após mutações está em desacordo com o configurado'
print('OK')
