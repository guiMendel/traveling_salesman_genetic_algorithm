# Problema do Caixeiro Viajante com  Algoritmo Genético
Esta implementação soluciona uma instância do problema do caixeiro viajante, em que a rota começa e termina sempre na cidade de Brasília.

![example](https://i.ibb.co/Vq9MyQY/example.png)

## O Problema
Nesta instância do problema do caixeiro viajante, as rotas têm sempre exatamente 11 cidades, sendo a inicial e a final sempre a cidade de Brasília. As cidades intermediárias são uma permutação das cidades de *São Paulo, Lima, Bogotá, Rio de Janeiro, Santiago, Caracas, Buenos Aires, Porto Alegre e Belo Horizonte*.
## A Solução
O **Algoritmo Genético** é um algoritmo de busca inspirado na teoria da evolução darwiniana, em que uma *população* de soluções (cada solução é uma diferente rota) é sujeita a uma série de *operações genéticas*, assim resultando numa série de *gerações*.

Cada *indivíduo* dessa população tem sua adequação avaliada para gerar um número, o **nível de adequação** *(fitness score)*.

Em cada geração, alguns indivíduos são selecionados para gerar a geração seguinte por meio das operações genéticas. Quanto mais adequado um indivíduo for, maior sua chance de seleção.

### A implementação
Nessa implementação, foram utilizadas três formas diferentes de reprodução: **cruzamento**, **mutação** e **elitismo**.
Com o cruzamento, 2 indivíduos selecionados têm partes de suas rotas cruzadas para formar uma rota filho.
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTE2NDEzNTA3NywtMjA0MzAxMTMwMSwtND
czMjg3Nzc4LDM0MDIwNTcwMyw3MzA5OTgxMTZdfQ==
-->