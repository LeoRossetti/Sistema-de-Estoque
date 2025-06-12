# Classe que representa uma pilha de engradados (estrutura LIFO)
# Cada pilha pode conter até 5 engradados
class PilhaEngradados:
    def __init__(self):
        # Lista que armazena os engradados empilhados
        self.pilha = []
        # Capacidade máxima da pilha (5 engradados)
        self.capacidade = 5

    # Empilha um novo engradado no topo da pilha
    def empilhar(self, engradado):
        if len(self.pilha) < self.capacidade:
            self.pilha.append(engradado)
        else:
            raise Exception('Pilha cheia!')

    # Remove e retorna o engradado do topo da pilha
    def desempilhar(self):
        if self.pilha:
            return self.pilha.pop()
        else:
            raise Exception('Pilha vazia!')

    # Retorna o engradado do topo da pilha sem remover
    def topo(self):
        if self.pilha:
            return self.pilha[-1]
        return None

    # Retorna True se a pilha está vazia
    def esta_vazia(self):
        return len(self.pilha) == 0

    # Retorna True se a pilha está cheia
    def esta_cheia(self):
        return len(self.pilha) == self.capacidade
