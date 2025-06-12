from produto import Produto
from engradado import Engradado
from pilha import PilhaEngradados
from estoque import Estoque
from pedido import Pedido, FilaPedidos
from relatorios import produtos_proximos_vencimento, itens_em_falta, historico_pedidos_recursivo
import json
import os

# Função para salvar a lista de produtos no arquivo JSON
# Utiliza serialização para garantir persistência dos dados
def salvar_produtos_json(lista_produtos):
    with open('produtos.json', 'w', encoding='utf-8') as f:
        json.dump([p.to_dict() for p in lista_produtos], f, ensure_ascii=False, indent=2)

# Função para carregar produtos do arquivo JSON
# Retorna uma lista de objetos Produto
def carregar_produtos_json():
    try:
        with open('produtos.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return [Produto.from_dict(d) for d in dados]
    except FileNotFoundError:
        return []

# Função para salvar o estoque (matriz de pilhas de engradados) em JSON
# Serializa toda a estrutura do estoque para persistência
def salvar_estoque_json(estoque):
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

# Função para carregar o estoque do arquivo JSON
# Reconstrói a matriz de pilhas e os objetos engradado/produto
# Garante que o sistema retome o estado anterior ao ser reiniciado
# Se não existir arquivo, retorna um estoque vazio
def carregar_estoque_json():
    from engradado import Engradado
    from produto import Produto
    try:
        with open('estoque.json', 'r', encoding='utf-8') as f:
            matriz_serializada = json.load(f)
        estoque = Estoque()
        for i, linha in enumerate(matriz_serializada):
            for j, pilha_serializada in enumerate(linha):
                pilha = estoque.matriz[i][j]
                for engradado_dict in pilha_serializada:
                    produto = Produto.from_dict(engradado_dict['produto'])
                    engradado = Engradado(produto, engradado_dict['quantidade'], engradado_dict['capacidade_max'], engradado_dict.get('peso_kg', 0.0))
                    pilha.empilhar(engradado)
        return estoque
    except FileNotFoundError:
        return Estoque()

def main():
    # Garante que o arquivo de estoque existe ao iniciar o sistema
    if not os.path.exists('estoque.json'):
        salvar_estoque_json(Estoque())
    print('Sistema de Estoque - Inicialização')
    while True:
        # Menu principal do sistema
        print('\n1. Adicionar produto')
        print('2. Listar produtos')
        print('3. Adicionar engradado ao estoque')
        print('4. Visualizar estoque')
        print('5. Registrar pedido')
        print('6. Processar pedidos')
        print('7. Relatório: produtos próximos ao vencimento')
        print('8. Relatório: itens em falta')
        print('9. Relatório: histórico de pedidos atendidos')
        print('0. Sair')
        opcao = input('Escolha uma opção: ')
        # Cadastro de produto novo
        if opcao == '1':
            print('\nCadastro de Produto:')
            # Coleta todos os dados obrigatórios do produto
            codigo = input('Código: ')
            lote = input('Lote: ')
            nome = input('Nome: ')
            peso = float(input('Peso do produto (em gramas): '))
            validade = input('Data de validade (DD/MM/YYYY): ')
            fabricacao = input('Data de fabricação (DD/MM/YYYY): ')
            preco_compra = float(input('Preço de compra: '))
            preco_venda = float(input('Preço de venda: '))
            fornecedor = input('Fornecedor: ')
            fabricante = input('Fabricante: ')
            categoria = input('Categoria: ')
            # Cria o objeto Produto e salva
            produto = Produto(codigo, lote, nome, peso, validade, fabricacao, preco_compra, preco_venda, fornecedor, fabricante, categoria)
            produtos = carregar_produtos_json()
            produtos.append(produto)
            salvar_produtos_json(produtos)
            print('Produto adicionado com sucesso!')
        # Listagem dos produtos cadastrados
        elif opcao == '2':
            produtos = carregar_produtos_json()
            if not produtos:
                print('Nenhum produto cadastrado.')
            else:
                print('\nLista de Produtos:')
                print('-'*60)
                for p in produtos:
                    print(f'Código: {p.codigo} | Nome: {p.nome} | Lote: {p.lote} | Validade: {p.validade}')
                print('-'*60)
        # Adição de engradado ao estoque
        elif opcao == '3':
            produtos = carregar_produtos_json()
            if not produtos:
                print('Cadastre produtos antes de criar engradados!')
                continue
            print('\nProdutos disponíveis:')
            print('-'*60)
            for idx, p in enumerate(produtos):
                print(f'{idx+1}. Código: {p.codigo} | Nome: {p.nome} | Lote: {p.lote} | Validade: {p.validade}')
            print('-'*60)
            idx_prod = int(input('Escolha o produto pelo número: ')) - 1
            if idx_prod < 0 or idx_prod >= len(produtos):
                print('Produto inválido!')
                continue
            produto = produtos[idx_prod]
            capacidade_max = int(input('Capacidade máxima do engradado: '))
            quantidade = int(input('Quantidade de itens neste engradado: '))
            peso_engradado = float(input('Peso do engradado (em kg): '))
            if quantidade > capacidade_max:
                print('Quantidade não pode exceder a capacidade máxima!')
                continue
            engradado = Engradado(produto, quantidade, capacidade_max, peso_engradado)
            estoque = carregar_estoque_json()
            inserido = False
            # Procura uma pilha vazia ou pilha do mesmo produto não cheia para empilhar
            for i in range(8):
                for j in range(5):
                    pilha = estoque.matriz[i][j]
                    if pilha.esta_vazia() or (not pilha.esta_vazia() and pilha.topo().produto.codigo == produto.codigo and not pilha.esta_cheia()):
                        try:
                            estoque.adicionar_engradado(i, j, engradado)
                            salvar_estoque_json(estoque)
                            print(f'Engradado adicionado ao estoque na linha {i}, coluna {j}!')
                            inserido = True
                            break
                        except Exception as e:
                            print(f'Erro: {e}')
                if inserido:
                    break
            if not inserido:
                print('Não há pilha disponível para este engradado (todas ocupadas ou cheias para este produto).')
        # Visualização detalhada do estoque
        elif opcao == '4':
            estoque = carregar_estoque_json()
            print('Visualização detalhada do estoque:')
            for i, linha in enumerate(estoque.matriz):
                print(f'Linha {i}:')
                for j, pilha in enumerate(linha):
                    if pilha.esta_vazia():
                        print(f'  Coluna {j}: [vazia]')
                    else:
                        print(f'  Coluna {j}:')
                        # Mostra todos os engradados empilhados (LIFO)
                        for idx, engradado in enumerate(reversed(pilha.pilha)):
                            print(f'    Engradado {len(pilha.pilha)-idx}: {engradado.produto.nome} | Qtd: {engradado.quantidade} | Cap: {engradado.capacidade_max}')
        # Registro de pedido (adiciona à fila FIFO)
        elif opcao == '5':
            produtos = carregar_produtos_json()
            if not produtos:
                print('Cadastre produtos antes de registrar pedidos!')
                continue
            print('\nProdutos disponíveis:')
            print('-'*60)
            for idx, p in enumerate(produtos):
                print(f'{idx+1}. Código: {p.codigo} | Nome: {p.nome} | Lote: {p.lote} | Validade: {p.validade}')
            print('-'*60)
            idx_prod = int(input('Escolha o produto pelo número: ')) - 1
            if idx_prod < 0 or idx_prod >= len(produtos):
                print('Produto inválido!')
                continue
            codigo_produto = produtos[idx_prod].codigo
            quantidade = int(input('Quantidade desejada (soma dos itens, não engradados): '))
            data_solicitacao = input('Data da solicitação (DD/MM/YYYY): ')
            nome_solicitante = input('Nome do solicitante: ')
            # Salva o pedido no arquivo de pedidos (fila FIFO)
            try:
                with open('pedidos.json', 'r', encoding='utf-8') as f:
                    pedidos_data = json.load(f)
            except FileNotFoundError:
                pedidos_data = []
            pedidos_data.append({
                'codigo_produto': codigo_produto,
                'quantidade': quantidade,
                'data_solicitacao': data_solicitacao,
                'nome_solicitante': nome_solicitante
            })
            with open('pedidos.json', 'w', encoding='utf-8') as f:
                json.dump(pedidos_data, f, ensure_ascii=False, indent=2)
            print('Pedido registrado!')
        # Processamento dos pedidos (ordem FIFO)
        elif opcao == '6':
            try:
                with open('pedidos.json', 'r', encoding='utf-8') as f:
                    pedidos_data = json.load(f)
            except FileNotFoundError:
                print('Nenhum pedido na fila!')
                continue
            if not pedidos_data:
                print('Nenhum pedido na fila!')
                continue
            estoque = carregar_estoque_json()
            pedidos_atendidos = []
            pedidos_restantes = []
            for pedido in pedidos_data:
                codigo_produto = pedido['codigo_produto']
                quantidade_necessaria = pedido['quantidade']
                total_removido = 0
                engradados_removidos = []
                # Remove engradados do topo das pilhas (LIFO) até atingir a quantidade
                for i in range(8):
                    for j in range(5):
                        pilha = estoque.matriz[i][j]
                        while (not pilha.esta_vazia() and pilha.topo().produto.codigo == codigo_produto and total_removido < quantidade_necessaria):
                            engradado = pilha.topo()
                            if total_removido + engradado.quantidade <= quantidade_necessaria:
                                pilha.desempilhar()
                                engradados_removidos.append({'linha': i, 'coluna': j, 'quantidade': engradado.quantidade})
                                total_removido += engradado.quantidade
                            else:
                                break
                        if total_removido >= quantidade_necessaria:
                            break
                    if total_removido >= quantidade_necessaria:
                        break
                if total_removido >= quantidade_necessaria:
                    print(f'Pedido atendido: {pedido} (Engradados removidos: {engradados_removidos})')
                    pedidos_atendidos.append(pedido)
                else:
                    print(f'Não há estoque suficiente para o pedido: {pedido}')
                    pedidos_restantes.append(pedido)
            # Atualiza o estoque e os arquivos de pedidos/histórico
            salvar_estoque_json(estoque)
            with open('pedidos.json', 'w', encoding='utf-8') as f:
                json.dump(pedidos_restantes, f, ensure_ascii=False, indent=2)
            try:
                with open('historico_pedidos.json', 'r', encoding='utf-8') as f:
                    historico = json.load(f)
            except FileNotFoundError:
                historico = []
            historico.extend(pedidos_atendidos)
            with open('historico_pedidos.json', 'w', encoding='utf-8') as f:
                json.dump(historico, f, ensure_ascii=False, indent=2)
        # Relatório de produtos próximos ao vencimento (ordem crescente de validade)
        elif opcao == '7':
            produtos = [p.to_dict() for p in carregar_produtos_json()]
            proximos = produtos_proximos_vencimento(produtos)
            print('Produtos próximos ao vencimento (30 dias):')
            for p in proximos:
                print(f"{p['codigo']} - {p['nome']} | Validade: {p['validade']}")
        # Relatório de itens em falta (produtos totalmente esgotados)
        elif opcao == '8':
            estoque = carregar_estoque_json()
            faltando = itens_em_falta(estoque)
            if not faltando:
                print('Nenhum item em falta.')
            else:
                print('Itens em falta:')
                for cod in faltando:
                    print(cod)
        # Relatório do histórico de pedidos atendidos (recursivo)
        elif opcao == '9':
            try:
                with open('historico_pedidos.json', 'r', encoding='utf-8') as f:
                    historico = json.load(f)
            except FileNotFoundError:
                historico = []
            print('Histórico de pedidos atendidos:')
            for p in historico_pedidos_recursivo(historico):
                print(p)
        # Opção para sair do sistema
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')


if __name__ == '__main__':
    main()
