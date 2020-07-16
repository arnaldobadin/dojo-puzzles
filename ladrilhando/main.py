"""
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
"""

import sys

QUAD_KEYS = ["A", "B", "C", "D", "E"]
TILE_KEYS = ["F", "G"]

def getSigIntInput(key):
    # try/catch to handle casting error
    try:
        value = int(input("> Insira o valor do campo '{}': ".format(key)))
        if (value < 0):
            raise
    except:
        raise ValueError("Valor inserido para o campo '{}' deve ser um inteiro maior ou igual a zero.".format(key))

    return value

def getQuadCoords():
    quad_coords = {}

    # use for loop to check inputs
    for key in QUAD_KEYS:
        quad_coords[key] = getSigIntInput(key)

    # check for rule number two, vertices (B, C) and (D, E) can't be the same
    if quad_coords[QUAD_KEYS[1]] == quad_coords[QUAD_KEYS[3]] and quad_coords[QUAD_KEYS[2]] == quad_coords[QUAD_KEYS[4]]:
        raise ValueError("Os vértices ('{}', '{}') e ('{}', '{}') não podem ser coincidentes.".format(*QUAD_KEYS[1:]))

    # if coordenate B is lower than D, this should be either a triangle or nothing
    if quad_coords[QUAD_KEYS[1]] <= quad_coords[QUAD_KEYS[3]]:
        raise ValueError("A coordenada '{}' não pode ser menor que a coordenada '{}'.".format(QUAD_KEYS[1], QUAD_KEYS[3]))

    return quad_coords

def rayCast(ray, target):
    a1 = ray[1][1] - ray[0][1]
    b1 = ray[0][0] - ray[1][0]
    c1 = (ray[1][0] * ray[0][1]) - (ray[0][0] * ray[1][1])

    d1 = (a1 * target[0][0]) + (b1 * target[0][1]) + c1
    d2 = (a1 * target[1][0]) + (b1 * target[1][1]) + c1

    if d1 >= 0 and d2 >= 0: return False
    if d1 < 0 and d2 < 0: return False

    a2 = target[1][1] - target[0][1]
    b2 = target[0][0] - target[1][0]
    c2 = (target[1][0]) * (target[0][1]) - (target[0][0] * target[1][1])

    d1 = (a2 * ray[0][0]) + (b2 * ray[0][1]) + c2
    d2 = (a2 * ray[1][0]) + (b2 * ray[1][1]) + c2

    if d1 >= 0 and d2 >= 0: return False
    if d1 < 0 and d2 < 0: return False

    # this if is to catch collinear case, it is True but someday can be useful
    if (a1 * b2) - (a2 * b1) == 0.0: return True
    return True

def isTileInsideQuad(quad_sides, tile_coords):
    # check if tile is inside quadrilateral using ray casting
    for tile in tile_coords:
        intersections = 0
        
        for quad in quad_sides:
            random_coord = [-(sys.float_info.epsilon / (tile[0] + 1)), -(sys.float_info.epsilon / (tile[1] + 1))]
            if rayCast([random_coord, tile], quad):
                intersections = intersections + 1

        if intersections % 2 == 1:
            return True

    return False

def calculateTilesPerQuad(quad, tile):
    # create quadrilateral sides
    quad_sides = [
        [[0, 0], [quad[QUAD_KEYS[0]], 0]],
        [[quad[QUAD_KEYS[0]], 0], [quad[QUAD_KEYS[1]], quad[QUAD_KEYS[2]]]],
        [[quad[QUAD_KEYS[1]], quad[QUAD_KEYS[2]]], [quad[QUAD_KEYS[3]], quad[QUAD_KEYS[4]]]],
        [[quad[QUAD_KEYS[3]], quad[QUAD_KEYS[4]]], [0, 0]],
    ]

    # get higher coord to create a estimated square of quadrilateral
    higher_coord = None

    for key, value in quad.items():
        if (not higher_coord or value > higher_coord):
            higher_coord = value

    # loop through the estimated square and count how many tiles is inside
    count = 0
    for cols in range(higher_coord):
        for rows in range(higher_coord):
            tiles_coords = [
                [rows * tile[TILE_KEYS[0]], cols * tile[TILE_KEYS[1]]],
                [(rows + 1) * tile[TILE_KEYS[0]], cols * tile[TILE_KEYS[1]]],
                [(rows + 1) * tile[TILE_KEYS[0]], (cols + 1) * tile[TILE_KEYS[1]]],
                [rows * tile[TILE_KEYS[0]], (cols + 1) * tile[TILE_KEYS[1]]]
            ]

            # offset cols if not first (prevents ray tracing from counting the last row)
            if cols != 0:
                for k in range(len(tiles_coords)):
                    tiles_coords[k][0] = tiles_coords[k][0] + 0.0001

            # offset rows if not first (prevents ray tracing from counting the last row)
            if rows != 0:
                for k in range(len(tiles_coords)):
                    tiles_coords[k][1] = tiles_coords[k][1] + 0.0001

            if isTileInsideQuad(quad_sides, tiles_coords):
                count = count + 1

    return count

def main():
    # get quadrilateral position coordenates
    print("Insira as coordenadas da sala a ser ladrilhada (começando do canto inferior esquerdo).\n")

    try:
        quad_coords = getQuadCoords()
    except ValueError as exception:
        print(exception)
        exit()

    # get tile sizes
    tile_sizes = {}

    print("\nInsira o valor dos lados do ladrilho (largura 'F' e comprimento 'G').")
    
    # use for loop to check inputs
    for key in TILE_KEYS:
        try:
            tile_sizes[key] = getSigIntInput(key)
        except ValueError as exception:
            print(exception)
            exit()

    result = calculateTilesPerQuad(quad_coords, tile_sizes)
    print("A quantidade de ladrilhos por sala é '{}'.".format(result))


if __name__ == "__main__":
    main()