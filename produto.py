# Classe que representa um produto do estoque
import json
from datetime import datetime

class Produto:
    def __init__(self, codigo, lote, nome, peso, validade, fabricacao, preco_compra, preco_venda, fornecedor, fabricante, categoria):
        # Atributos principais do produto
        self.codigo = codigo
        self.lote = lote
        self.nome = nome
        self.peso = peso
        self.validade = validade
        self.fabricacao = fabricacao
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.fornecedor = fornecedor
        self.fabricante = fabricante
        self.categoria = categoria

    # Serializa o produto para dicionário (usado para salvar em JSON)
    def to_dict(self):
        return self.__dict__

    # Cria um objeto Produto a partir de um dicionário (usado ao carregar do JSON)
    @staticmethod
    def from_dict(data):
        return Produto(**data)

    # Serializa o produto para string JSON
    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    # Cria um objeto Produto a partir de uma string JSON
    @staticmethod
    def from_json(json_str):
        return Produto.from_dict(json.loads(json_str))
