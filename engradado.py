# Classe que representa um engradado no estoque
# Cada engradado armazena apenas um tipo de produto
class Engradado:
    def __init__(self, produto, quantidade, capacidade_max, peso_kg):
        # Produto armazenado neste engradado
        self.produto = produto
        # Quantidade de itens do produto neste engradado
        self.quantidade = quantidade
        # Capacidade máxima de itens que o engradado pode armazenar
        self.capacidade_max = capacidade_max
        # Peso total do engradado (em kg)
        self.peso_kg = peso_kg

    # Retorna True se o engradado está cheio
    def esta_cheio(self):
        return self.quantidade >= self.capacidade_max

    # Retorna True se o engradado está vazio
    def esta_vazio(self):
        return self.quantidade == 0
