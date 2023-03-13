#!/usr/bin/env python3

import sys
import random
from copy import deepcopy

VALORES = [11, 12, 13, 14, 21, 22,23, 24, 31, 32,33,34, 41, 42, 43, 44]


EMPTY = 0
AZUL  = 'A'
CINZA = 'C'
VERMELHO = 'V'

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'


TABULEIRO = [[0,0,0, 0] for _ in range(0, 4)]






def getDadosaAcao(indices: str) -> str or tuple:
    if len(indices) == 2:
        i , j = int(indices[0]) -1 , int(indices[1])-1
        return  i, j
    return indices


def getSlideVazio(opc: str, key: str):
    opcLU = {
        '1110': True,
        '1100': True,
        '1000': True, 
        '1111': True,
        '0000' : True
    }
    opcRD = {
        '0111': True,
        '0011' : True,
        '0001' : True,
        '1111': True,
        '0000' : True
    } 

    if opc == 'R' or  opc == 'D':
        return opcRD.get(key)
    elif opc == 'L' or opc == 'U':
        return opcLU.get(key)


def deslizarOTabuleiro(letra: str) -> str:
    return 'U'


def getAcao(tipoCor: int) -> str:
    opcoes = {0: 'A', 
              1: 'C', 
              2 : 'D',
              3: 'V', 
              4 : 'D'
              }
    return opcoes[tipoCor]
    


def setValoresNoTabuleiro(memoria: list, linha: int, coluna: int, cor: str ) -> False:
    valorMemoria = memoria[linha][coluna]
    if not valorMemoria:
        memoria[linha][coluna] = {'cor': cor, 'valor': 1}
        return True
    return False

def completaZerosAdireita(lista: list):
    n = 4 - len(lista)
    lista.extend([0]* n)

def removeZerosDeUmaListaECompletaComZerosADireita(lista: list):
    newLista = [i for i in lista if i]
    completaZerosAdireita(newLista)
    return newLista


      
def slideUPOuDown(tabuleiro: list, opcao: str, canSlide = False):

    slide = False

    if opcao == DOWN:
        tabuleiro.reverse()

    for coluna in range(4):
        
        listaColuna = []
        makeSlide = ''
        for linha in range(0, 4):
            casa_n  = tabuleiro[linha][coluna]
            makeSlide += '1' if casa_n else '0'
            if casa_n:
                listaColuna.append(casa_n)

        completaZerosAdireita(listaColuna)

        if not getSlideVazio(opcao, makeSlide) and not slide:
            slide = True


        i = 0
        while i < 3:
            casa_n = listaColuna[i]
            casa_n_mais = listaColuna[i + 1]

            if casa_n and casa_n_mais:
                
                if casa_n['cor'] == casa_n_mais['cor'] and casa_n['valor'] == casa_n_mais['valor']:
                    listaColuna[i]['valor'] *= 3
                    listaColuna[i + 1] = 0
                    i += 2
                    slide = True
                    continue
                elif casa_n['cor'] != casa_n_mais['cor'] and casa_n['valor'] == casa_n_mais['valor']:
                    listaColuna[i] = 0
                    listaColuna[i + 1] = 0
                    i += 2
                    slide = True
                    continue
            i += 1
        
        listaColuna = removeZerosDeUmaListaECompletaComZerosADireita(listaColuna)

        if not canSlide:
            for linha in range(4):
                tabuleiro[linha][coluna] = listaColuna[linha]
            
    if opcao == DOWN:
        tabuleiro.reverse()
    

    # print(tabuleiro)   
    
    return slide
    
   


def slideRigthOuLeft(tabuleiro: list, opcao:str, canSlide =False) -> None:

    # print(tabuleiro)
    

    slide = False
    for linha in range(4):
        makeSlide = ''
        listaColuna = []
        for coluna in range(0, 4):
            casa_n  = tabuleiro[linha][coluna]
            makeSlide += '1' if casa_n else '0'
            if casa_n:
                listaColuna.append(casa_n)

        if not getSlideVazio(opcao, makeSlide) and not slide:
            slide = True
        
        if opcao == RIGHT:
            listaColuna.reverse()
        completaZerosAdireita(listaColuna)

        


        i = 0
        while i < 3:
            casa_n = listaColuna[i]
            casa_n_mais = listaColuna[i + 1]

            if casa_n and casa_n_mais:
                
                if casa_n['cor'] == casa_n_mais['cor'] and casa_n['valor'] == casa_n_mais['valor']:
                    listaColuna[i]['valor'] *= 3
                    listaColuna[i + 1] = 0
                    i += 2
                    slide = True
                    continue
                elif casa_n['cor'] != casa_n_mais['cor'] and casa_n['valor'] == casa_n_mais['valor']:
                    listaColuna[i] = 0
                    listaColuna[i + 1] = 0
                    i += 2
                    slide = True
                    continue
            i += 1

        listaColuna = removeZerosDeUmaListaECompletaComZerosADireita(listaColuna)

        # if EMPTY in listaColuna:
        #     slide = True

        if opcao == RIGHT:
            listaColuna.reverse()
        
        # print(opcao,listaColuna)
        
        # print(listaColuna, '\n')
       
        if not canSlide:
            for coluna in range(4):
                tabuleiro[linha][coluna] = listaColuna[coluna]
            
     
    return slide

    


def acoesDeSlide(tabuleiro: list, opcao: str):
    if opcao ==  DOWN or opcao == UP:
        slideUPOuDown(tabuleiro, opcao)
    else:
        slideRigthOuLeft(tabuleiro, opcao)



tab = [
    [ 0, {'cor': 'C', 'valor' : 1}, 0, {'cor': 'V', 'valor' : 9}],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 3} ],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, 0, {'cor': 'C', 'valor' : 1}],
    [{'cor': 'A', 'valor' : 3}, {'cor': 'V', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 1}]
    ]


tab1 = [
    [ {'cor': 'C', 'valor' : 1}, {'cor': 'V', 'valor' : 9},  {'cor': 'C', 'valor' : 1}, {'cor': 'C', 'valor' : 2}],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 3} ],
    [{'cor': 'C', 'valor' : 2}, {'cor': 'C', 'valor' : 3}, {'cor': 'V', 'valor' : 3}, {'cor': 'C', 'valor' : 9}],
    [{'cor': 'A', 'valor' : 3}, {'cor': 'V', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 1}]
    ]

tab3 = deepcopy(tab)

# slideUPOuDown(tab, 'D')

# print(slideUPOuDown(tab, 'U', True))

tab4 = [[{'cor': 'C', 'valor': 2}, {'cor': 'C', 'valor': 1}, 0, 0], [{'cor': 'C', 'valor': 1}, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
tab5 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, {...}], [{...}, {...}, {...}, {...}]]

# print(slideRigthOuLeft(tab4, 'L', True)) # -> L
# print(slideRigthOuLeft(tab4, 'R', True)) # -> L

# print(tab4)
# slideUPOuDown(tab3, 'U') # -> R




            
            



        



            


            

                

         

            






    

def executarAcaoNoTabuleiro(opcaoDeAcao: str, opcao: str):

    if opcaoDeAcao == AZUL:
        i, j =  getAcao(opcao)
        setValoresNoTabuleiro(TABULEIRO, i, j, AZUL)
    elif opcao == CINZA:
        i, j =  getAcao(opcao)
        setValoresNoTabuleiro(TABULEIRO, i, j, CINZA)
    elif opcao == VERMELHO:
        i, j =  getAcao(opcao)
        setValoresNoTabuleiro(TABULEIRO, i, j, CINZA)
    elif opcao == UP:
        pass


    



        

    


def main():

  entrada = sys.stdin.readline()
  
  
  if (entrada.strip() == "A"):
      
      tipoDeCor = 0
      while (True):
          
        if (entrada.strip() == "Quit"):
            break

        lc = VALORES [random.randint(0, 15)]

        print(str(lc))

        sys.stdout.flush()

        entrada = sys.stdin.readline()

        acao = getAcao(entrada)

              


          
  else:
      # Estou jogando como Order
      memoria = []
      while (True):
          if (entrada.strip() == "Quit"):
              break
          lc = random.randint(11, 44)
          # memoria.append(entrada[1]+entrada[2])
          # Escolha aleatoria de peca existente
          # random.shuffle(memoria)
          # peca = memoria[0]
          # memoria.remove(peca)
          # Laço para definir local destino
          # Tem que respeitar horizontal ou vertical
          # random.shuffle(linhas)
          # random.shuffle(colunas)
          # lc = linhas[0]+colunas[0]
          # while ((lc in memoria) or (lc[0]!=peca[0]) or (lc[1]!=peca[1])):
          #     random.shuffle(linhas)
          #     random.shuffle(colunas)
          #     lc = linhas[0]+colunas[0]
          # memoria.append(lc)
          # #Saida da jogada
          # print(peca+lc)
          lc = random.randint(11, 44);

          print(lc)

          sys.stdout.flush()
          # Leitura da jogada do adversario Chaos
          
          entrada = sys.stdin.readline()



# main()