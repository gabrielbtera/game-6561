def deslizar_para_baixo(matriz):
    # Define uma variável para armazenar se houve deslizamento ou não
    houve_deslizamento = False
    # Percorre a matriz coluna por coluna, de baixo para cima
    for coluna in range(len(matriz[0])):
        # Inicializa uma lista para armazenar os valores não nulos da coluna
        valores_nao_nulos = []
        # Percorre a coluna e adiciona os valores não nulos à lista
        for linha in range(len(matriz) - 1, -1, -1):
            if matriz[linha][coluna] != 0:
                valores_nao_nulos.append(matriz[linha][coluna])
        # Percorre a coluna novamente, de baixo para cima, e substitui os valores pelo próximo valor não nulo da lista, ou zero se não houver mais valores não nulos
        for linha in range(len(matriz) - 1, -1, -1):
            if linha >= len(matriz) - len(valores_nao_nulos):
                if matriz[linha][coluna] != valores_nao_nulos[len(valores_nao_nulos) - 1 - (linha - (len(matriz) - len(valores_nao_nulos)))]:
                    houve_deslizamento = True
                matriz[linha][coluna] = valores_nao_nulos[len(valores_nao_nulos) - 1 - (linha - (len(matriz) - len(valores_nao_nulos)))]
            else:
                if matriz[linha][coluna] != 0:
                    houve_deslizamento = True
                matriz[linha][coluna] = 0
    # Retorna uma tupla com a matriz deslizada para baixo e o valor booleano indicando se houve deslizamento ou não
    return (matriz, houve_deslizamento)


def deslizar_para_cima(matriz):
    # Define uma variável para armazenar se houve deslizamento ou não
    houve_deslizamento = False
    # Percorre a matriz coluna por coluna, de cima para baixo
    for coluna in range(len(matriz[0])):
        # Inicializa uma lista para armazenar os valores não nulos da coluna
        valores_nao_nulos = []
        # Percorre a coluna e adiciona os valores não nulos à lista
        for linha in range(len(matriz)):
            if matriz[linha][coluna] != 0:
                valores_nao_nulos.append(matriz[linha][coluna])
        # Percorre a coluna novamente, de cima para baixo, e substitui os valores pelo próximo valor não nulo da lista, ou zero se não houver mais valores não nulos
        for linha in range(len(matriz)):
            if linha < len(valores_nao_nulos):
                if matriz[linha][coluna] != valores_nao_nulos[linha]:
                    houve_deslizamento = True
                matriz[linha][coluna] = valores_nao_nulos[linha]
            else:
                if matriz[linha][coluna] != 0:
                    houve_deslizamento = True
                matriz[linha][coluna] = 0
    # Retorna uma tupla com a matriz deslizada para cima e o valor booleano indicando se houve deslizamento ou não
    return (matriz, houve_deslizamento)

def deslizar_para_esquerda(matriz):
    # Define uma variável para armazenar se houve deslizamento ou não
    houve_deslizamento = False
    # Percorre a matriz linha por linha, da esquerda para a direita
    for linha in range(len(matriz)):
        # Inicializa uma lista para armazenar os valores não nulos da linha
        valores_nao_nulos = []
        # Percorre a linha e adiciona os valores não nulos à lista
        for coluna in range(len(matriz[0])):
            if matriz[linha][coluna] != 0:
                valores_nao_nulos.append(matriz[linha][coluna])
        # Percorre a linha novamente, da esquerda para a direita, e substitui os valores pelo próximo valor não nulo da lista, ou zero se não houver mais valores não nulos
        for coluna in range(len(matriz[0])):
            if coluna < len(valores_nao_nulos):
                if matriz[linha][coluna] != valores_nao_nulos[coluna]:
                    houve_deslizamento = True
                matriz[linha][coluna] = valores_nao_nulos[coluna]
            else:
                if matriz[linha][coluna] != 0:
                    houve_deslizamento = True
                matriz[linha][coluna] = 0
    # Retorna uma tupla com a matriz deslizada para a esquerda e o valor booleano indicando se houve deslizamento ou não
    return (matriz, houve_deslizamento)


def deslizar_para_direita(matriz):
    # Define uma variável para armazenar se houve deslizamento ou não
    houve_deslizamento = False
    # Percorre a matriz linha por linha, da esquerda para a direita
    for linha in range(len(matriz)):
        # Inicializa uma lista para armazenar os valores não nulos da linha
        valores_nao_nulos = []
        # Percorre a linha e adiciona os valores não nulos à lista
        for coluna in range(len(matriz[0]) - 1, -1, -1):
            if matriz[linha][coluna] != 0:
                valores_nao_nulos.append(matriz[linha][coluna])
        # Percorre a linha novamente, da direita para a esquerda, e substitui os valores pelo próximo valor não nulo da lista, ou zero se não houver mais valores não nulos
        for coluna in range(len(matriz[0]) - 1, -1, -1):
            if coluna >= len(matriz[0]) - len(valores_nao_nulos):
                if matriz[linha][coluna] != valores_nao_nulos[len(valores_nao_nulos) - 1 - (coluna - (len(matriz[0]) - len(valores_nao_nulos)))]:
                    houve_deslizamento = True
                matriz[linha][coluna] = valores_nao_nulos[len(valores_nao_nulos) - 1 - (coluna - (len(matriz[0]) - len(valores_nao_nulos)))]
            else:
                if matriz[linha][coluna] != 0:
                    houve_deslizamento = True
                matriz[linha][coluna] = 0
    # Retorna uma tupla com a matriz deslizada para direita e o valor booleano indicando se houve deslizamento ou não
    return (matriz, houve_deslizamento)




tab3 = [
    [{'cor': 'V', 'valor' : 2}, {'cor': 'A', 'valor' : 2},  {'cor': 'C', 'valor' : 2}, {'cor': 'C', 'valor' : 1}],
    [{'cor': 'C', 'valor' : 1}, {'cor': 'A', 'valor' : 1}, {'cor': 'A', 'valor' : 1},{'cor': 'V', 'valor' : 1}],
    [0, 0, 0,0],
    [0, 0, 0,0]
    ]


t, m = deslizar_para_baixo(tab3)

for i in t:
    print(i, m)

m , t = deslizar_para_cima(t)


print('cima')
for i in m:
    print(i)
