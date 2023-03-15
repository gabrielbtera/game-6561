from copy import deepcopy

def slideLeftOuRight(tabuleiro: list, direcao: str) -> tuple:
    
    tabuleiro = deepcopy(tabuleiro)

    slide = False
    # Percorre a matriz linha por linha, da direita para a esquerda

    for linha in range(len(tabuleiro)):
        # Inicializa uma lista para armazenar as pecas do tabuleiro
        pecas_tabuleiro = []
        # Percorre a linha e adiciona os valores não nulos à lista
        if direcao == 'L':
            for coluna in range(len(tabuleiro[linha])):
                if tabuleiro[linha][coluna] != 0:
                    pecas_tabuleiro.append(tabuleiro[linha][coluna])
        else:
            for coluna in range(len(tabuleiro) - 1, -1, -1):
                if tabuleiro[linha][coluna] != 0:
                    pecas_tabuleiro.append(tabuleiro[linha][coluna])
                    
        # for coluna in range(len(tabuleiro[linha])):
        #     if tabuleiro[linha][coluna] != 0:
        #         pecas_tabuleiro.append(tabuleiro[linha][coluna])
        indice = 0
        while indice < len(pecas_tabuleiro) - 1:
            
            if pecas_tabuleiro[indice]['cor'] != pecas_tabuleiro[indice+1]['cor'] and pecas_tabuleiro[indice]['valor'] == pecas_tabuleiro[indice+1]['valor']:
                del pecas_tabuleiro[indice]
                tamanho_tab = len(pecas_tabuleiro)
                if tamanho_tab  >= indice:
                    del pecas_tabuleiro[indice]
                if tamanho_tab < indice:
                    del pecas_tabuleiro[indice+1]
                continue
            if pecas_tabuleiro[indice]['cor'] == pecas_tabuleiro[indice+1]['cor'] and pecas_tabuleiro[indice]['valor'] == pecas_tabuleiro[indice+1]['valor']:
                pecas_tabuleiro[indice] = {'cor': pecas_tabuleiro[indice]['cor'], 'valor': pecas_tabuleiro[indice]['valor'] * 3}
                del pecas_tabuleiro[indice+1]
                indice += 1
                continue
            
            indice += 1
       
        
        if direcao == 'R':
            pecas_tabuleiro.reverse()
            pecas_tabuleiro = [0] * (len(tabuleiro[linha]) - len(pecas_tabuleiro)) + pecas_tabuleiro

        elif direcao == 'L':
            pecas_tabuleiro = pecas_tabuleiro + [0] * (len(tabuleiro[linha]) - len(pecas_tabuleiro))
        

        if tabuleiro[linha] != pecas_tabuleiro:
            slide = True
            tabuleiro[linha] = pecas_tabuleiro
    
    return (tabuleiro, slide)




def slideUpDwon(tabuleiro: list, direcao: str) -> tuple:

    tabuleiro = deepcopy(tabuleiro)

    slide = False 

    # Percorre a matriz coluna por coluna, de cima para baixo ou de baixo para cima
    for coluna in range(len(tabuleiro)):
        valores_nao_nulos = []

        if direcao == 'U':
            for linha in range(len(tabuleiro)):
                if tabuleiro[linha][coluna] != 0:
                    valores_nao_nulos.append(tabuleiro[linha][coluna])
        else:
            for linha in range(len(tabuleiro) - 1, -1, -1):
                if tabuleiro[linha][coluna] != 0:
                    valores_nao_nulos.append(tabuleiro[linha][coluna])
            
        
        indice = 0
        while indice < len(valores_nao_nulos) - 1:
            if valores_nao_nulos[indice]['cor'] != valores_nao_nulos[indice+1]['cor'] and valores_nao_nulos[indice]['valor'] == valores_nao_nulos[indice+1]['valor']:
                del valores_nao_nulos[indice]
                tamanho_tab = len(valores_nao_nulos)
                if tamanho_tab  >= indice:
                    del valores_nao_nulos[indice]
                if tamanho_tab < indice:
                    del valores_nao_nulos[indice+1]
                continue
            if valores_nao_nulos[indice]['cor'] == valores_nao_nulos[indice+1]['cor'] and valores_nao_nulos[indice]['valor'] == valores_nao_nulos[indice+1]['valor']:
                valores_nao_nulos[indice] = {'cor': valores_nao_nulos[indice]['cor'], 'valor': valores_nao_nulos[indice]['valor'] * 3}
                del valores_nao_nulos[indice+1]
               
            indice += 1

        if direcao == 'U':
             valores_nao_nulos = valores_nao_nulos + [0] * (len(tabuleiro) - len(valores_nao_nulos))
        else:
            valores_nao_nulos.reverse()
            valores_nao_nulos = [0] * (len(tabuleiro) - len(valores_nao_nulos)) + valores_nao_nulos

        for linha in range(len(tabuleiro)):
            if tabuleiro[linha][coluna] != valores_nao_nulos[linha]:
                slide = True
                tabuleiro[linha][coluna] = valores_nao_nulos[linha]
    return (tabuleiro, slide)


tab3 = [
    [{'cor': 'V', 'valor' : 2}, {'cor': 'A', 'valor' : 2},  {'cor': 'C', 'valor' : 2}, {'cor': 'C', 'valor' : 1}],
     [0, 0, {'cor': 'A', 'valor' : 1},{'cor': 'V', 'valor' : 2}],
    [0, 0, 0,0],
    [0, 0, 0,0]
    ]


tab = [
    [ 0, {'cor': 'C', 'valor' : 1},0 , {'cor': 'V', 'valor' : 9} ],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 3} ],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, 0, {'cor': 'C', 'valor' : 1}],
    [{'cor': 'A', 'valor' : 3}, {'cor': 'V', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 1}]
    ]




