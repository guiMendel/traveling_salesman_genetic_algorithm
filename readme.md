# Problema do Caixeiro Viajante com  Algoritmo Genético
Esta implementação soluciona uma instância do problema do caixeiro viajante, em que a rota começa e termina sempre na cidade de Brasília.

![example](https://i.ibb.co/Vq9MyQY/example.png)

## Como Executar
Basta ter a linguagem *python* instalada em sua máquina, navegar para a pasta do repositório via terminal e executar o seguinte comando:
```python
    python

## O Problema
Nesta instância do problema do caixeiro viajante, as rotas têm sempre exatamente 11 cidades, sendo a inicial e a final sempre a cidade de Brasília. As cidades intermediárias são uma permutação das cidades de *São Paulo, Lima, Bogotá, Rio de Janeiro, Santiago, Caracas, Buenos Aires, Porto Alegre e Belo Horizonte*.
## A Solução
O **Algoritmo Genético** é um algoritmo de busca inspirado na teoria da evolução darwiniana, em que uma *população* de soluções (cada solução é uma diferente rota) é sujeita a uma série de *operações genéticas*, assim resultando numa série de *gerações*.

Cada *indivíduo* dessa população tem sua adequação avaliada para gerar um número, o **nível de adequação** *(fitness score)*.

Em cada geração, alguns indivíduos são selecionados para gerar a geração seguinte por meio das operações genéticas. Quanto mais adequado um indivíduo for, maior sua chance de seleção.

### A implementação
O algoritmo foi implementado na linguagem **Python 3.8.5**, de maneira bem modularizada e com uso extensivo de orientação a objetos.
> Foram utilizadas as bibliotecas *matplotlib*, *random*, *pprint* e *time*.

Nessa implementação, foram utilizadas três formas diferentes de reprodução: **cruzamento**, **mutação** e **elitismo**.

- Com o cruzamento, 2 indivíduos selecionados têm partes de suas rotas cruzadas para formar uma rota filho.
- Com a mutação, cada *gene* dessa rota filho (cada cidade) tem uma chance de sofrer uma alteração: nesse caso, uma troca com outro gene.
- Com o elitismo, o melhor indivíduo de uma geração passa automáticamente, intacto, para a geração seguinte.

A população inicial é gerada aleatoriamente.

O projeto é organizado em diferentes arquivos, e os dados das cidade foram armazenados em arquivos *json*.
![enter image description here](https://i.ibb.co/zJC4XXM/concept-model.png)
> Um diagrama ilustrando o procedimento adotado pelo programa
### Os Gráficos
Ao final da execução do código, dois gráficos são apresentados: um que ilustra a rota final obtida num mapa e outro que traça a evolução dos custos do *melhor indivíduo* de cada geração com o passar das gerações.

Os gráficos são apresentados pela biblioteca *matplotlib*.

A camada de apresentação do projeto se comunica com a camada lógica por meio do padrão de projeto *Observer*, que garante desacoplamento máximo entre as camadas.
## Resultados Obtidos
Todos os testes realizados ao longo da implementação serviram seu papel com excelência. Ao final do projeto, o programa já estava 100% funcional. Foi necessário ajustar as configurações do algoritmo antes que ele obtivesse sucesso.

Inicialmente o método de elitismo não seria implementado, mas ao final da implementação foi possível constatar, pelos gráficos obtidos, que o custo frequentemente dava saltos e regredia com o passar das gerações.
Esse evento se dava pois uma boa rota acabava por vezes sofrendo uma piora ao ser cruzada com outra ruim, ou ainda porque uma rota boa poderia acabar estragada por uma mutação aleatória.
Com a adição do elitismo se tornou possível garantir que uma geração seria ao menos tão boa quanto sua ascendente.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTUwMzA2ODQyOSw0ODI3MjU2MDYsLTIwND
MwMTEzMDEsLTQ3MzI4Nzc3OCwzNDAyMDU3MDMsNzMwOTk4MTE2
XX0=
-->