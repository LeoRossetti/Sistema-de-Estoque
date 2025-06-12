import json
from produto import Produto
from engradado import Engradado
from estoque import Estoque

def carregar_produtos_json():
    with open('produtos.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
        return [Produto.from_dict(d) for d in dados]

def main():
    produtos = carregar_produtos_json()
    estoque = Estoque()
    idx_prod = 0
    for i in range(8):
        for j in range(5):
            produto = produtos[idx_prod % len(produtos)]
            engradado = Engradado(produto, quantidade=10, capacidade_max=10, peso_kg=10.0)
            estoque.adicionar_engradado(i, j, engradado)
            idx_prod += 1
    # Salva o estoque preenchido
    matriz_serializada = []
    for linha in estoque.matriz:
        linha_serializada = []
        for pilha in linha:
            pilha_serializada = []
            for engradado in pilha.pilha:
                engradado_dict = {
                    'produto': engradado.produto.to_dict(),
                    'quantidade': engradado.quantidade,
                    'capacidade_max': engradado.capacidade_max,
                    'peso_kg': getattr(engradado, 'peso_kg', 0.0)
                }
                pilha_serializada.append(engradado_dict)
            linha_serializada.append(pilha_serializada)
        matriz_serializada.append(linha_serializada)
    with open('estoque.json', 'w', encoding='utf-8') as f:
        json.dump(matriz_serializada, f, ensure_ascii=False, indent=2)
    print('Estoque preenchido com sucesso!')

if __name__ == '__main__':
    main()
