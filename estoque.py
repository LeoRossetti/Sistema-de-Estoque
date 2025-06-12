# Classe que representa o estoque como uma matriz de pilhas de engradados
from pilha import PilhaEngradados

class Estoque:
    def __init__(self):
        # Define o tamanho do estoque: 8 linhas x 5 colunas
        self.linhas = 8
        self.colunas = 5
        # Cria a matriz de pilhas (cada posição é uma PilhaEngradados)
        self.matriz = [[PilhaEngradados() for _ in range(self.colunas)] for _ in range(self.linhas)]

    # Adiciona um engradado em uma posição específica da matriz
    def adicionar_engradado(self, linha, coluna, engradado):
        self.matriz[linha][coluna].empilhar(engradado)

    # Remove e retorna o engradado do topo de uma pilha específica
    def remover_engradado(self, linha, coluna):
        return self.matriz[linha][coluna].desempilhar()

    # Retorna uma matriz com o nome do produto do topo de cada pilha (ou '-' se vazia)
    def consultar_estoque(self):
        return [[pilha.topo().produto.nome if not pilha.esta_vazia() else '-' for pilha in linha] for linha in self.matriz]

    # Busca todas as posições onde o produto com o código informado está no topo da pilha
    def buscar_produto(self, codigo_produto):
        posicoes = []
        for i in range(self.linhas):
            for j in range(self.colunas):
                pilha = self.matriz[i][j]
                if not pilha.esta_vazia() and pilha.topo().produto.codigo == codigo_produto:
                    posicoes.append((i, j))
        return posicoes
