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
O algoritmo foi implementado na linguagem **Python 3.8.5**.

Nessa implementação, foram utilizadas três formas diferentes de reprodução: **cruzamento**, **mutação** e **elitismo**.

- Com o cruzamento, 2 indivíduos selecionados têm partes de suas rotas cruzadas para formar uma rota filho.
- Com a mutação, cada *gene* dessa rota filho (cada cidade) tem uma chance de sofrer uma alteração: nesse caso, uma troca com outro gene.
- Com o elitismo, o melhor indivíduo de uma geração passa automáticamente, intacto, para a geração seguinte.

O projeto é organizado em diferentes arquivos, e os dados das cidade foram armazenados em arquivos *json*.
![enter image description here](https://i.ibb.co/zJC4XXM/concept-model.png)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE2NDQ1NTAwNTEsNDgyNzI1NjA2LC0yMD
QzMDExMzAxLC00NzMyODc3NzgsMzQwMjA1NzAzLDczMDk5ODEx
Nl19
-->