import json
from pprint import pprint
from definitions.geneticAlgorithm import PopulationGenerator, NaturalSelection

# ETAPA 1: LER OS DADOS
# ---------------------
# Distâncias
# as chaves estão em ordem alfabética, e cada par aparece somente uma vez. Assim eliminamos redundância
with open("data/distances.json", "r") as read_file:
    distance = json.load(read_file)
# Coordenadas (somente utilizadas na apresentação)
with open("data/coordinates.json", "r") as read_file:
    coordinates = json.load(read_file)
# Dicionário sigla -> nome
with open("data/names.json", "r") as read_file:
    name = json.load(read_file)

# ETAPA 2: INICIALIZAR POPULAÇÃO ALEATORIAMENTE
# ---------------------------------------------
# Configurações
population_size = 30
city_list = coordinates.keys()

population = PopulationGenerator(population_size).generatePopulation(city_list)

# ETAPA 3: CÁLCULO DA ADEQUAÇÃO DE CADA INDIVÍDUO
# -----------------------------------------------
# Cálculo
model = NaturalSelection(distance)
fitnessList = model.fitness(population)
# Apresentação


pprint(list(zip(population, fitnessList)))