import matplotlib.pyplot as plt
from random import random

class Graphics:
    """
    Tem por função lidar com a apresentação dos gráficos em tela
    """
    def __init__(self, coordinates, names, width, height):
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

    def __randomColor(self, alpha):
        return (random(), random(), random(), alpha)

    def addRoutePlot(self, route):
        """
        Adiciona uma rota ao gráfico de rotas
        """
        # Geramos uma nova lista com as coordenadas de cada cidade da lista
        routeCoordinates = [self.coordinates[city] for city in route]
        # Separamos essa lista em duas, para inseri-las no plot (utilização do 'splat' operator)
        routeX, routeY = zip(*routeCoordinates)

        self.map.plot(routeX, routeY, color=self.__randomColor(0.6), linestyle='dotted', linewidth=2)

    def generateCostPlot(self, cost):
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