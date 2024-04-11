# -*- coding: utf-8 -*-
"""padronizar_especificações_supri

# CODIGO VÁLIDO
"""

"""Leitura do arquivo inical e construção das listas para processamento.

"""

import pandas as pd
g8 = pd.read_excel("/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/grupo08_novo.xlsx")

g8.rename(columns={'Descrição do Item': 'Item'}, inplace=True)
g8.to_excel("/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/grupo08_novo.xlsx", index=False)

g8.head()

import pandas as pd

# Substitua 'caminho_do_arquivo' pelo caminho real para o seu arquivo Excel.
#df = pd.read_excel('/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_4/grupo04_novo.xlsx')

# Converter a coluna de interesse em uma lista de strings
lista_de_itens = g8['Item'].astype(str).tolist()

# Em seguida, cria uma string única, onde cada item está em uma nova linha e entre aspas
string_com_itens_em_linhas_separadas_com_aspas = ',\n'.join([f'"{item}"' for item in lista_de_itens])

# Mostrar a string resultante
print(string_com_itens_em_linhas_separadas_com_aspas)

# Salvando os itens em um arquivo de texto, cada um em uma nova linha
with open('/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/itens_em_linhas_separadas_com_aspas_g8.txt', 'w', encoding='utf-8') as file:
    file.write(string_com_itens_em_linhas_separadas_com_aspas)

pd.read_table("/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/itens_em_linhas_separadas_com_aspas_g8.txt").describe()

"""Retirando espaços e inserindo linhas. codigo opcional porque o anterior ja realiza a contrução das linhas e inserção das virgulas em cada linha"""

# Nome do arquivo de entrada
produtos = '/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/itens_em_linhas_separadas_com_aspas_g8.txt'

# Ler o arquivo de entrada
with open(produtos, 'r', encoding='utf-8') as file:
    linhas = file.readlines()

# Remover espaços em branco e quebras de linha
linhas = [linha.strip() for linha in linhas]

# Adicionar aspas em cada item
#itens_com_aspas = ['"{}"'.format(item) for item in linhas if item]  # Ignora linhas vazias

# Nome do arquivo de saída com um exemplo generico
nome_do_arquivo_de_saida = '/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/itens_formatados_g8.txt'

# Salvando os itens em um arquivo de texto, cada um em uma nova linha
with open(nome_do_arquivo_de_saida, 'w', encoding='utf-8') as file:
    for item in linhas:
        file.write(item + '\n')

print(f"Arquivo '{nome_do_arquivo_de_saida}' salvo com sucesso!")

"""Processamento dos dados para inserção em categorias"""



import re

# Função para determinar a categoria baseada na unidade
def determinar_categoria(parte):
    # Seu dicionário de mapeamento aqui
    unidade_para_categoria = {
    r'(?i)\bgramas\b': 'Peso',
    r'(?i)\bgrama\b': 'Peso',
    r'(?i)\bquilo\b': 'Peso',
    r'(?i)\bquilos\b': 'Peso',
    r'(?i)\bml\b': 'Volume',
    r'(?i)\blitros\b': 'Volume',
    r'(?i)\blitro\b': 'Volume',
    r'(?i)\bsaches\b': 'Quantidade',
    r'(?i)\bunidades\b': 'Quantidade',
    r'(?i)\bunidade\b': 'Quantidade',
    r'(?i)\bsache\b': 'Quantidade',
    r'(?i)\benvelopes\b': 'Quantidade',
    r'(?i)\benvelope\b': 'Quantidade',
    r'(?i)\bpacotes\b': 'Quantidade',
    r'(?i)\bpacote\b': 'Quantidade',
    r'(?i)\bcaixas\b': 'Quantidade',
    r'(?i)\bun\b': 'Quantidade',
    r'(?i)\bcaixa\b': 'Quantidade',
    r'(?i)\bcaixa acoplada\b': 'Tipo',
    r'(?i)\bsaquinhos\b': 'Quantidade',
    r'(?i)\bsaquinho\b':'Quantidade',
    r'(?i)\bfrasco\b': 'Quantidade',
    r'(?i)\bfrascos\b': 'Quantidade',
    r'(?i)\b(?:pacotes|caixas|unidade|sache|envelopes)\b': 'Quantidade',
    r'(?i)\b(?:kg|g|gr)\b': 'Peso',
    r'(?i)\b(?:KG|G|GR)\b': 'Peso',
    r'(?i)\b\d+\s*x\s*\d+\s*(cm|mm|m)\b|\b\d+\s+-\s+\d+\s*(cm|mm|m)\b|\b\d+\s*mm?\s*x\s*\d+\s*mm?(\s*x\s*\d+\s*mm?)?': 'Dimensão',
    r'(?i)\b(?:l|ml)\b': 'Volume',
    r'(?i)\b(?:L|ML)\b': 'Volume',
    r'(?i)\bcapacidade\b': 'Volume',
    r'(?i)\bcapacidade\s+(\d+(\s*-\s*\d+)?\s*(ml|l))\b':'Volume',
    r'(?i)\b(?:kg|g|gr|gramas|quilos)\b': 'Peso',
    r'(?i)\b(?:l|ml|litros|litro|capacidade\s+(\d+(\s*-\s*\d+)?\s*(ml|l)))\b': 'Volume',
    r'(?i)\b(?:unidades|saches|envelopes|pacotes|caixas|saquinhos|frasco|frascos|un)\b': 'Quantidade',
    r'(?i)\b(?:kg|g|gr|gramas|quilos)\b':'Peso',
    r'(?i)\b(?:l|ml|litros|capacidade)\b':'Volume',
    r'(?i)\b(?:unidades|saches|envelopes|pacotes|caixas|saquinhos|frascos)\b':'Quantidade',
    r'\w+\s*,\s*.+': 'Tipo',
    r'(?i)\balto vacuo\b': 'Linha',
    r'(?i)\btradicional\b': 'Linha',
    r'(?i)\bgourmet\b': 'Linha',
    r'(?i)\bcor\b': 'Cor',
    r'(?i)\bnbr\.\s*\d+\b': 'Norma',
    r'(?i)\bNBR\s*\d+\b': 'Norma',
    r'(?i)\bbiodegradável\b': 'Tipo',
    r'(?i)\bsem impressão\b':'Tipo',
    r'(?i)\bpersonalizado\b': 'Tipo',
    r'(?i)\bantiferruginoso\b': 'Tipo',
    r'(?i)\b\d+\s+dobras\b': 'Tipo',
    r'(?i)\bfolha\s+(dupla|simples)\b': 'Tipo',
    r'(?i)\bcristal\b': 'Tipo',
    r'(?i)\bmacio\b':'Tipo',
    r'(?i)\bcomum\b':'Tipo',
    r'(?i)\binox\b':'Material',
    r'(?i)\breciclado\b': 'Material',
    r'(?i)\bseda\b': 'Material',
    r'(?i)\balgodão\b': 'Material',
    r'(?i)\bvidro\b': 'Material',
    r'(?i)\baço\b': 'Material',
    r'(?i)\b(?i)plástico\b':'Material',
    r'(?i)\bpapel\b': 'Material',
    r'(?i)\bnylon\b': 'Material',
    r'(?i)\bbambu\b': 'Material',
    r'(?i)\bmadeira\b': 'Material',
    r'(?i)\bsaco\b':'Tipo',
    r'(?i)\brecarregavel\b':'Tipo',
    r'(?i)\balto vacuo|tradicional|gourmet\b': 'Linha',
    r'(?i)\bnr\.|nr.\s*\d+|biodegradável|sem impressão|personalizado|cristal|dupla|simples|comum\b': 'Tipo',
    r'(?i)\b(?:alto vacuo|tradicional|gourmet|cor|nr\.\s*\d+|NR\s*\d+|biodegradável|sem impressão|personalizado|antiferruginoso|\d+\s+dobras|folha\s+(dupla|simples)|cristal|macio|comum|inox|aço|reciclado|seda|algodão|vidro|plástico|papel|nylon|bambu|madeira|saco)\b': 'Tipo',
    r'(?i)\binox|aço|reciclado|seda|algodão|vidro|plástico|papel|nylon|bambu|madeira\b': 'Material',
    r'(?i)\b(?:azul|vermelha|vermelho|verde|preta|preto|amarela|laranja|rosa|rosa claro|cru|branco|branca|cinza|marrom|bege|branco gelo)\b':'Cor',
    r'(?i)\bbiodegradavel\b':'Tipo',
    r'(?i)\b(?:x|cm|mm|m)\b': 'Dimensão',
    r'(?i)\b(?:x|CM|MM|M)\b': 'Dimensão',
    r'(?i)\b\d+\s*mm?\s*x\s*\d+\s*mm?(\s*x\s*\d+\s*mm?)?\b': 'Dimensão',
    r'(?i)\b\d+\s*x\s*\d+\s*(cm|mm|m)\b|\b\d+\s+-\s+\d+\s*(cm|mm|m)\b': 'Dimensão',
    r'(?i)\b\d+\s*(cm|mm|m)\b': 'Dimensão',
    r'(?i)\b(?!\d+\s*(?:cm|mm|m|CM|MM|M)\b)(\w+\s*,\s*.+)\b': 'Dimensão',
    r'(?i)\b\d+\s*(cm|mm|m|CM|MM|M)\b': 'Dimensão',
    r'(?i)\b\d+\s*x\s*\d+\s*(cm|mm|m|CM|MM|M)\b': 'Dimensão',
    r'^(\d+ CM)$': 'Dimensão',
    r'^(\d+) X (\d+) X (\d+) MM$': 'Dimensão',
    r'^(\d+(\.\d+)? MM X \d+(\.\d+)? M)$': 'Dimensão',
    r'^TIPO .+?DE (\d+(\.\d+)? CM)$': 'Dimensão',
    r'\brolo com \d+ metros\b': 'Dimensão',
    r'(?i)\bTipo\s+(.*)': 'Tipo',
    r'\b(\d+)\s*CM\b': 'Dimensão',
    r'(\d+)\s*(METROS|CM)': 'Dimensão',
    r'(\d+)\s*(METROS|CM)': 'Dimensão',
    r'(\d+)\s*circunferência\s*\d+\s*cm\b': 'Dimensão',
    r'(?i)COD\.\s*[\d\w\.\/-]+': 'Código',
    r'(?i)REF\.\s*[\d\w\.\/-]+': 'Referência',
    r'\bL=\s*\d+([\.,]\d+)?\s*CM\s*X\s*A=\s*\d+([\.,]\d+)?\s*CM\b': 'Dimensão',



    }
    for regex, categoria in unidade_para_categoria.items():
        if re.search(regex, parte, re.IGNORECASE):
            return categoria
    return "Outros"

# Função para processar cada linha do arquivo e retornar como string categorizada
def processar_linha(linha):
    partes = linha.strip().split(' - ')
    nome_item = partes[0]
    categorias = {}

    for parte in partes[1:]:
        categoria = determinar_categoria(parte)
        if categoria:
            categorias.setdefault(categoria, []).append(parte)

    categorias_formatadas = {k: ', '.join(v) for k, v in categorias.items()}
    return f"Nome do Item: {nome_item}; " + ', '.join(f"{k}: {v}" for k, v in categorias_formatadas.items())

# Leitura do arquivo de itens e escrita no novo arquivo categorizado
with open('/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/itens_em_linhas_separadas_com_aspas_g8.txt', 'r', encoding='utf-8') as file:
    linhas = file.readlines()

with open('/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/itens_categorizados_g8.txt', 'w', encoding='utf-8') as novo_arquivo:
    for linha in linhas:
        linha_categorizada = processar_linha(linha)
        novo_arquivo.write(linha_categorizada + '\n')

print("Arquivo 'itens_categorizados.txt' salvo com sucesso!")

"""Leitura do arquivo de saida para conferencia da lista gerada"""

with open('/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/itens_categorizados_g8.txt', 'r') as f:
  text = f.read()
print(text)

"""Inserção da lista no arquivo de leitura de origem, com campo ao lado do campo original para comparação"""

import pandas as pd

# Carregar o DataFrame original
df = pd.read_excel('/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/grupo08_novo.xlsx')

# Ler o arquivo TXT com os itens categorizados
with open('/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/itens_categorizados_g8.txt', 'r', encoding='utf-8') as file:
    itens_categorizados = file.readlines()

# Verificar se o número de linhas do arquivo TXT corresponde ao DataFrame
if len(itens_categorizados) != len(df):
    raise ValueError("O número de linhas do arquivo categorizado não corresponde ao DataFrame original.")

# Adicionar os itens categorizados ao DataFrame em uma nova coluna temporária
df['item_categorizado_temp'] = [linha.strip() for linha in itens_categorizados]

# Obter o índice da coluna 'Item'
index_item = df.columns.get_loc('Item')

# Inserir a coluna 'item categorizado' à direita da coluna 'Item'
df.insert(index_item + 1, 'item categorizado', df['item_categorizado_temp'])

# Remover a coluna temporária
df.drop('item_categorizado_temp', axis=1, inplace=True)

# Salvar o DataFrame atualizado no mesmo formato do arquivo original
df.to_excel('/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/itens_grupo_8_catmat_atualizado.xlsx', index=False)

"""Leitura do arquivo fim para conferencia"""

pd.read_excel("/content/drive/MyDrive/projeto_pmsp_cod_online/grupo_8/itens_grupo_8_catmat_atualizado.xlsx")

"""## FIM DO CODIGO VALIDO

##############################

