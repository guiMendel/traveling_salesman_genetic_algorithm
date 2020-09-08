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
time.sleep(1)

# ETAPA 2: INICIALIZAR POPULAÇÃO ALEATORIAMENTE
# ---------------------------------------------
# Configurações
print('\nETAPA 2: INICIALIZAÇÃO DE POPULAÇÃO')
population_size = 10
city_list = coordinates.keys()
print('Inicializando população', end='...')
population = PopulationGenerator(population_size, city_list).generatePopulation()
print('OK')
time.sleep(1)

# ETAPA 3: CÁLCULO DA ADEQUAÇÃO DE CADA INDIVÍDUO
# -----------------------------------------------
# Cálculo
print('\nETAPA 3: ADEQUAÇÃO')
print('Inicializando modelo', end='...')
model = NaturalSelection(distance, population)
print('OK')
print('Calculando adequação', end='...')
fitnessScores = model.fitness()
print('OK')
# pprint(list(zip(population, fitnessScores)))
time.sleep(1)

# ETAPA 4: SELEÇÃO DOS CASAIS
# ---------------------------
print('\nETAPA 4: SELEÇÃO')
print('Selecionando casais', end='...')
couples = model.selectMatingPool(2)
print('OK')
# pprint(list(zip(population,fitnessScores)))
# pprint(couples)
time.sleep(1)

# ETAPA 5: AVANÇAR GERAÇÃO
# ------------------------
print('\nETAPA 5: NOVA GERAÇÃO')


graphics = Graphics(coordinates, name, 15, 8)