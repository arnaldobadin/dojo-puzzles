### Ladrilhando:

> Dojo escolhido: http://dojopuzzles.com/problemas/exibe/ladrilhando/

```
    Um arquiteto gosta muito de projetar salas em formato quadrangular, que
    normalmente não são tão complicadas de se construir,
    exceto quando os lados não são perpendiculares uns aos outros.

    Nestes casos, na hora de ladrilhar as salas, existe uma dificuldade em saber o número
    exato de ladrilhos retangulares que deverão ser utilizados para não haver desperdício
    dos ladrilhos que devem ser cortados para se ajustar o chão às paredes.

    - Uma sala é definida pelos pontos (0, 0), (A, 0), (B, C) e (D, E) onde todas as coordenadas (A, B, C, D e E) são inteiros maiores que zero;
    - Os vértices (B, C) e (D, E) não são coincidentes;
    - Um ladrinho possui dimensões F x G (com F e G inteiros maior que zero);
    - A parte não utilizada de um ladrilho cortado é jogada fora (mesmo que pudesse ser reutilizada em outra parte da sala).
    - Os ladrilhos começam a ser posicionados a partir da posição (0, 0) perpendiculares à parede formada por (0, 0) e (A, 0).

    Você deve ajudar este arquiteto desenvolvendo um programa que, dado as coordenadas da sala e o
    tamanho dos ladrilhos, retorne a quantidade exata de ladrilhos que serão suficientes para cobrir toda a sala.
```

Utilizei python com a técnica de [Ray Casting](https://en.wikipedia.org/wiki/Point_in_polygon) para resolver o problema.
Faço uma estimativa do tamanho do cômodo, gero uma matrix com todos os ladrilhos e elimino os que não estão dentro do polígono utilizando [Ray Casting](https://en.wikipedia.org/wiki/Point_in_polygon).

Na primeira tentiva eu tentei usar geometria e calcular a posição das linhas no plano, porém o polígono do cômodo podia ser irregular e a quantidade de cálculos a se fazer era muito grande.

As coordenadas do polígono do cômodo começa pelo canto inferior esquerdo, então para desenhar um quadrado por exemplo, usa-se:
> A: 4
> B: 4
> C: 4
> D: 0
> E: 4

Onde (0, 0) é o canto inferior esquerdo, (A, 0) é o canto inferior direito, (B, C) é o canto superior direito e (D, E) é o canto superior esquerdo.

Os campos 'F' e 'G' são respectivamente relacionados a largura e ao comprimento do ladrilho. Então para criar um ladrilho retangular, usa-se:
> F: 2
> G: 3
