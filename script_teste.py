import json
import random
from produto import Produto
from engradado import Engradado
from estoque import Estoque
from main import salvar_produtos_json, salvar_estoque_json, carregar_produtos_json, carregar_estoque_json

def criar_produtos_exemplo():
    nomes = [
        'Coca-Cola', 'Pepsi', 'Fanta', 'Sprite', 'Guaraná', 'Dolly', 'Sukita', 'Itubaína', 'Schweppes', 'Tubaína'
    ]
    produtos = []
    for i, nome in enumerate(nomes, 1):
        produtos.append(Produto(
            codigo=f'{i:03}',
            lote=f'L{i}',
            nome=nome,
            peso=1000,
            validade=f'{random.randint(1,28):02}/12/2025',
            fabricacao=f'{random.randint(1,28):02}/12/2024',
            preco_compra=round(random.uniform(3.0, 6.0), 2),
            preco_venda=round(random.uniform(6.5, 10.0), 2),
            fornecedor=nome,
            fabricante=nome,
            categoria='Bebida'
        ))
    salvar_produtos_json(produtos)
    print('10 produtos cadastrados aleatoriamente!')

def preencher_estoque():
    produtos = carregar_produtos_json()
    estoque = Estoque()
    if not produtos:
        print('Nenhum produto cadastrado!')
        return
    num_produtos = min(len(produtos), 5)  # Até 5 produtos diferentes para 5 colunas
    for j in range(5):  # Para cada coluna
        produto = produtos[j % num_produtos]  # Um produto diferente por coluna
        for i in range(8):  # Para cada linha
            for _ in range(5):  # Empilha até 5 engradados por pilha
                engradado = Engradado(produto, quantidade=10, capacidade_max=10)
                try:
                    estoque.matriz[i][j].empilhar(engradado)
                except Exception:
                    break  # Pilha cheia
    salvar_estoque_json(estoque)
    print('Estoque preenchido: cada coluna com um produto diferente!')

def registrar_pedidos_exemplo():
    pedidos = [
        {'codigo_produto': '001', 'quantidade': 12, 'data_solicitacao': '12/06/2025', 'nome_solicitante': 'Leo'},
        {'codigo_produto': '002', 'quantidade': 8, 'data_solicitacao': '12/06/2025', 'nome_solicitante': 'Maria'},
        {'codigo_produto': '003', 'quantidade': 20, 'data_solicitacao': '12/06/2025', 'nome_solicitante': 'João'},
    ]
    with open('pedidos.json', 'w', encoding='utf-8') as f:
        json.dump(pedidos, f, ensure_ascii=False, indent=2)
    print('Pedidos registrados!')

def main():
    criar_produtos_exemplo()
    preencher_estoque()
    registrar_pedidos_exemplo()
    print('Pronto para rodar o processamento de pedidos pelo sistema principal!')

if __name__ == '__main__':
    main()
