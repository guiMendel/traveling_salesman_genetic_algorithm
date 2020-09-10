import json
import time
from pprint import pprint
from definitions.geneticAlgorithm import PopulationGenerator, NaturalSelection
from definitions.presentation import Graphics

# Configurações
population_size = 100
mutation_rate = 0.1
arena_size = 40
graphicsWidth = 15
graphicsHeight = 8
generations = 25
routes_to_plot = 1

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
city_list = list(coordinates.keys())

# ETAPA 2: INICIALIZAR POPULAÇÃO ALEATORIAMENTE
# ---------------------------------------------
# Configurações
print('\nETAPA 2: INICIALIZAÇÃO DE POPULAÇÃO')

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
fitnessScores = model.getFitness()
assert len(fitnessScores)==population_size, 'ERRO: Tamanho da lista de valores de adequação não condiz com o tamanho da população'
print('OK')
# pprint(list(zip(population, fitnessScores)))
# time.sleep(.3)

# ETAPA 3.5: APRESENTAÇÃO EM TELA
# -------------------------------
print('\nETAPA 3.5: GRÁFICOS')
# Configuração

print('Inicializando gráficos', end='...')
graphics = Graphics(0, 0, coordinates, name, graphicsWidth, graphicsHeight)
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
# Configuração

print('Selecionando casais', end='...')
couples = model.selectMatingPool(arena_size, population_size)
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
population = model.breed(couples)
assert len(population) == population_size, 'ERRO: Tamanho da nova geração está em desacordo com o configurado'
print('OK')
# time.sleep(.3)

# ETAPA 6: MUTAÇÕES
# -----------------
print('\nETAPA 6: MUTAÇÕES')
# Configuração

print('Realizando mutação teste', end='...')
genes_before = population[0]
model.testMutateWithChance(0, 1.0)
genes_after = model.population[0]
assert sorted(genes_before) == sorted(population[0]), f'ERRO: Mutação gerou indivíduo inválido.\nAntes: {genes_before}\nDepois: {population[0]}'
assert genes_before != genes_after, 'ERRO: Mutação obrigatória não mudou nada'

genes_before = model.population[0]
model.testMutateWithChance(0, 0.0)
genes_after = model.population[0]
assert genes_before == genes_after, 'ERRO: Mutação proibida mudou algo'

print('OK')

print('Realizando mutação na população', end='...')
model.mutatePopulationWithChance(mutation_rate)
assert len(population) == population_size, 'ERRO: Tamanho da população após mutações está em desacordo com o configurado'
print('OK')

# ETAPA 7: GERAÇÕES AUTOMÁTICAS
# -----------------------------
print('\nETAPA 7: GERAÇÕES AUTOMÁTICAS')
# Configuração

print('Uma iteração automática de geração', end='...')
population_before = population
population = model.testAdvanceGeneration(arena_size, mutation_rate, True)
assert len(population)==population_size, 'ERRO: Tamanho da população após geração automática está em desacordo com o configurado'
assert population_before!=population, 'ERRO: Geração automática falhou em alterar a população'
print('OK')

print('Múltiplas iterações automáticas de geração', end='...')
population_before = population
the_fittest = model.geneticAlgorithm(generations, arena_size, mutation_rate, True)
population = model.getPopultaion()
assert len(population)==population_size, 'ERRO: Tamanho da população após múltiplas gerações automáticas está em desacordo com o configurado'
assert population_before!=population, 'ERRO: Gerações automáticas falharam em alterar a população'
print('OK')
# print(f'Indivíduo final gerado: {the_fittest}')

# ETAPA 8: GERAÇÕES AUTOMÁTICAS COM REPORTAGEM DE PROGRESSO
# ---------------------------------------------------------
print('\nETAPA 8: GERAÇÕES AUTOMÁTICAS COM REPORTAGEM DE PROGRESSO')
# Configuração
model = NaturalSelection(distance, PopulationGenerator(population_size, city_list).generatePopulation())
graphics = Graphics(routes_to_plot, generations, coordinates, name, graphicsWidth, graphicsHeight)

print('Múltiplas iterações automáticas de geração', end='...')
# Observer
model.subscribe(graphics.receiveData)
# Salva o custo antigo
old_cost = model.getFitness()[model.getFittest()]

the_fittest = model.geneticAlgorithm(generations, arena_size, mutation_rate, True)
# Gera o gráfico
graphics.generateGraph()
# Pega os custos registrados
generation_costs = graphics.getGenerationCosts()
# Pega o custo final do modelo
final_cost = model.getFitness()[model.getFittest()]
assert len(generation_costs) == generations + 1, f'ERRO: A camada de apresentação registrou uma quantidade de gerações diferente da definida.\nDefinida: {generations} + geração inicial\nRegistrada:{len(generation_costs)}'
assert generation_costs[-1] == final_cost, f'ERRO: O custo final registrado na apresentação difere do modelo interno.\nCustos registrados: {generation_costs}\nCusto no modelo: {final_cost}'
assert generation_costs[0] == old_cost, f'ERRO: O custo inicial registrado na apresentação difere do modelo interno\nCustos registrados: {generation_costs}\nCusto no modelo: {old_cost}'
assert graphics.getNumberPlottedRoutes() == routes_to_plot, f'ERRO: A quantidade de rotas impressas difere da solicitada\nImpressas: {graphics.getNumberPlottedRoutes()}\nSolicitadas: {routes_to_plot}'
# print(f'Melhor indivíduo: {the_fittest}\nCusto: {final_cost}')
graphics.display()
print('OK')
