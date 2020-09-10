import matplotlib.pyplot as plt
from random import random

class Graphics:
    """
    Tem por função lidar com a apresentação dos gráficos em tela
    """
    def __init__(self, routes_to_display:int, generations:int, coordinates:dict, names:dict, width:float, height:float):
        self.fig = plt.figure(figsize=[width, height])
        
        self.map = self.fig.add_subplot(121)
        self.map.set_title("Mapa de Rotas")
        self.map.set_xticks([])
        self.map.set_yticks([])

        # As configurações desse axes são definidas posteriormente
        self.curve = self.fig.add_subplot(122)

        self.width = width
        self.height = height
        self.coordinates = coordinates
        self.name = names
        # Calcula qual o intervalo de gerações que deve se passar antes de amostrar uma rota
        # Tira um do routes_to_display pois sempre imprime a última rota por padrão
        # Soma um em generations pois a geração 0 conta como uma extra
        if routes_to_display != 1:
            self.generations_per_plot = int((generations + 1)/max(routes_to_display - 1, 1))
        else:
            self.generations_per_plot = None

    """Armazena os custos de cada geração, para gerar o gráfico ao final"""
    generation_cost = []
    """Indica quantas rotas já foram impressas"""
    routes_plotted = 0

    def __randomColor(self, alpha:float):
        return (random()*0.4, random()*0.4, random()*0.4, alpha)

    def addRoutePlot(self, route):
        """
        Adiciona uma rota ao gráfico de rotas
        """

        # Pula se não houver rota
        if route is None:
            return
        # Incrementa o contador de rotas impressas
        self.routes_plotted += 1        
        # Geramos uma nova lista com as coordenadas de cada cidade da lista
        routeCoordinates = [self.coordinates[city] for city in route]
        # Separamos essa lista em duas, para inseri-las no plot (utilização do 'splat' operator)
        routeX, routeY = zip(*routeCoordinates)

        self.map.plot(routeX, routeY, color=self.__randomColor(0.6), linestyle='dotted', linewidth=4)

    def generateCostPlot(self, cost:list):
        """
        Gera o gráfico de custos

        Params
        ------
        cost : list (int)
            Uma lsita com os custos de cada indivíduo da população
        """
        self.curve.cla()
        self.curve.set_title("Evolucao de Custos")
        self.curve.set_ylabel("Custo")
        self.curve.set_xlabel("Geracao")
        self.curve.plot(cost)

    def display(self):
        """
        Apresenta os gráficos em tela
        """
        # Imprime as cidades
        coordinateValues = self.coordinates.values()
        coordX, coordY = zip(*coordinateValues)
        self.map.scatter(coordX, coordY, color="black")
        # Imprime o nome das cidades
        for city in self.name:
            x, y = self.coordinates[city]
            # Desloca um pouco para cima
            y -= self.height/5
            self.map.text(x, y, self.name[city][0])
        
        # figure = self.fig
        plt.show()

    # Para ser utilizada como observer com o sujeito Natural Selection
    def receiveData(self, message):
        # Destrincha a mensagem
        generation, cost, route = message["generation"], message["best_cost"], message["best_route"]

        # Armazena o custo de todas as gerações
        self.generation_cost.append(cost)


        # Já imprime a rota em intervalos predefinidos
        if self.generations_per_plot and generation % self.generations_per_plot == 0:
            self.addRoutePlot(route)
            self.last_route = None
        else:
            # Sempre armazena a última rota recebida
            self.last_route = route
    
    def generateGraph(self):
        # Imprime a última geração
        self.addRoutePlot(self.last_route)

        # Gera o gráfico de custo
        self.generateCostPlot(self.generation_cost)

    def getGenerationCosts(self):
        return self.generation_cost

    def getNumberPlottedRoutes(self):
        return self.routes_plotted
        