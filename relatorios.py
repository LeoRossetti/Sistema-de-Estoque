# Funções de relatório para o sistema de estoque
from datetime import datetime, timedelta

# Relatório recursivo: encontra produtos próximos ao vencimento
# Retorna produtos cuja validade está a até 'dias' dias de hoje, ordenados do que vence primeiro para o que vence depois
def produtos_proximos_vencimento(lista_produtos, dias=30, idx=0, resultado=None):
    if resultado is None:
        resultado = []
    if idx >= len(lista_produtos):
        # Ordena pelo tempo restante para vencer (menor primeiro)
        def dias_para_vencer(prod):
            validade = prod['validade']
            try:
                validade_dt = datetime.strptime(validade, '%d/%m/%Y')
            except Exception:
                validade_dt = datetime.now() + timedelta(days=365)
            return (validade_dt - datetime.now()).days
        return sorted(resultado, key=dias_para_vencer)
    produto = lista_produtos[idx]
    validade = produto['validade']
    try:
        validade_dt = datetime.strptime(validade, '%d/%m/%Y')
    except Exception:
        validade_dt = datetime.now() + timedelta(days=365)
    if 0 <= (validade_dt - datetime.now()).days <= dias:
        resultado.append(produto)
    return produtos_proximos_vencimento(lista_produtos, dias, idx+1, resultado)

# Relatório: retorna produtos totalmente esgotados (sem nenhum engradado com quantidade > 0)
def itens_em_falta(estoque):
    codigos_produtos = set()
    codigos_com_estoque = set()
    for i in range(len(estoque.matriz)):
        for j in range(len(estoque.matriz[0])):
            pilha = estoque.matriz[i][j]
            for engradado in pilha.pilha:
                codigos_produtos.add(engradado.produto.codigo)
                if engradado.quantidade > 0:
                    codigos_com_estoque.add(engradado.produto.codigo)
    return codigos_produtos - codigos_com_estoque

# Relatório recursivo: histórico de pedidos atendidos
def historico_pedidos_recursivo(historico, idx=0):
    if idx >= len(historico):
        return []
    return [historico[idx]] + historico_pedidos_recursivo(historico, idx+1)
