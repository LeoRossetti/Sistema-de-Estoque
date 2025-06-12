from collections import deque

# Classe que representa um pedido de produto
class Pedido:
    def __init__(self, codigo_produto, quantidade, data_solicitacao, nome_solicitante):
        # Código do produto solicitado
        self.codigo_produto = codigo_produto
        # Quantidade de itens solicitados
        self.quantidade = quantidade
        # Data em que o pedido foi feito
        self.data_solicitacao = data_solicitacao
        # Nome de quem fez o pedido
        self.nome_solicitante = nome_solicitante

# Classe que representa uma fila de pedidos (estrutura FIFO)
class FilaPedidos:
    def __init__(self):
        # Utiliza deque para implementar a fila de pedidos
        self.fila = deque()

    # Adiciona um pedido ao final da fila
    def adicionar_pedido(self, pedido):
        self.fila.append(pedido)

    # Remove e retorna o pedido mais antigo da fila
    def processar_pedido(self):
        if self.fila:
            return self.fila.popleft()
        return None

    # Retorna True se a fila está vazia
    def esta_vazia(self):
        return len(self.fila) == 0
