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

##############################

----------

#INÍCIO DE CODIGO TESTE
"""

import re

# Seu dicionário de mapeamento aqui
unidade_para_categoria = {
    # ... (inserir todas as expressões regulares do dicionário aqui) ...
    # ... (as expressões regulares já estão inseridas acima) ...
    r'(?i)-\s*COD\.\s*[\d\w\.\/-]+': 'Código',
    r'(?i)COD\.\s*[\d\w\.\/-]+': 'Código',
    r'(?i)REF\.\s*[\d\w\.\/-]+': 'Referência'

    # ... (continuação do dicionário) ...
}

# Função para determinar a categoria baseada na unidade
def determinar_categoria(parte):
    for regex, categoria in unidade_para_categoria.items():
        if re.search(regex, parte, re.IGNORECASE):
            return categoria
    return "Desconhecida"

# Lista de itens para categorizar
itens = [
    "ABAFADOR DO ESCAPAMENTO - COD.46.400.685/TEMPRA",
    # ... (adicionar todos os itens aqui) ...
    "ALAVANCA DE TROCA DE MARCHA - PARA MOTOCICLETA HONDA XRE300 - 2017",
    "ALAVANCA DO CABO DO CAPUZ AUTOMOTIVO - REF. 2S65/16B626/AD1/FORD",
    # ... (adicionar todos os itens aqui) ...
]

# Processar e imprimir cada item com sua categoria
for item in itens:
    partes = item.split(' - ')
    nome_item = partes[0]
    categorias = []

    for parte in partes[1:]:
        categoria = determinar_categoria(parte)
        if categoria:
            categorias.append(f"{categoria}: {parte}")

    print(f"Nome do Item: {nome_item}; " + ', '.join(categorias))



"""# ** VERSOES ANTERIORES **"""

import pandas as pd
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

    }

    for regex, categoria in unidade_para_categoria.items():
        if re.search(regex, parte, re.IGNORECASE):
            return categoria
    return None

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
    return ', '.join(f"{k}: {v}" for k, v in categorias_formatadas.items())

# Ler o arquivo original
with open('/content/itens_em_linhas_separadas_com_aspas.txt', 'r', encoding='utf-8') as file:
    linhas = file.readlines()

# Processar cada linha para obter itens categorizados
itens_categorizados = [processar_linha(linha) for linha in linhas]

# Criar DataFrame com linhas originais e itens categorizados
df = pd.DataFrame({
    'Linha Original': linhas,
    'Itens Categorizados': itens_categorizados
})

# Salvar o DataFrame em um novo arquivo CSV
df.to_csv('itens_com_categorias.csv', index=False, encoding='utf-8-sig')

print("Arquivo 'itens_com_categorias.csv' salvo com sucesso!")

import re

# Função para determinar a categoria baseada na unidade
def determinar_categoria(parte):
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
    r'(?i)\bcor\b': 'Tipo',
    r'(?i)\bnr\.\s*\d+\b': 'Norma',
    r'(?i)\bnr\s*\d+\b': 'Norma',
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
    r'(?i)\b(?:azul|vermelha|vermelho|verde|preta|preto|amarela|laranja|rosa||rosa claro|branca|branco|cinza|marrom|bege)\b':'Tipo',
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
    r'(\d+)\s*(METROS|CM)': 'Dimensão'



}

# Função para extrair as informações de cada produto
def extrair_informacoes(produto):
    partes = produto.split(" - ")
    nome = partes[0].strip()
    quantidade = partes[-1].strip() if len(partes) > 1 else 'sem registro'

    info_produto = {"Nome do Item": nome, "Quantidade": quantidade}

    # Processar as partes intermediárias para extrair informações adicionais
    for parte in partes[1:-1]:
        categoria = determinar_categoria(parte)
        if categoria:
            if categoria in info_produto:
                info_produto[categoria] += f", {parte}"
            else:
                info_produto[categoria] = parte
        # Aqui você pode adicionar mais lógica se precisar processar outras partes

    return info_produto

# Lista de produtos para testar
produtos = [
    "ABRACADEIRA DE NYLON - 2,5 X 100 MM - 100 UNIDADES",
    "ABRACADEIRA DE NYLON - 3,6 X 150 MM - 100 UNIDADES",


    # Adicione mais itens aqui se necessário
]

# Processar e imprimir os produtos
produtos_estruturados = [extrair_informacoes(produto) for produto in produtos]

for produto in produtos_estruturados:
    print(produto)

import pandas as pd
import re

# Função para determinar a categoria baseada na unidade
def determinar_categoria(parte):
    # Seu dicionário de mapeamento aqui
    unidade_para_categoria = {
        # ... (cole seu dicionário aqui)
    }
    for regex, categoria in unidade_para_categoria.items():
        if re.search(regex, parte, re.IGNORECASE):
            return categoria
    return None

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
    return ', '.join(f"{k}: {v}" for k, v in categorias_formatadas.items())

# Ler o arquivo original
with open('itens.txt', 'r', encoding='utf-8') as file:
    linhas = file.readlines()

# Processar cada linha para obter itens categorizados
itens_categorizados = [processar_linha(linha) for linha in linhas]

# Criar DataFrame com linhas originais e itens categorizados
df = pd.DataFrame({
    'Linha Original': linhas,
    'Itens Categorizados': itens_categorizados
})

# Salvar o DataFrame em um novo arquivo CSV
df.to_csv('itens_com_categorias.csv', index=False, encoding='utf-8-sig')

print("Arquivo 'itens_com_categorias.csv' salvo com sucesso!")

"""Importanto dados de coluna de data set"""

import pandas as pd
import re

# Carregar dataset
dataset_path = '/content/GRUPO02_catmat.xlsx'
dataset = pd.read_excel(dataset_path)

# Definindo os códigos para filtragem
codigos_para_filtrar = [215]  # Substitua com os códigos reais

# Filtrar o dataset com base nos códigos
filtro_coluna = 'Natureza'  # Substitua com o nome real da coluna
dataset_filtrado = dataset[dataset[filtro_coluna].isin(codigos_para_filtrar)]

# Lista de produtos para testar (Extraída do dataset filtrado)

# Aqui estou assumindo que os produtos estão em uma coluna chamada 'Produtos'
produtos = dataset_filtrado['Item'].tolist()

# Código para processar e padronizar os produtos
# Dicionário para mapear unidades a suas categorias
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
    r'(?i)\bcor\b': 'Tipo',
    r'(?i)\bnr\.\s*\d+\b': 'Norma',
    r'(?i)\bnr\s*\d+\b': 'Norma',
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
    r'(?i)\b(?:azul|vermelha|vermelho|verde|preta|preto|amarela|laranja|rosa||rosa claro|branca|branco|cinza|marrom|bege)\b':'Tipo',
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
    r'(\d+)\s*(METROS|CM)': 'Dimensão'



}

# Função para determinar a categoria baseada na unidade
def determinar_categoria(parte):
    for regex, categoria in unidade_para_categoria.items():
        if re.search(regex, parte, re.IGNORECASE):
            return categoria
    return None




# Função para extrair as informações de cada produto
def extrair_informacoes(produto):
    partes = re.split(r' - ', produto)
    #produto = produto.replace(' - ', ', ')
    partes = re.split(r';\s*', produto)
    nome = partes[0]
    info_produto = {"Nome do Item": nome}

    for parte in partes[1:]:
        categoria = determinar_categoria(parte)
        if categoria:
            if categoria in info_produto:
                info_produto[categoria] += f", {parte}"
            else:
                info_produto[categoria] = parte
        elif ":" in parte:
          chave, valor = parte.split(":", 1)
          info_produto[chave.strip()] = valor.strip()

    return info_produto




# Processar e imprimir os produtos
produtos_estruturados = [extrair_informacoes(produto) for produto in produtos]

for produto in produtos_estruturados:
    for chave, valor in produto.items():
        print(f"{chave}: {valor}")
    print("\n---\n")

# Criar uma lista de strings formatadas para cada produto
produtos_formatados = []
for produto in produtos_estruturados:
    partes = [f"{k}: {v}" for k, v in produto.items() if v]
    produtos_formatados.append(", ".join(partes))
# Processar e imprimir os produtos
produtos_estruturados = [extrair_informacoes(produto) for produto in produtos]

for produto in produtos_estruturados:
    for chave, valor in produto.items():
        print(f"{chave}: {valor}")
    print("\n---\n")



# Criar uma lista de strings formatadas para cada produto
produtos_formatados = []
for produto in produtos_estruturados:
    partes = [f"{k}: {v}" for k, v in produto.items() if v != 'sem registro']
    linha_formatada = "; ".join(partes)
    produtos_formatados.append(linha_formatada)


# Criar DataFrame
df = pd.DataFrame({'Item': produtos_formatados})

# Salvar em CSV
caminho_csv = "/content/itens_padronizados.csv"
df.to_csv(caminho_csv, index=False, encoding='utf-8-sig')

print(f"Arquivo '{caminho_csv}' salvo com sucesso!")

pd.read_csv("/content/itens_padronizados.csv", sep=",")

pd.read_excel("/content/GRUPO02_catmat.xlsx")

"""##Inserir para analise, os itens NATUREZA: 215, 070, 051"""

import re
import pandas as pd


# Dicionário para mapear unidades a suas categorias
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
    r'(?i)\bcor\b': 'Tipo',
    r'(?i)\bnr\.\s*\d+\b': 'Norma',
    r'(?i)\bnr\s*\d+\b': 'Norma',
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
    r'(?i)\b(?:azul|vermelha|vermelho|verde|preta|preto|amarela|laranja|rosa||rosa claro|branca|branco|cinza|marrom|bege)\b':'Tipo',
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
    r'(\d+)\s*(METROS|CM)': 'Dimensão'



}

# Função para determinar a categoria baseada na unidade

def determinar_categoria(parte):
    # Padrão para capturar medidas de dimensão (ex: "30 CM", "40 CM")
    padrao_dimensao = re.compile(r'\b\d+(\.\d+)?\s*(cm|mm|m)\b', re.IGNORECASE)

    # Verificar primeiro as categorias específicas
    for regex, categoria in unidade_para_categoria.items():
        if re.search(regex, parte, re.IGNORECASE):
            return categoria

    # Verificar se é uma medida de dimensão
    if padrao_dimensao.search(parte):
        return 'Dimensão'

    # Se não for número e estiver depois da primeira vírgula ou hífen, classificar como 'Tipo'
    if not re.search(r'\d', parte):
        return 'Tipo'

    return None




# Função para extrair as informações de cada produto
def extrair_informacoes(produto):
    partes = re.split(r', | - ', produto)
    nome = partes[0]
    info_produto = {"Nome do Item": nome}

    for parte in partes[1:]:
        categoria = determinar_categoria(parte)
        if categoria:
            if categoria in info_produto:
                info_produto[categoria] += f", {parte}"
            else:
                info_produto[categoria] = parte

    return info_produto




# Lista de produtos para testar
produtos = [
        "ACUCAR CRISTAL",
        "ACUCAR REFINADO AMORFO/MICROCRISTALINO",
        "ACUCAR REFINADO GRANULADO  SACHE DE 5 GRAMAS",
        "ACUCAR REFINADO - COM 400 SACHES DE 5 GRAMAS",
        "ACUCAR CRISTAL ORGANICO",
        "CAFE TORRADO MOIDO, PACOTE COM 250 GRAMAS",
        "CAFE TORRADO E MOIDO - ALMOFADA DE 500 GRAMAS",
        "CAFE TORRADO E MOIDO - ALTO VACUO DE 500 GRAMAS - SUPERIOR",
        "CAFE TORRADO E MOIDO, TIPO GOURMET, ALTO VACUO - 500 GRAMAS",
        "CAFE TORRADO E MOIDO, TRADICIONAL - ALTO VACUO DE 500 GRAMAS",
        "FILTRO DE PAPEL PARA CAFE NR 103 - CAIXA COM 40 UNIDADES",
        "FILTRO DE PAPEL PARA CAFE NR, 103 - 30 UNIDADES",
        "FILTRO PARA CAFE NR, 102 - CAIXA COM 30 UNIDADES",
        "FILTRO DE PAPEL PARA CAFE NR. 102 - 30 UNIDADES",
        "FILTRO DE PAPEL PARA CAFETEIRA ELETRICA, NR. 04 - 30 UNIDADES",
        "CHA DE BOLDO DO CHILE, COM 15 SACHES - 15 GRAMAS",
        "CHA DE CAMOMILA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE CAMOMILA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE CAMOMILA, COM 25 SACHES - 40 GRAMAS",
        "CHA DE CAPIM LIMAO - 1 QUILO",
        "CHA DE CAPIM CIDREIRA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 20 SACHES - 20 GRAMAS",
        "CHA DE ERVA DOCE - 1 QUILO",
        "CHA DE ERVA DOCE, COM 10 SACHES - 20 GRAMAS",
        "CHA DE ERVA DOCE, COM 10 SACHES - 9 GRAMAS",
        "CHA DE ERVA DOCE, COM 15 SACHES - 30 GRAMAS",
        "CHA DE ERVA DOCE, COM 25 SACHES - 40 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 10 SACHES - 20 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 15 SACHES - 24 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 15 SACHES - 30 GRAMAS",
        "CHA DE GENGIBRE COM ESPECIARIAS, COM 10 SACHES - 10 GRAMAS",
        "CHA DE HORTELA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE HORTELA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE HORTELA, COM 25 SACHES - 40 GRAMAS",
        "CHA DE MACA COM CANELA, COM 10 SACHES - 30 GRAMAS",
        "CHA DE MACA COM CANELA, COM 15 SACHES - 30 GRAMAS",
        "CHA DE MACA VERMELHA, COM 10 SACHES - 15 GRAMAS",
        "CHA DE MACA VERMELHA, COM 10 SACHES - 20 GRAMAS",
        "CHA DE MORANGO, COM 10 SACHES - 15 GRAMAS",
        "CHA DE PESSEGO, COM 25 SACHES - 40 GRAMAS",
        "CHA MATE - 200 GRAMAS",
        "CHA MATE - 250 GRAMAS",
        "CHA MATE NATURAL - CAIXA COM 25 SAQUINHOS",
        "CHA MATE, COM 20 SACHES - 32 GRAMAS",
        "CHA MATE, SABOR LIMAO, COM 25 SACHES - 40 GRAMAS",
        "CHA MATE, SABOR NATURAL, COM 25 SACHES - 40 GRAMAS",
        "CHA MISTO DE FRUTAS E FLORES CITRICAS, COM 15 SACHES - 15 GRAMAS",
        "CHA PRETO, COM 15 SACHES - 15 GRAMAS",
        "CHA PRETO, SABOR LIMAO - 340 ML",
        "CHA VERDE, COM 10 SACHES - 16 GRAMAS",
        "CHA VERDE, COM 15 SACHES - 24 GRAMAS",
        "ADOCANTE DIETETICO EM PO, ASPARTAME, SACHE 0,8 GRAMAS - 1000 ENVELOPES",
        "ADOCANTE EM PO (ASPARTAME) - 0,8 GRAMAS - 50 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,6 GRAMAS - 1000 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,8 GRAMAS - 1000 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,8 GRAMAS - 50 UNIDADES",
        "ADOCANTE EM SACHE - 50 UNIDADES",
        "ADOCANTE LIQUIDO - 100 ML",
        "ADOCANTE LIQUIDO (ASPARTAME) - FRASCO COM 100 ML",
        "ADOCANTE LIQUIDO (SACARINA) - FRASCO COM 100 ML",
        "ADOCANTE LIQUIDO (SUCRALOSE) - 100 ML",
        "MEXEDOR DE BAMBU PARA CAFE, COMPRIMENTO 10 CM - 1000 UNIDADES",
        "MEXEDOR DE MADEIRA PARA CAFE, TIPO PALHETA - 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO COLHER - 200 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO ESPATULA DE 9 CM - PACOTE COM 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO ESPATULA DE 9 CM - PACOTE COM 500 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 250 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 500 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 60 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 180 A 220 ML",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 45 A 60 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 200 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 180 A 220 ML - 50 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 45 A 60 ML - 55 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 70 ML - 50 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 180 ML  - 100 UNIDADES",
        "COPO PLASTICO DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 180 ML - PACOTE COM 100 UNIDADES",
        "COPO DE PLASTICO DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - PACOTE COM 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, CAPACIDADE 200 ML - PACOTE COM 25 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 100 ML - 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, CAPACIDADE 200 ML - PACOTE COM 25 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 100 ML - 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - 100 UNIDADES",
        "COPO, EM FIBRA DE COCO E POLIPROPILENO - 300 ML",
        "COPO PERSONALIZADO, EM FIBRA DE COCO - 350 ML",
        "COPO PLASTICO DESCARTAVEL PARA CAFE - CAPACIDADE 50 ML",
        "COPO PLASTICO DESCARTAVEL PARA AGUA - CAPACIDADE 150 ML",
        "COPO PLASTICO DESCARTAVEL - 200 ML",
        "COPO PLASTICO DESCARTAVEL - 60 ML",
        "COPO PLASTICO DESCARTAVEL - 80 ML",
        "COPO PLASTICO DESCARTAVEL - 180 ML",
        "GAS LIQUEFEITO DE PETROLEO - BOTIJAO COM 13 QUILOS",
        "GAS LIQUEFEITO DE PETROLEO - CILINDRO COM 45 QUILOS",
        "GAS LIQUEFEITO DE PETROLEO",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 3 - AZUL",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 3 - PRETA",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - AZUL",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - PRETA",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - VERMELHA",
        "APONTADOR PARA LAPIS",
        "APONTADOR PARA LAPIS SIMPLES COM RESERVATORIO",
        "BORRACHA BICOLOR - LAPIS/TINTA",
        "BORRACHA BRANCA PARA LAPIS",
        "BORRACHA DE PAPELARIA PARA GRAFITE, EM LATEX NATURAL, BRANCA - NR. 40",
        "BORRACHA VERDE - GRANDE",
        "CADERNO CAPA DURA 1/4 - 96 A 100 FOLHAS EM PAPEL RECICLADO",
        "CAIXA PARA ARQUIVO MORTO EM PAPELAO - 360 X 250 X 135 MM",
        "CAIXA PARA ARQUIVO MORTO EM PAPELAO - 360 X 250 X 140 MM",
        "CALCULADORA ELETRONICA DE MESA COM 12 DIGITOS",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - AZUL",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - PRETA",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - VERMELHA",
        "CANETA ESFEROGRAFICA TRACO 1 MM - AZUL",
        "CANETA ESFEROGRAFICA TRACO 1 MM - PRETA",
        "CANETA ESFEROGRAFICA TRACO 1 MM - VERMELHA",
        "CANETA MARCA TEXTO COR - AMARELA",
        "CANETA MARCA COR - LARANJA",
        "CANETA MARCA - TEXTO - ROSA",
        "CANETA MARCA - TEXTO - VERDE",
        "CANETA PARA RETROPROJETOR - AZUL",
        "CANETA PARA RETROPROJETOR - VERMELHA",
        "CANETA PARA RETROPROJETOR PRETA - CAIXA 12 UNIDADES",
        "COLA EM BASTAO - PEQUENA, LAVAVEL - TUBO COM APROXIMADAMENTE 8 A 10 GRAMAS",
        "COLA EM BASTAO, A BASE DE AGUA, ATOXICA - 21 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 110 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 225 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 40 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 90 GRAMAS",
        "COLA LIQUIDA TRANSPARENTE, LAVAVEL - TUBO COM 40 GRAMAS",
        "CORRETIVO EM FITA - 5 MM X 6 M",
        "CORRETIVO EM FITA 4,2 MM X 8,5 M",
        "CORRETIVO EM FITA DE 5 MM - ROLO COM 5 M",
        "CORRETIVO LIQUIDO, A BASE DE AGUA - FRASCO DE 16 A 20 ML",
        "CORRETIVO LIQUIDO, BRANCO - FRASCO COM 18 ML",
        "ENVELOPE SEM IMPRESSAO 75G/M2 - 114 X 229 MM - PAPEL RECICLADO",
        "LAPIS BORRACHA",
        "LAPIS GRAFITE - 2 MM",
        "LAPIS PRETO NR,2 - MADEIRA DE MANEJO SUSTENTAVEL",
        "LAPIS PRETO NR.2",
        "LAPIS PRETO NR.2 - MADEIRA DE MANEJO SUSTENTAVEL",
        "LAPISEIRA, CORPO EM PLASTICO RECICLADO, COM CLIPE, PONTA E ACIONADOR DE METAL/BORRACHA - 0,7 MM",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - AZUL",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - PRETO",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - VERDE",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - VERMELHO",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 38 X 50 MM - BLOCO COM 100 FOLHAS",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 76 X 102 MM - BLOCO COM 100 FOLHAS",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 76 X 76 MM - BLOCO COM 100 FOLHAS",
        "PAPEL SULFITE COM CERTIFICADO AMBIENTAL, BRANCO, A4 - 75 G/M2 - 210 X 297 MM",
        "PAPEL SULFITE RECICLADO A4 - 75G/M2 - 210 X 297 MM",
        "PAPEL SULFITE COM CERTIFICADO AMBIENTAL, BRANCO, A3 - 75 G/M2 - 297 X 420 MM",
        "PASTA PARA PRONTUARIO - ROSA CLARO",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - VERDE",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - VERMELHO",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - VERDE",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - VERMELHO",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - VERMELHO",
        "PORTA FITA ADESIVA - PEQUENO",
        "PORTA TUDO - (LAPIS, CLIPS E PAPEL)",
        "REABASTECEDOR PARA PINCEL ATOMICO - PRETO",
        "REABASTECEDOR PARA PINCEL ATOMICO - VERMELHO",
        "REGUA PLASTICA - DIMENSÃO 30 CM",
        "REGUA PLASTICA - DIMENSÃO 40 CM",
        "TESOURA DE ACO INOX - USO GERAL (10 A 15 CM) - MEDIA",
        "TESOURA DE ACO INOX - USO GERAL (16 A 22 CM) - GRANDE",
        "TINTA PARA CARIMBO - AZUL - TUBO DE 40 A 50 ML",
        "TINTA PARA CARIMBO - PRETA - TUBO DE 40 A 50 ML",
        "TINTA PARA CARIMBO - VERMELHA - TUBO DE 40 A 50 ML",
        "PAPEL TOALHA EM BOBINA, FOLHA SIMPLES - 20 CM X 200 M",
        "PAPEL TOALHA INTERFOLHA 2 DOBRAS (1 VINCO) - 220 A 230 MM X 220 A 230 MM - PACOTE COM 4 X 250 FOLHAS",
        "PAPEL TOALHA PICOTADO - FOLHA DUPLA - PACOTE COM 2 UNIDADES",
        "PAPEL TOALHA EM BOBINA - ROLO COM 50 METROS",
        "PAPEL TOALHA INTERFOLHA 2 DOBRAS (1 VINCO) - 220 A 230 MM X 260 A 270 MM - PACOTE COM 4 X 250",
        "PAPEL TOALHA INTERFOLHA 2 DOBRAS - 230 X 210 MM - PACOTE COM 1000 FOLHAS",
        "PAPEL TOALHA EM BOBINA - ROLO COM 100 METROS",
        "PAPEL TOALHA INTERFOLHA 3 DOBRAS, 230 X 270 MM - 1000 FOLHAS",
        "PAPEL TOALHA, FOLHA DUPLA, 20 X 22 CM - ROLO COM 60 FOLHAS",
        "PAPEL HIGIENICO, FOLHA DUPLA, 100 MM X 30 M - SELO FSC",
        "PAPEL HIGIENICO - ROLO - COM 40 METROS",
        "PAPEL HIGIENICO - ROLO - COM 600 METROS",
        "PAPEL HIGIENICO - ROLO - COM 300 METROS",
        "PAPEL HIGIENICO - ROLO - COM 30 METROS",
        "PAPEL HIGIENICO, FOLHA SIMPLES, ROLO 300 METROS - PACOTE COM 8 UNIDADES",
        "AGUA SANITARIA ALVEJANTE E DESINFETANTE - FRASCO COM 1 LITRO",
        "ALCOOL ANTISSEPTICO 70%, EM GEL - 5 LITROS",
        "ALCOOL ETILICO 46% - FRASCO COM 1 LITRO",
        "ALCOOL ETILICO 70% (P/P) SOLUCAO ALMOTOLIA 100 ML",
        "ALCOOL ETILICO HIDRATADO 70 INPM - 1 LITRO",
        "ALCOOL ETILICO HIDRATADO 70 INPM, EM GEL - 440 GRAMAS",
        "ALCOOL GEL 70% - FRASCO COM 500 ML",
        "ALCOOL LIQUIDO 70 % - 1 LITRO",
        "DESENGRIPANTE DE USO GERAL - ANTIFERRUGINOSO E LUBRIFICANTE AEROSOL - DE 300 ML",
        "DETERGENTE EM PO - SACO COM 1 QUILO",
        "DETERGENTE EM PO BIODEGRADAVEL - SACO COM 5 QUILOS",
        "DETERGENTE LIQUIDO - BIODEGRADAVEL - FRASCO COM 500 ML",
        "ESPONJA DE ESPUMA - DUPLA FACE",
        "ESPONJA DE LA DE ACO - PACOTE COM 08 UNIDADES",
        "ESPONJA FIBRACO - DUPLA FACE",
        "LAVATINA - DE NYLON PARA VASO SANITARIO - TIPO VASSOURINHA",
        "LIMPADOR GERAL DE MULTIPLO USO LIMPEZA INSTANTANEA - FRASCO COM 500 ML",
        "PA PARA LIXO COM CABO DE MADEIRA LONGO",
        "PANO DE ALGODAO PARA COPA - 40 X 60 CM",
        "PANO DE ALGODAO PARA COPA - 45 X 75 CM",
        "PANO DE FLANELA - 27 X 37 CM",
        "PANO DE FLANELA - 28 X 38 CM",
        "PANO DE FLANELA - 30 X 40 CM",
        "PANO DE FLANELA - 30 X 50 CM",
        "PANO DE FLANELA - 30 X 60 CM",
        "PANO DE FLANELA - 38 X 58 CM",
        "PANO DE FLANELA - 60 X 40 CM",
        "PANO PARA CHAO - TIPO SACO",
        "RECIPIENTE PARA MATERIAL PERFURO CORTANTE - 7 LITROS",
        "RODO ENXUGADOR - DIMENSÃO 30 CM",
        "RODO ENXUGADOR - DIMENSÃO 40 CM",
        "RODO ENXUGADOR, DIMENSÃO 60 CM",
        "SABAO COMUM EM PEDRA - PEDACO DE 200 GRAMAS",
        "SABAO DE COCO - PEDACO DE 200 GRAMAS",
        "SABAO EM PO",
        "SACO PLASTICO PARA LIXO - 100 LITROS (20 KG) - 75 X 105 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 100 LITROS (20 KG) - 75 X 105 CM - VERMELHO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 20 LITROS",
        "SACO PLASTICO PARA LIXO - 30 LITROS (6 KG) - 59 X 62 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 40 LITROS",
        "SACO PLASTICO PARA LIXO - 50 LITROS (10 KG) - 63 X 80 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 60 LITROS",
        "SACO PLASTICO PARA LIXO VERDE - CAPACIDADE 60 LITROS",
        "VASSOURA DE PELO - 30 CM",
        "VASSOURA DE PELO - 40 CM",
        "VASSOURA DE PELO - 60 CM",
        "VASSOURA DE PIACAVA - NR.04",
        "VASSOURAO DE PIACAVA TIPO PREFEITURA - 40 CM"

]

# Processar e imprimir os produtos
produtos_estruturados = [extrair_informacoes(produto) for produto in produtos]

for produto in produtos_estruturados:
    for chave, valor in produto.items():
        print(f"{chave}: {valor}")
    print("\n---\n")



# Criar uma lista de strings formatadas para cada produto
produtos_formatados = []
for produto in produtos_estruturados:
    partes = [f"{k}: {v}" for k, v in produto.items() if v != 'sem registro']
    linha_formatada = "; ".join(partes)
    produtos_formatados.append(linha_formatada)


# Criar DataFrame
df = pd.DataFrame({'Item': produtos_formatados})

# Salvar em CSV
caminho_csv = "/content/itens_padronizados.csv"
df.to_csv(caminho_csv, index=False, encoding='utf-8-sig')

print(f"Arquivo '{caminho_csv}' salvo com sucesso!")

pd.read_csv("/content/itens_padronizados.csv")

import re

# Dicionário para mapear unidades a suas categorias
unidade_para_categoria = {
    # ...outras expressões regulares...
    r'\b\d+\s*(cm|mm|m|CM|MM|M)\b': 'Dimensão',
    r'\b\d+\s*x\s*\d+\s*(cm|mm|m|CM|MM|M)\b': 'Dimensão',
    # ...expressões regulares para Peso, Volume, Quantidade, etc...
    r'(?i)\b(?:alto vacuo|tradicional|gourmet|cor|nr.|nr\.\s*\d+|biodegradável|sem impressão|personalizado|antiferruginoso|\d+\s+dobras|folha\s+(dupla|simples)|picotado|cristal|macio|comum|inox|aço|reciclado|seda|algodão|vidro|plástico|papel|nylon|bambu|madeira|saco|recarregavel|azul|vermelha|vermelho|verde|preta|preto|amarela|laranja|rosa|rosa claro|branca|branco|cinza|marrom|bege)\b': 'Tipo',
    # Evitar que 'Tipo' capture padrões que deveriam ser 'Dimensão'
    r'(?i)\b(?!\d+\s*(?:cm|mm|m|CM|MM|M)\b)(\w+\s*,\s*.+)\b': 'Tipo',
    # ...expressões regulares para Material, Linha, Norma, etc...
    #r'(?i)\b(?:alto vacuo|tradicional|gourmet|color|nr\.\s*\d+|biodegradável|sem impressão|personalizado|antiferruginoso|\d+\s+dobras|folha\s+(dupla|simples)|cristal|macio|comum|inox|aço|reciclado|seda|algodão|vidro|plástico|papel|nylon|bambu|madeira|saco|recarregavel|azul|vermelha|vermelho|verde|preta|preto|amarela|laranja|rosa|rosa claro|branca|branco|cinza|marrom|bege)\b': 'Tipo',
    r'(?i)\b(?:kg|g|gr|gramas|quilos)\b': 'Peso',
    r'(?i)\b(?:l|ml|litros|litro|capacidade)\b': 'Volume',
    r'(?i)\b(?:unidades|saches|envelopes|pacotes|caixas|saquinhos|frascos)\b': 'Quantidade',
    r'(?i)\b(?:alto vacuo|tradicional|gourmet)\b': 'Linha',
    r'(?i)\b(?:inox|aço|reciclado|seda|algodão|vidro|plástico|papel|nylon|bambu|madeira)\b': 'Material',
    r'(?i)\bnr\.\s*\d+\b': 'Norma',
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
    r'(?i)\bsaquinhos\b': 'Quantidade',
    r'(?i)\bsaquinho\b':'Quantidade',
    r'(?i)\bfrasco\b': 'Quantidade',
    r'(?i)\bfrascos\b': 'Quantidade',
    r'(?i)\b(?:pacotes|caixas|unidade|sache|envelopes)\b': 'Quantidade',
    r'(?i)\b(?:kg|g|gr)\b': 'Peso',
    r'(?i)\b(?:KG|G|GR)\b': 'Peso',
    r'(?i)\b(?:l|ml)\b': 'Volume',
    r'(?i)\b(?:L|ML)\b': 'Volume',
    r'(?i)\bcapacidade\b': 'Volume',
    r'(?i)\bcapacidade\s+(\d+(\s*-\s*\d+)?\s*(ml|l))\b':'Volume',
    r'(?i)\b(?:kg|g|gr|gramas|quilos)\b': 'Peso',
    r'(?i)\b(?:l|ml|litros|litro|capacidade\s+(\d+(\s*-\s*\d+)?\s*(ml|l)))\b': 'Volume',
    r'(?i)\b(?:unidades|saches|envelopes|pacotes|caixas|saquinhos|frasco|frascos|un|nr)\b': 'Quantidade',
    r'(?i)\b(?:kg|g|gr|gramas|quilos)\b':'Peso',
    r'(?i)\b(?:l|ml|litros|capacidade)\b':'Volume',
    r'(?i)\b(?:unidades|saches|envelopes|pacotes|caixas|saquinhos|frascos)\b':'Quantidade',
    r'(?i)\balto vacuo\b': 'Linha',
    r'(?i)\btradicional\b': 'Linha',
    r'(?i)\bgourmet\b': 'Linha',
    r'(?i)\bnr\.\s*\d+\b': 'Norma',
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
    r'(?i)\balto vacuo|tradicional|gourmet\b': 'Linha',
}

def determinar_categoria(parte):
    for regex, categoria in unidade_para_categoria.items():
        if re.search(regex, parte, re.IGNORECASE):
            return categoria
    return None

def extrair_informacoes(produto):
    partes = re.split(r', | - ', produto)
    nome = partes[0]
    info_produto = {}

    # Processa cada parte do produto
    for parte in partes[1:]:
        categoria = determinar_categoria(parte)
        if categoria:
            # Adiciona a categoria ao dicionário se não estiver presente
            if categoria not in info_produto:
                info_produto[categoria] = parte
            # Para "Tipo", acumula valores adicionais se já existir
            elif categoria == 'Tipo':
                info_produto[categoria] += f", {parte}"

    return {"Nome do Item": nome, **info_produto}

# Lista de produtos para testar
produtos = [
     "ACUCAR CRISTAL",
        "ACUCAR REFINADO AMORFO/MICROCRISTALINO",
        "ACUCAR REFINADO GRANULADO - SACHE DE 5 GRAMAS",
        "ACUCAR REFINADO, COM 400 SACHES DE 5 GRAMAS",
        "ACUCAR CRISTAL ORGANICO",
        "CAFE TORRADO MOIDO, PACOTE COM 250 GRAMAS",
        "CAFE TORRADO E MOIDO - ALMOFADA DE 500 GRAMAS",
        "CAFE TORRADO E MOIDO - ALTO VACUO DE 500 GRAMAS - SUPERIOR",
        "CAFE TORRADO E MOIDO, TIPO GOURMET, ALTO VACUO - 500 GRAMAS",
        "CAFE TORRADO E MOIDO, TRADICIONAL - ALTO VACUO DE 500 GRAMAS",
        "FILTRO DE PAPEL PARA CAFE NR, 103 - CAIXA COM 40 UNIDADES",
        "FILTRO DE PAPEL PARA CAFE NR, 103 - 30 UNIDADES",
        "FILTRO PARA CAFE NR, 102 - CAIXA COM 30 UNIDADES",
        "FILTRO DE PAPEL PARA CAFE NR. 102 - 30 UNIDADES",
        "FILTRO DE PAPEL PARA CAFETEIRA ELETRICA, NR. 04 - 30 UNIDADES",
        "CHA DE BOLDO DO CHILE, COM 15 SACHES - 15 GRAMAS",
        "CHA DE CAMOMILA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE CAMOMILA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE CAMOMILA, COM 25 SACHES - 40 GRAMAS",
        "CHA DE CAPIM LIMAO - 1 QUILO",
        "CHA DE CAPIM CIDREIRA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 20 SACHES - 20 GRAMAS",
        "CHA DE ERVA DOCE - 1 QUILO",
        "CHA DE ERVA DOCE, COM 10 SACHES - 20 GRAMAS",
        "CHA DE ERVA DOCE, COM 10 SACHES - 9 GRAMAS",
        "CHA DE ERVA DOCE, COM 15 SACHES - 30 GRAMAS",
        "CHA DE ERVA DOCE, COM 25 SACHES - 40 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 10 SACHES - 20 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 15 SACHES - 24 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 15 SACHES - 30 GRAMAS",
        "CHA DE GENGIBRE COM ESPECIARIAS, COM 10 SACHES - 10 GRAMAS",
        "CHA DE HORTELA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE HORTELA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE HORTELA, COM 25 SACHES - 40 GRAMAS",
        "CHA DE MACA COM CANELA, COM 10 SACHES - 30 GRAMAS",
        "CHA DE MACA COM CANELA, COM 15 SACHES - 30 GRAMAS",
        "CHA DE MACA VERMELHA, COM 10 SACHES - 15 GRAMAS",
        "CHA DE MACA VERMELHA, COM 10 SACHES - 20 GRAMAS",
        "CHA DE MORANGO, COM 10 SACHES - 15 GRAMAS",
        "CHA DE PESSEGO, COM 25 SACHES - 40 GRAMAS",
        "CHA MATE - 200 GRAMAS",
        "CHA MATE - 250 GRAMAS",
        "CHA MATE NATURAL - CAIXA COM 25 SAQUINHOS",
        "CHA MATE, COM 20 SACHES - 32 GRAMAS",
        "CHA MATE, SABOR LIMAO, COM 25 SACHES - 40 GRAMAS",
        "CHA MATE, SABOR NATURAL, COM 25 SACHES - 40 GRAMAS",
        "CHA MISTO DE FRUTAS E FLORES CITRICAS, COM 15 SACHES - 15 GRAMAS",
        "CHA PRETO, COM 15 SACHES - 15 GRAMAS",
        "CHA PRETO, SABOR LIMAO - 340 ML",
        "CHA VERDE, COM 10 SACHES - 16 GRAMAS",
        "CHA VERDE, COM 15 SACHES - 24 GRAMAS",
        "ADOCANTE DIETETICO EM PO, ASPARTAME, SACHE 0,8 GRAMAS - 1000 ENVELOPES",
        "ADOCANTE EM PO (ASPARTAME) - 0,8 GRAMAS - 50 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,6 GRAMAS - 1000 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,8 GRAMAS - 1000 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,8 GRAMAS - 50 UNIDADES",
        "ADOCANTE EM SACHE - 50 UNIDADES",
        "ADOCANTE LIQUIDO - 100 ML",
        "ADOCANTE LIQUIDO (ASPARTAME) - FRASCO COM 100 ML",
        "ADOCANTE LIQUIDO (SACARINA) - FRASCO COM 100 ML",
        "ADOCANTE LIQUIDO (SUCRALOSE) - 100 ML",
        "MEXEDOR DE BAMBU PARA CAFE, COMPRIMENTO 10 CM - 1000 UNIDADES",
        "MEXEDOR DE MADEIRA PARA CAFE, TIPO PALHETA - 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO COLHER - 200 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO ESPATULA DE 9 CM - PACOTE COM 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO ESPATULA DE 9 CM - PACOTE COM 500 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 250 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 500 UNIDADES",
        "COPO DE PAPEL, DESCARTAVEL PARA CAFE - CAPACIDADE 60 ML",
        "COPO DE PAPEL, DESCARTAVEL PARA AGUA - CAPACIDADE 180 A 220 ML",
        "COPO DE PAPEL, DESCARTAVEL PARA CAFE - CAPACIDADE 45 A 60 ML",
        "COPO DE PAPEL, DESCARTAVEL PARA AGUA - CAPACIDADE 200 ML",
        "COPO DE PAPEL, DESCARTAVEL PARA AGUA - CAPACIDADE 180 A 220 ML - 50 UNIDADES",
        "COPO DE PAPEL, DESCARTAVEL PARA CAFE - CAPACIDADE 45 A 60 ML - 55 UNIDADES",
        "COPO DE PAPEL, DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 70 ML - 50 UNIDADES",
        "COPO DE PAPEL, DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 180 ML  - 100 UNIDADES",
        "COPO PLASTICO, DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 180 ML - PACOTE COM 100 UNIDADES",
        "COPO DE PLASTICO, DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - PACOTE COM 100 UNIDADES",
        "COPO DE PAPEL, DESCARTAVEL, CAPACIDADE 200 ML - PACOTE COM 25 UNIDADES",
        "COPO DE PAPEL, DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 100 ML - 100 UNIDADES",
        "COPO DE PAPEL, DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - 100 UNIDADES",
        "COPO DE PAPEL, DESCARTAVEL, CAPACIDADE 200 ML - PACOTE COM 25 UNIDADES",
        "COPO DE PAPEL, DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 100 ML - 100 UNIDADES",
        "COPO DE PAPEL, DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - 100 UNIDADES",
        "COPO, EM FIBRA DE COCO E POLIPROPILENO - 300 ML",
        "COPO PERSONALIZADO, EM FIBRA DE COCO - 350 ML",
        "COPO PLASTICO, DESCARTAVEL PARA CAFE - CAPACIDADE 50 ML",
        "COPO PLASTICO,DESCARTAVEL PARA AGUA - CAPACIDADE 150 ML",
        "COPO PLASTICO, DESCARTAVEL - 200 ML",
        "COPO PLASTICO, DESCARTAVEL - 60 ML",
        "COPO PLASTICO, DESCARTAVEL - 80 ML",
        "COPO PLASTICO, DESCARTAVEL - 180 ML",
        "GAS LIQUEFEITO DE PETROLEO - BOTIJAO COM 13 QUILOS",
        "GAS LIQUEFEITO DE PETROLEO - CILINDRO COM 45 QUILOS",
        "GAS LIQUEFEITO DE PETROLEO",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 3 - AZUL",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 3 - PRETA",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - AZUL",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - PRETA",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - VERMELHA",
        "APONTADOR PARA LAPIS",
        "APONTADOR PARA LAPIS SIMPLES COM RESERVATORIO",
        "BORRACHA BICOLOR - LAPIS/TINTA",
        "BORRACHA BRANCA PARA LAPIS",
        "BORRACHA DE PAPELARIA PARA GRAFITE, EM LATEX NATURAL, BRANCA - NR. 40",
        "BORRACHA VERDE - GRANDE",
        "CADERNO CAPA DURA 1/4 - 96 A 100 FOLHAS EM PAPEL RECICLADO",
        "CAIXA PARA ARQUIVO MORTO EM PAPELAO - 360 X 250 X 135 MM",
        "CAIXA PARA ARQUIVO MORTO EM PAPELAO - 360 X 250 X 140 MM",
        "CALCULADORA ELETRONICA DE MESA COM 12 DIGITOS",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - AZUL",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - PRETA",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - VERMELHA",
        "CANETA ESFEROGRAFICA TRACO 1 MM - AZUL",
        "CANETA ESFEROGRAFICA TRACO 1 MM - PRETA",
        "CANETA ESFEROGRAFICA TRACO 1 MM - VERMELHA",
        "CANETA MARCA TEXTO COR - AMARELA",
        "CANETA MARCA COR - LARANJA",
        "CANETA MARCA - TEXTO - ROSA",
        "CANETA MARCA - TEXTO - VERDE",
        "CANETA PARA RETROPROJETOR - AZUL",
        "CANETA PARA RETROPROJETOR - VERMELHA",
        "CANETA PARA RETROPROJETOR PRETA - CAIXA 12 UNIDADES",
        "COLA EM BASTAO - PEQUENA, LAVAVEL - TUBO COM APROXIMADAMENTE 8 A 10 GRAMAS",
        "COLA EM BASTAO, A BASE DE AGUA, ATOXICA - 21 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 110 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 225 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 40 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 90 GRAMAS",
        "COLA LIQUIDA TRANSPARENTE, LAVAVEL - TUBO COM 40 GRAMAS",
        "CORRETIVO EM FITA - 5 MM X 6 M",
        "CORRETIVO EM FITA 4,2 MM X 8,5 M",
        "CORRETIVO EM FITA DE 5 MM - ROLO COM 5 M",
        "CORRETIVO LIQUIDO, A BASE DE AGUA - FRASCO DE 16 A 20 ML",
        "CORRETIVO LIQUIDO, BRANCO - FRASCO COM 18 ML",
        "ENVELOPE SEM IMPRESSAO 75G/M2 - 114 X 229 MM - PAPEL RECICLADO",
        "LAPIS BORRACHA",
        "LAPIS GRAFITE - 2 MM",
        "LAPIS PRETO NR,2 - MADEIRA DE MANEJO SUSTENTAVEL",
        "LAPIS PRETO NR.2",
        "LAPIS PRETO NR.2 - MADEIRA DE MANEJO SUSTENTAVEL",
        "LAPISEIRA, CORPO EM PLASTICO RECICLADO, COM CLIPE, PONTA E ACIONADOR DE METAL/BORRACHA - 0,7 MM",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - AZUL",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - PRETO",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - VERDE",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - VERMELHO",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 38 X 50 MM - BLOCO COM 100 FOLHAS",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 76 X 102 MM - BLOCO COM 100 FOLHAS",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 76 X 76 MM - BLOCO COM 100 FOLHAS",
        "PAPEL SULFITE COM CERTIFICADO AMBIENTAL, BRANCO, A4 - 75 G/M2 - 210 X 297 MM",
        "PAPEL SULFITE RECICLADO A4 - 75G/M2 - 210 X 297 MM",
        "PAPEL SULFITE COM CERTIFICADO AMBIENTAL, BRANCO, A3 - 75 G/M2 - 297 X 420 MM",
        "PASTA PARA PRONTUARIO - ROSA CLARO",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - VERDE",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - VERMELHO",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - VERDE",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - VERMELHO",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - VERMELHO",
        "PORTA FITA ADESIVA - PEQUENO",
        "PORTA TUDO (LAPIS, CLIPS E PAPEL)",
        "REABASTECEDOR PARA PINCEL ATOMICO - PRETO",
        "REABASTECEDOR PARA PINCEL ATOMICO - VERMELHO",
        "REGUA PLASTICA - 30 CM",
        "REGUA PLASTICA - 40 CM",
        "TESOURA DE ACO INOX - USO GERAL (10 A 15 CM) - MEDIA",
        "TESOURA DE ACO INOX - USO GERAL (16 A 22 CM) - GRANDE",
        "TINTA PARA CARIMBO - AZUL - TUBO DE 40 A 50 ML",
        "TINTA PARA CARIMBO - PRETA - TUBO DE 40 A 50 ML",
        "TINTA PARA CARIMBO - VERMELHA - TUBO DE 40 A 50 ML",
        "PAPEL TOALHA, EM BOBINA, FOLHA SIMPLES - 20 CM X 200 M",
        "PAPEL TOALHA, INTERFOLHA 2 DOBRAS (1 VINCO) - 220 A 230 MM X 220 A 230 MM - PACOTE COM 4 X 250 FOLHAS",
        "PAPEL TOALHA, PICOTADO - FOLHA DUPLA - PACOTE COM 2 UNIDADES",
        "PAPEL TOALHA, EM BOBINA - ROLO COM 50 METROS",
        "PAPEL TOALHA, INTERFOLHA 2 DOBRAS (1 VINCO) - 220 A 230 MM X 260 A 270 MM - PACOTE COM 4 X 250",
        "PAPEL TOALHA, INTERFOLHA 2 DOBRAS - 230 X 210 MM - PACOTE COM 1000 FOLHAS",
        "PAPEL TOALHA, EM BOBINA - ROLO COM 100 METROS",
        "PAPEL TOALHA, INTERFOLHA 3 DOBRAS, 230 X 270 MM - 1000 FOLHAS",
        "PAPEL TOALHA, FOLHA DUPLA, 20 X 22 CM - ROLO COM 60 FOLHAS",
        "PAPEL HIGIENICO, FOLHA DUPLA, 100 MM X 30 M - SELO FSC",
        "PAPEL HIGIENICO - ROLO COM 40 METROS",
        "PAPEL HIGIENICO - ROLO COM 600 METROS",
        "PAPEL HIGIENICO - ROLO COM 300 METROS",
        "PAPEL HIGIENICO - ROLO COM 30 METROS",
        "PAPEL HIGIENICO, FOLHA SIMPLES, ROLO 300 METROS - PACOTE COM 8 UNIDADES",
        "AGUA SANITARIA ALVEJANTE E DESINFETANTE - FRASCO COM 1 LITRO",
        "ALCOOL ANTISSEPTICO 70%, EM GEL - 5 LITROS",
        "ALCOOL ETILICO 46% - FRASCO COM 1 LITRO",
        "ALCOOL ETILICO 70% (P/P) SOLUCAO ALMOTOLIA 100 ML",
        "ALCOOL ETILICO HIDRATADO 70 INPM - 1 LITRO",
        "ALCOOL ETILICO HIDRATADO 70 INPM, EM GEL - 440 GRAMAS",
        "ALCOOL GEL 70% - FRASCO COM 500 ML",
        "ALCOOL LIQUIDO 70 % - 1 LITRO",
        "DESENGRIPANTE DE USO GERAL - ANTIFERRUGINOSO E LUBRIFICANTE AEROSOL - DE 300 ML",
        "DETERGENTE EM PO - SACO COM 1 QUILO",
        "DETERGENTE EM PO - BIODEGRADAVEL - SACO COM 5 QUILOS",
        "DETERGENTE LIQUIDO - BIODEGRADAVEL - FRASCO COM 500 ML",
        "ESPONJA DE ESPUMA - DUPLA FACE",
        "ESPONJA DE LA DE ACO - PACOTE COM 08 UNIDADES",
        "ESPONJA FIBRACO - DUPLA FACE",
        "LAVATINA DE NYLON PARA VASO SANITARIO VASSOURINHA",
        "LIMPADOR GERAL DE MULTIPLO USO LIMPEZA INSTANTANEA - FRASCO COM 500 ML",
        "PA PARA LIXO COM CABO DE MADEIRA LONGO",
        "PANO DE ALGODAO PARA COPA - 40 X 60 CM",
        "PANO DE ALGODAO PARA COPA - 45 X 75 CM",
        "PANO DE FLANELA - 27 X 37 CM",
        "PANO DE FLANELA - 28 X 38 CM",
        "PANO DE FLANELA - 30 X 40 CM",
        "PANO DE FLANELA - 30 X 50 CM",
        "PANO DE FLANELA - 30 X 60 CM",
        "PANO DE FLANELA - 38 X 58 CM",
        "PANO DE FLANELA - 60 X 40 CM",
        "PANO PARA CHAO - TIPO SACO",
        "RECIPIENTE PARA MATERIAL PERFURO CORTANTE - 7 LITROS",
        "RODO ENXUGADOR - 30 CM",
        "RODO ENXUGADOR - 40 CM",
        "RODO ENXUGADOR - 60 CM",
        "SABAO COMUM EM PEDRA - PEDACO DE 200 GRAMAS",
        "SABAO DE COCO - PEDACO DE 200 GRAMAS",
        "SABAO EM PO",
        "SACO PLASTICO PARA LIXO - 100 LITROS (20 KG) - 75 X 105 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 100 LITROS (20 KG) - 75 X 105 CM - VERMELHO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 20 LITROS",
        "SACO PLASTICO PARA LIXO - 30 LITROS (6 KG) - 59 X 62 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 40 LITROS",
        "SACO PLASTICO PARA LIXO - 50 LITROS (10 KG) - 63 X 80 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 60 LITROS",
        "SACO PLASTICO PARA LIXO VERDE - CAPACIDADE 60 LITROS",
        "VASSOURA DE PELO - 30 CM",
        "VASSOURA DE PELO - 40 CM",
        "VASSOURA DE PELO - 60 CM",
        "VASSOURA DE PIACAVA - NR.04",
        "VASSOURAO DE PIACAVA TIPO PREFEITURA - 40 CM"
]

# Estruturação dos produtos
produtos_estruturados = [extrair_informacoes(produto) for produto in produtos]

# Exibir os produtos estruturados
for produto in produtos_estruturados:
    print(produto)

import re

# Dicionário para mapear unidades a suas categorias
unidade_para_categoria = {
    r'\bgramas\b': 'Peso',
    r'\bgrama\b': 'Peso',
    r'\bquilo\b': 'Peso',
    r'\bquilos\b': 'Peso',
    r'\bml\b': 'Volume',
    r'\blitros\b': 'Volume',
    r'\blitro\b': 'Volume',
    r'\bsaches\b': 'Quantidade',
    r'\bunidades\b': 'Quantidade',
    r'\bunidade\b': 'Quantidade',
    r'\bsache\b': 'Quantidade',
    r'\benvelopes\b': 'Quantidade',
    r'\benvelope\b': 'Quantidade',
    r'\bpacotes\b': 'Quantidade',
    r'\bpacote\b': 'Quantidade',
    r'\bcaixas\b': 'Quantidade',
    r'\bun\b': 'Quantidade',
    r'\bnr\b': 'Dimensão',
    r'\bcaixa\b': 'Quantidade',
    r'\bsaquinhos\b': 'Quantidade',
    r'\bsaquinho\b':'Quantidade',
    r'\bfrasco\b': 'Quantidade',
    r'\bfrascos\b': 'Quantidade',
    r'\b(?:pacotes|caixas|unidade|sache|envelopes)\b': 'Quantidade',
    r'\b(?:kg|g|gr)\b': 'Peso',
    r'\b(?:KG|G|GR)\b': 'Peso',
    r'\b(?:x|cm|mm|m|)\b': 'Dimensão',
    r'\b(?:x|CM|MM|M|)\b': 'Dimensão',
    r'\b(?:l|ml)\b': 'Volume',
    r'\b(?:L|ML)\b': 'Volume',
    r'\bcapacidade\b': 'Volume',
    r'\d+\s*mm?\s*x\s*\d+\s*mm?(\s*x\s*\d+\s*mm?)?': 'Dimensão',
    r'\b\d+\s*x\s*\d+\s*(cm|mm|m)\b|\b\d+\s+-\s+\d+\s*(cm|mm|m)\b':'Dimensão',
    r'\bcapacidade\s+(\d+(\s*-\s*\d+)?\s*(ml|l))\b':'Volume',
    r'\b(?:kg|g|gr|gramas|quilos)\b': 'Peso',
    r'\b(?:l|ml|litros|litro|capacidade\s+(\d+(\s*-\s*\d+)?\s*(ml|l)))\b': 'Volume',
    r'\b(?:unidades|saches|envelopes|pacotes|caixas|saquinhos|frasco|frascos|un|nr)\b': 'Quantidade',
    r'\b(?:x|cm|mm|m|mm?\s*x\s*\d+\s*mm?(\s*x\s*\d+\s*mm?)?|\d+\s*x\s*\d+\s*(cm|mm|m)|\d+\s+-\s+\d+\s*(cm|mm|m))\b': 'Dimensão',
    r'\b(?:kg|g|gr|gramas|quilos)\b':'Peso',
    r'\b(?:l|ml|litros|capacidade)\b':'Volume',
    r'\b(?:unidades|saches|envelopes|pacotes|caixas|saquinhos|frascos)\b':'Quantidade',
    r'\b(?:x|cm|mm|m|nr)\b':'Dimensão',
    r'\w+\s*,\s*.+': 'Tipo',
    r'\b(?i)alto vacuo\b': 'Linha',
    r'\b(?i)tradicional\b': 'Linha',
    r'\b(?i)gourmet\b': 'Linha',
    r'\b(?i)color\b': 'Tipo',
    r'\b(?i)nr\.\s*\d+\b': 'Norma',
    r'\b(?i)biodegradável\b': 'Tipo',
    r'\b(?i)sem impressão\b':'Tipo',
    r'\b(?i)personalizado\b': 'Tipo',
    r'\b(?i)antiferruginoso\b': 'Tipo',
    r'\b(?i)\d+\s+dobras\b': 'Tipo',
    r'\b(?i)folha\s+(dupla|simples)\b': 'Tipo',
    r'\b(?i)cristal\b': 'Tipo',
    r'\b(?i)macio\b':'Tipo',
    r'\b(?i)comum\b':'Tipo',
    r'\b(?i)inox\b':'Material',
    r'\b(?i)reciclado\b': 'Material',
    r'\b(?i)seda\b': 'Material',
    r'\b(?i)algodão\b': 'Material',
    r'\b(?i)vidro\b': 'Material',
    r'\b(?i)aço\b': 'Material',
    r'\b(?i)plástico\b':'Material',
    r'\b(?i)papel\b': 'Material',
    r'\b(?i)nylon\b': 'Material',
    r'\b(?i)bambu\b': 'Material',
    r'\b(?i)madeira\b': 'Material',
    r'\b(?i)saco\b':'Tipo',
    r'\b(?i)alto vacuo|tradicional|gourmet\b': 'Linha',
    r'\b(?i)nr\.\s*\d+|biodegradável|sem impressão|personalizado|cristal|dupla|simples|comum\b': 'Tipo',
    r'\b(?i)inox|aço|reciclado|seda|algodão|vidro|plástico|papel|nylon|bambu|madeira\b': 'Material'

}

# Função para determinar a categoria baseada na unidade

def determinar_categoria(parte):

    # Verificar primeiro as categorias específicas
    for regex, categoria in unidade_para_categoria.items():
        if re.search(regex, parte, re.IGNORECASE):
            return categoria

    # Se não corresponder a nenhuma categoria específica, classificar como 'Tipo'
    return 'Tipo'



    # Função para extrair as informações de cada produto
def extrair_informacoes(produto):

    partes = re.split(r', | - ', produto)
    nome = partes[0]
    tipo = dimensao = peso = quantidade = volume = "sem registro"

    # Tratar a primeira parte após o nome do item
    if len(partes) > 1:
        primeira_parte = partes[1]
        primeira_categoria = determinar_categoria(primeira_parte)
        if primeira_categoria == 'Tipo':
            tipo = primeira_parte
        elif primeira_categoria == 'Peso':
            peso = primeira_parte
        elif primeira_categoria == 'Volume':
            volume = primeira_parte
        elif primeira_categoria == 'Quantidade':
            quantidade = primeira_parte
        elif primeira_categoria == 'Dimensão':
            dimensao = primeira_parte

    # Análise das partes restantes
    for parte in partes[2:]:
        categoria = determinar_categoria(parte)
        if categoria == 'Peso' and peso == "sem registro":
            peso = parte
        elif categoria == 'Volume' and volume == "sem registro":
            volume = parte
        elif categoria == 'Quantidade' and quantidade == "sem registro":
            quantidade = parte
        elif categoria == 'Dimensão' and dimensao == "sem registro":
            dimensao = parte
        elif categoria == 'Tipo' and tipo == "sem registro":
            tipo = parte

    return {
        "Nome do Item": nome,
        "Tipo": tipo,
        "Dimensão": dimensao,
        "Peso": peso,
        "Volume": volume,
        "Quantidade": quantidade
    }


# Lista de produtos para testar
produtos = [
        "ACUCAR CRISTAL",
        "ACUCAR REFINADO AMORFO/MICROCRISTALINO",
        "ACUCAR REFINADO GRANULADO - SACHE DE 5 GRAMAS",
        "ACUCAR REFINADO, COM 400 SACHES DE 5 GRAMAS",
        "ACUCAR CRISTAL ORGANICO",
        "CAFE TORRADO MOIDO, PACOTE COM 250 GRAMAS",
        "CAFE TORRADO E MOIDO - ALMOFADA DE 500 GRAMAS",
        "CAFE TORRADO E MOIDO - ALTO VACUO DE 500 GRAMAS - SUPERIOR",
        "CAFE TORRADO E MOIDO, TIPO GOURMET, ALTO VACUO - 500 GRAMAS",
        "CAFE TORRADO E MOIDO, TRADICIONAL - ALTO VACUO DE 500 GRAMAS",
        "FILTRO DE PAPEL PARA CAFE NR, 103 - CAIXA COM 40 UNIDADES",
        "FILTRO DE PAPEL PARA CAFE NR, 103 - 30 UNIDADES",
        "FILTRO PARA CAFE NR, 102 - CAIXA COM 30 UNIDADES",
        "FILTRO DE PAPEL PARA CAFE NR. 102 - 30 UNIDADES",
        "FILTRO DE PAPEL PARA CAFETEIRA ELETRICA, NR. 04 - 30 UNIDADES",
        "CHA DE BOLDO DO CHILE, COM 15 SACHES - 15 GRAMAS",
        "CHA DE CAMOMILA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE CAMOMILA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE CAMOMILA, COM 25 SACHES - 40 GRAMAS",
        "CHA DE CAPIM LIMAO - 1 QUILO",
        "CHA DE CAPIM CIDREIRA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 20 SACHES - 20 GRAMAS",
        "CHA DE ERVA DOCE - 1 QUILO",
        "CHA DE ERVA DOCE, COM 10 SACHES - 20 GRAMAS",
        "CHA DE ERVA DOCE, COM 10 SACHES - 9 GRAMAS",
        "CHA DE ERVA DOCE, COM 15 SACHES - 30 GRAMAS",
        "CHA DE ERVA DOCE, COM 25 SACHES - 40 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 10 SACHES - 20 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 15 SACHES - 24 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 15 SACHES - 30 GRAMAS",
        "CHA DE GENGIBRE COM ESPECIARIAS, COM 10 SACHES - 10 GRAMAS",
        "CHA DE HORTELA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE HORTELA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE HORTELA, COM 25 SACHES - 40 GRAMAS",
        "CHA DE MACA COM CANELA, COM 10 SACHES - 30 GRAMAS",
        "CHA DE MACA COM CANELA, COM 15 SACHES - 30 GRAMAS",
        "CHA DE MACA VERMELHA, COM 10 SACHES - 15 GRAMAS",
        "CHA DE MACA VERMELHA, COM 10 SACHES - 20 GRAMAS",
        "CHA DE MORANGO, COM 10 SACHES - 15 GRAMAS",
        "CHA DE PESSEGO, COM 25 SACHES - 40 GRAMAS",
        "CHA MATE - 200 GRAMAS",
        "CHA MATE - 250 GRAMAS",
        "CHA MATE NATURAL - CAIXA COM 25 SAQUINHOS",
        "CHA MATE, COM 20 SACHES - 32 GRAMAS",
        "CHA MATE, SABOR LIMAO, COM 25 SACHES - 40 GRAMAS",
        "CHA MATE, SABOR NATURAL, COM 25 SACHES - 40 GRAMAS",
        "CHA MISTO DE FRUTAS E FLORES CITRICAS, COM 15 SACHES - 15 GRAMAS",
        "CHA PRETO, COM 15 SACHES - 15 GRAMAS",
        "CHA PRETO, SABOR LIMAO - 340 ML",
        "CHA VERDE, COM 10 SACHES - 16 GRAMAS",
        "CHA VERDE, COM 15 SACHES - 24 GRAMAS",
        "ADOCANTE DIETETICO EM PO, ASPARTAME, SACHE 0,8 GRAMAS - 1000 ENVELOPES",
        "ADOCANTE EM PO (ASPARTAME) - 0,8 GRAMAS - 50 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,6 GRAMAS - 1000 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,8 GRAMAS - 1000 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,8 GRAMAS - 50 UNIDADES",
        "ADOCANTE EM SACHE - 50 UNIDADES",
        "ADOCANTE LIQUIDO - 100 ML",
        "ADOCANTE LIQUIDO (ASPARTAME) - FRASCO COM 100 ML",
        "ADOCANTE LIQUIDO (SACARINA) - FRASCO COM 100 ML",
        "ADOCANTE LIQUIDO (SUCRALOSE) - 100 ML",
        "MEXEDOR DE BAMBU PARA CAFE, COMPRIMENTO 10 CM - 1000 UNIDADES",
        "MEXEDOR DE MADEIRA PARA CAFE, TIPO PALHETA - 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO COLHER - 200 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO ESPATULA DE 9 CM - PACOTE COM 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO ESPATULA DE 9 CM - PACOTE COM 500 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 250 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 500 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 60 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 180 A 220 ML",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 45 A 60 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 200 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 180 A 220 ML - 50 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 45 A 60 ML - 55 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 70 ML - 50 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 180 ML  - 100 UNIDADES",
        "COPO PLASTICO DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 180 ML - PACOTE COM 100 UNIDADES",
        "COPO DE PLASTICO DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - PACOTE COM 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, CAPACIDADE 200 ML - PACOTE COM 25 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 100 ML - 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, CAPACIDADE 200 ML - PACOTE COM 25 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 100 ML - 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - 100 UNIDADES",
        "COPO, EM FIBRA DE COCO E POLIPROPILENO - 300 ML",
        "COPO PERSONALIZADO, EM FIBRA DE COCO - 350 ML",
        "COPO PLASTICO DESCARTAVEL PARA CAFE - CAPACIDADE 50 ML",
        "COPO PLASTICO DESCARTAVEL PARA AGUA - CAPACIDADE 150 ML",
        "COPO PLASTICO DESCARTAVEL - 200 ML",
        "COPO PLASTICO DESCARTAVEL - 60 ML",
        "COPO PLASTICO DESCARTAVEL - 80 ML",
        "COPO PLASTICO DESCARTAVEL - 180 ML",
        "GAS LIQUEFEITO DE PETROLEO - BOTIJAO COM 13 QUILOS",
        "GAS LIQUEFEITO DE PETROLEO - CILINDRO COM 45 QUILOS",
        "GAS LIQUEFEITO DE PETROLEO",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 3 - AZUL",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 3 - PRETA",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - AZUL",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - PRETA",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - VERMELHA",
        "APONTADOR PARA LAPIS",
        "APONTADOR PARA LAPIS SIMPLES COM RESERVATORIO",
        "BORRACHA BICOLOR - LAPIS/TINTA",
        "BORRACHA BRANCA PARA LAPIS",
        "BORRACHA DE PAPELARIA PARA GRAFITE, EM LATEX NATURAL, BRANCA - NR. 40",
        "BORRACHA VERDE - GRANDE",
        "CADERNO CAPA DURA 1/4 - 96 A 100 FOLHAS EM PAPEL RECICLADO",
        "CAIXA PARA ARQUIVO MORTO EM PAPELAO - 360 X 250 X 135 MM",
        "CAIXA PARA ARQUIVO MORTO EM PAPELAO - 360 X 250 X 140 MM",
        "CALCULADORA ELETRONICA DE MESA COM 12 DIGITOS",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - AZUL",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - PRETA",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - VERMELHA",
        "CANETA ESFEROGRAFICA TRACO 1 MM - AZUL",
        "CANETA ESFEROGRAFICA TRACO 1 MM - PRETA",
        "CANETA ESFEROGRAFICA TRACO 1 MM - VERMELHA",
        "CANETA MARCA TEXTO COR - AMARELA",
        "CANETA MARCA COR - LARANJA",
        "CANETA MARCA - TEXTO - ROSA",
        "CANETA MARCA - TEXTO - VERDE",
        "CANETA PARA RETROPROJETOR - AZUL",
        "CANETA PARA RETROPROJETOR - VERMELHA",
        "CANETA PARA RETROPROJETOR PRETA - CAIXA 12 UNIDADES",
        "COLA EM BASTAO - PEQUENA, LAVAVEL - TUBO COM APROXIMADAMENTE 8 A 10 GRAMAS",
        "COLA EM BASTAO, A BASE DE AGUA, ATOXICA - 21 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 110 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 225 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 40 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 90 GRAMAS",
        "COLA LIQUIDA TRANSPARENTE, LAVAVEL - TUBO COM 40 GRAMAS",
        "CORRETIVO EM FITA - 5 MM X 6 M",
        "CORRETIVO EM FITA 4,2 MM X 8,5 M",
        "CORRETIVO EM FITA DE 5 MM - ROLO COM 5 M",
        "CORRETIVO LIQUIDO, A BASE DE AGUA - FRASCO DE 16 A 20 ML",
        "CORRETIVO LIQUIDO, BRANCO - FRASCO COM 18 ML",
        "ENVELOPE SEM IMPRESSAO 75G/M2 - 114 X 229 MM - PAPEL RECICLADO",
        "LAPIS BORRACHA",
        "LAPIS GRAFITE - 2 MM",
        "LAPIS PRETO NR,2 - MADEIRA DE MANEJO SUSTENTAVEL",
        "LAPIS PRETO NR.2",
        "LAPIS PRETO NR.2 - MADEIRA DE MANEJO SUSTENTAVEL",
        "LAPISEIRA, CORPO EM PLASTICO RECICLADO, COM CLIPE, PONTA E ACIONADOR DE METAL/BORRACHA - 0,7 MM",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - AZUL",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - PRETO",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - VERDE",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - VERMELHO",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 38 X 50 MM - BLOCO COM 100 FOLHAS",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 76 X 102 MM - BLOCO COM 100 FOLHAS",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 76 X 76 MM - BLOCO COM 100 FOLHAS",
        "PAPEL SULFITE COM CERTIFICADO AMBIENTAL, BRANCO, A4 - 75 G/M2 - 210 X 297 MM",
        "PAPEL SULFITE RECICLADO A4 - 75G/M2 - 210 X 297 MM",
        "PAPEL SULFITE COM CERTIFICADO AMBIENTAL, BRANCO, A3 - 75 G/M2 - 297 X 420 MM",
        "PASTA PARA PRONTUARIO - ROSA CLARO",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - VERDE",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - VERMELHO",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - VERDE",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - VERMELHO",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - VERMELHO",
        "PORTA FITA ADESIVA - PEQUENO",
        "PORTA TUDO (LAPIS, CLIPS E PAPEL)",
        "REABASTECEDOR PARA PINCEL ATOMICO - PRETO",
        "REABASTECEDOR PARA PINCEL ATOMICO - VERMELHO",
        "REGUA PLASTICA - 30 CM",
        "REGUA PLASTICA - 40 CM",
        "TESOURA DE ACO INOX - USO GERAL (10 A 15 CM) - MEDIA",
        "TESOURA DE ACO INOX - USO GERAL (16 A 22 CM) - GRANDE",
        "TINTA PARA CARIMBO - AZUL - TUBO DE 40 A 50 ML",
        "TINTA PARA CARIMBO - PRETA - TUBO DE 40 A 50 ML",
        "TINTA PARA CARIMBO - VERMELHA - TUBO DE 40 A 50 ML",
        "PAPEL TOALHA EM BOBINA, FOLHA SIMPLES - 20 CM X 200 M",
        "PAPEL TOALHA INTERFOLHA 2 DOBRAS (1 VINCO) - 220 A 230 MM X 220 A 230 MM - PACOTE COM 4 X 250 FOLHAS",
        "PAPEL TOALHA PICOTADO - FOLHA DUPLA - PACOTE COM 2 UNIDADES",
        "PAPEL TOALHA EM BOBINA - ROLO COM 50 METROS",
        "PAPEL TOALHA INTERFOLHA 2 DOBRAS (1 VINCO) - 220 A 230 MM X 260 A 270 MM - PACOTE COM 4 X 250",
        "PAPEL TOALHA INTERFOLHA 2 DOBRAS - 230 X 210 MM - PACOTE COM 1000 FOLHAS",
        "PAPEL TOALHA EM BOBINA - ROLO COM 100 METROS",
        "PAPEL TOALHA INTERFOLHA 3 DOBRAS, 230 X 270 MM - 1000 FOLHAS",
        "PAPEL TOALHA, FOLHA DUPLA, 20 X 22 CM - ROLO COM 60 FOLHAS",
        "PAPEL HIGIENICO, FOLHA DUPLA, 100 MM X 30 M - SELO FSC",
        "PAPEL HIGIENICO - ROLO COM 40 METROS",
        "PAPEL HIGIENICO - ROLO COM 600 METROS",
        "PAPEL HIGIENICO - ROLO COM 300 METROS",
        "PAPEL HIGIENICO - ROLO COM 30 METROS",
        "PAPEL HIGIENICO, FOLHA SIMPLES, ROLO 300 METROS - PACOTE COM 8 UNIDADES",
        "AGUA SANITARIA ALVEJANTE E DESINFETANTE - FRASCO COM 1 LITRO",
        "ALCOOL ANTISSEPTICO 70%, EM GEL - 5 LITROS",
        "ALCOOL ETILICO 46% - FRASCO COM 1 LITRO",
        "ALCOOL ETILICO 70% (P/P) SOLUCAO ALMOTOLIA 100 ML",
        "ALCOOL ETILICO HIDRATADO 70 INPM - 1 LITRO",
        "ALCOOL ETILICO HIDRATADO 70 INPM, EM GEL - 440 GRAMAS",
        "ALCOOL GEL 70% - FRASCO COM 500 ML",
        "ALCOOL LIQUIDO 70 % - 1 LITRO",
        "DESENGRIPANTE DE USO GERAL - ANTIFERRUGINOSO E LUBRIFICANTE AEROSOL DE 300 ML",
        "DETERGENTE EM PO - SACO COM 1 QUILO",
        "DETERGENTE EM PO BIODEGRADAVEL - SACO COM 5 QUILOS",
        "DETERGENTE LIQUIDO BIODEGRADAVEL - FRASCO COM 500 ML",
        "ESPONJA DE ESPUMA - DUPLA FACE",
        "ESPONJA DE LA DE ACO - PACOTE COM 08 UNIDADES",
        "ESPONJA FIBRACO DUPLA FACE",
        "LAVATINA DE NYLON PARA VASO SANITARIO - VASSOURINHA",
        "LIMPADOR GERAL DE MULTIPLO USO - LIMPEZA INSTANTANEA - FRASCO COM 500 ML",
        "PA PARA LIXO COM CABO DE MADEIRA LONGO",
        "PANO DE ALGODAO PARA COPA - 40 X 60 CM",
        "PANO DE ALGODAO PARA COPA - 45 X 75 CM",
        "PANO DE FLANELA - 27 X 37 CM",
        "PANO DE FLANELA - 28 X 38 CM",
        "PANO DE FLANELA - 30 X 40 CM",
        "PANO DE FLANELA - 30 X 50 CM",
        "PANO DE FLANELA - 30 X 60 CM",
        "PANO DE FLANELA - 38 X 58 CM",
        "PANO DE FLANELA - 60 X 40 CM",
        "PANO PARA CHAO - TIPO SACO",
        "RECIPIENTE PARA MATERIAL PERFURO CORTANTE - 7 LITROS",
        "RODO ENXUGADOR - 30 CM",
        "RODO ENXUGADOR - 40 CM",
        "RODO ENXUGADOR - 60 CM",
        "SABAO COMUM EM PEDRA - PEDACO DE 200 GRAMAS",
        "SABAO DE COCO - PEDACO DE 200 GRAMAS",
        "SABAO EM PO",
        "SACO PLASTICO PARA LIXO - 100 LITROS (20 KG) - 75 X 105 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 100 LITROS (20 KG) - 75 X 105 CM - VERMELHO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 20 LITROS",
        "SACO PLASTICO PARA LIXO - 30 LITROS (6 KG) - 59 X 62 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 40 LITROS",
        "SACO PLASTICO PARA LIXO - 50 LITROS (10 KG) - 63 X 80 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 60 LITROS",
        "SACO PLASTICO PARA LIXO - VERDE - CAPACIDADE 60 LITROS",
        "VASSOURA DE PELO - 30 CM",
        "VASSOURA DE PELO - 40 CM",
        "VASSOURA DE PELO - 60 CM",
        "VASSOURA DE PIACAVA - NR.04",
        "VASSOURAO DE PIACAVA TIPO PREFEITURA - 40 CM"

]

# Estruturação dos produtos
produtos_estruturados = [extrair_informacoes(produto) for produto in produtos]

# Exibir os produtos estruturados
for produto in produtos_estruturados:
    print(f"Nome do Item: {produto['Nome do Item']}")
    if produto['Tipo'] != 'sem registro':
        print(f"Tipo: {produto['Tipo']}")
    if produto['Dimensão'] != 'sem registro':
        print(f"Dimensão: {produto['Dimensão']}")
    if produto['Peso'] != 'sem registro':
        print(f"Peso: {produto['Peso']}")
    if produto['Quantidade'] != 'sem registro':
        print(f"Quantidade: {produto['Quantidade']}")
    if produto['Volume'] != 'sem registro':
        print(f"Volume: {produto['Volume']}")
    print("\n---\n")

produtos_estruturados

import re

# Dicionário para mapear unidades e expressões regulares a suas categorias
unidades_para_categoria = {
    r'\bgramas\b': 'Peso',
    r'\bgrama\b': 'Peso',
    r'\bquilo\b': 'Peso',
    r'\bquilos\b': 'Peso',
    r'\bml\b': 'Volume',
    r'\blitros\b': 'Volume',
    r'\blitro\b': 'Volume',
    r'\bsaches\b': 'Quantidade',
    r'\bunidades\b': 'Quantidade',
    r'\bunidade\b': 'Quantidade',
    r'\bsache\b': 'Quantidade',
    r'\benvelopes\b': 'Quantidade',
    r'\benvelope\b': 'Quantidade',
    r'\bpacotes\b': 'Quantidade',
    r'\bpacote\b': 'Quantidade',
    r'\bcaixas\b': 'Quantidade',
    r'\bun\b': 'Quantidade',
    r'\bnr\b': 'Dimensão',
    r'\bcaixa\b': 'Quantidade',
    r'\bsaquinhos\b': 'Quantidade',
    r'\bsaquinho\b':'Quantidade',
    r'\bfrasco\b': 'Quantidade',
    r'\bfrascos\b': 'Quantidade',
    r'\b(?:pacotes|caixas|unidade|sache|envelopes)\b': 'Quantidade',
    r'\b(?:kg|g|gr)\b': 'Peso',
    r'\b(?:KG|G|GR)\b': 'Peso',
    r'\b(?:x|cm|mm|m|)\b': 'Dimensão',
    r'\b(?:x|CM|MM|M|)\b': 'Dimensão',
    r'\b(?:l|ml)\b': 'Volume',
    r'\b(?:L|ML)\b': 'Volume',
    r'\bcapacidade\b': 'Volume'
   # r'\d+\s*mm?\s*x\s*\d+\s*mm?(\s*x\s*\d+\s*mm?)?': 'Dimensão'

}

# Função para determinar a categoria baseada na unidade encontrada
def determinar_categoria(fragmento):
    fragmento = fragmento.lower()  # Converter para lowercase para correspondência de padrões
    for padrao, categoria in unidades_para_categoria.items():
        if re.search(padrao, fragmento, re.IGNORECASE):  # Pesquisa insensível a maiúsculas e minúsculas
            return categoria
    return 'Tipo'

# Expressão regular para identificar dimensões
#regex_dimensao = r'\b\d+\s*x\s*\d+\s*(cm|mm|m)\b|\b\d+\s+-\s+\d+\s*(cm|mm|m)\b'

# Função para extrair as informações de cada produto
def extrair_informacoes(produto):
    # Separação baseada em caracteres especiais
    partes = re.split(r', | - ', produto)
    nome = partes[0] if partes else 'sem registro'
    tipo = partes[1] if len(partes) > 1 else "sem tipo"
    # Inicializando variáveis
    dimensao = volume = peso = quantidade = 'sem registro'

    # Padrões regex para identificar dimensões e volumes
    regex_dimensao = re.compile(r'\b\d+\s*x\s*\d+\s*(cm|mm|m)\b|\b\d+\s+-\s+\d+\s*(cm|mm|m)\b')
    regex_volume = re.compile(r'\bcapacidade\s+(\d+(\s*-\s*\d+)?\s*(ml|l))\b', re.IGNORECASE)


    # Análise das partes restantes após o nome do produto
    # Análise das partes restantes após o nome do produto
    for parte in partes[2:]:
        if regex_dimensao.search(parte):
            dimensao = regex_dimensao.search(parte).group()
        elif regex_volume.search(parte):
            volume = regex_volume.search(parte).group(1)
        elif 'g' in parte or 'kg' in parte:
            peso = parte
        elif 'unidade' in parte or 'sache' in parte or 'pacote' in parte:
            quantidade = parte

    return {
        "Nome do Item": nome,
        "Tipo": tipo,
        "Dimensão": dimensao,
        "Peso": peso,
        "Volume": volume,
        "Quantidade": quantidade
    }

# Lista de produtos de exemplo (substitua pelos seus produtos)
produtos = [
        "ACUCAR CRISTAL",
        "ACUCAR REFINADO AMORFO/MICROCRISTALINO",
        "ACUCAR REFINADO GRANULADO - SACHE DE 5 GRAMAS",
        "ACUCAR REFINADO, COM 400 SACHES DE 5 GRAMAS",
        "ACUCAR CRISTAL ORGANICO",
        "CAFE TORRADO MOIDO, PACOTE COM 250 GRAMAS",
        "CAFE TORRADO E MOIDO - ALMOFADA DE 500 GRAMAS",
        "CAFE TORRADO E MOIDO - ALTO VACUO DE 500 GRAMAS - SUPERIOR",
        "CAFE TORRADO E MOIDO, TIPO GOURMET, ALTO VACUO - 500 GRAMAS",
        "CAFE TORRADO E MOIDO, TRADICIONAL - ALTO VACUO DE 500 GRAMAS",
        "FILTRO DE PAPEL PARA CAFE NR, 103 - CAIXA COM 40 UNIDADES",
        "FILTRO DE PAPEL PARA CAFE NR, 103 - 30 UNIDADES",
        "FILTRO PARA CAFE NR, 102 - CAIXA COM 30 UNIDADES",
        "FILTRO DE PAPEL PARA CAFE NR. 102 - 30 UNIDADES",
        "FILTRO DE PAPEL PARA CAFETEIRA ELETRICA, NR. 04 - 30 UNIDADES",
        "CHA DE BOLDO DO CHILE, COM 15 SACHES - 15 GRAMAS",
        "CHA DE CAMOMILA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE CAMOMILA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE CAMOMILA, COM 25 SACHES - 40 GRAMAS",
        "CHA DE CAPIM LIMAO - 1 QUILO",
        "CHA DE CAPIM CIDREIRA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 20 SACHES - 20 GRAMAS",
        "CHA DE ERVA DOCE - 1 QUILO",
        "CHA DE ERVA DOCE, COM 10 SACHES - 20 GRAMAS",
        "CHA DE ERVA DOCE, COM 10 SACHES - 9 GRAMAS",
        "CHA DE ERVA DOCE, COM 15 SACHES - 30 GRAMAS",
        "CHA DE ERVA DOCE, COM 25 SACHES - 40 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 10 SACHES - 20 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 15 SACHES - 24 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 15 SACHES - 30 GRAMAS",
        "CHA DE GENGIBRE COM ESPECIARIAS, COM 10 SACHES - 10 GRAMAS",
        "CHA DE HORTELA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE HORTELA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE HORTELA, COM 25 SACHES - 40 GRAMAS",
        "CHA DE MACA COM CANELA, COM 10 SACHES - 30 GRAMAS",
        "CHA DE MACA COM CANELA, COM 15 SACHES - 30 GRAMAS",
        "CHA DE MACA VERMELHA, COM 10 SACHES - 15 GRAMAS",
        "CHA DE MACA VERMELHA, COM 10 SACHES - 20 GRAMAS",
        "CHA DE MORANGO, COM 10 SACHES - 15 GRAMAS",
        "CHA DE PESSEGO, COM 25 SACHES - 40 GRAMAS",
        "CHA MATE - 200 GRAMAS",
        "CHA MATE - 250 GRAMAS",
        "CHA MATE NATURAL - CAIXA COM 25 SAQUINHOS",
        "CHA MATE, COM 20 SACHES - 32 GRAMAS",
        "CHA MATE, SABOR LIMAO, COM 25 SACHES - 40 GRAMAS",
        "CHA MATE, SABOR NATURAL, COM 25 SACHES - 40 GRAMAS",
        "CHA MISTO DE FRUTAS E FLORES CITRICAS, COM 15 SACHES - 15 GRAMAS",
        "CHA PRETO, COM 15 SACHES - 15 GRAMAS",
        "CHA PRETO, SABOR LIMAO - 340 ML",
        "CHA VERDE, COM 10 SACHES - 16 GRAMAS",
        "CHA VERDE, COM 15 SACHES - 24 GRAMAS",
        "ADOCANTE DIETETICO EM PO, ASPARTAME, SACHE 0,8 GRAMAS - 1000 ENVELOPES",
        "ADOCANTE EM PO (ASPARTAME) - 0,8 GRAMAS - 50 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,6 GRAMAS - 1000 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,8 GRAMAS - 1000 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,8 GRAMAS - 50 UNIDADES",
        "ADOCANTE EM SACHE - 50 UNIDADES",
        "ADOCANTE LIQUIDO - 100 ML",
        "ADOCANTE LIQUIDO (ASPARTAME) - FRASCO COM 100 ML",
        "ADOCANTE LIQUIDO (SACARINA) - FRASCO COM 100 ML",
        "ADOCANTE LIQUIDO (SUCRALOSE) - 100 ML",
        "MEXEDOR DE BAMBU PARA CAFE, COMPRIMENTO 10 CM - 1000 UNIDADES",
        "MEXEDOR DE MADEIRA PARA CAFE, TIPO PALHETA - 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO COLHER - 200 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO ESPATULA DE 9 CM - PACOTE COM 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO ESPATULA DE 9 CM - PACOTE COM 500 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 250 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 500 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 60 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 180 A 220 ML",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 45 A 60 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 200 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 180 A 220 ML - 50 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 45 A 60 ML - 55 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 70 ML - 50 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 180 ML  - 100 UNIDADES",
        "COPO PLASTICO DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 180 ML - PACOTE COM 100 UNIDADES",
        "COPO DE PLASTICO DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - PACOTE COM 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, CAPACIDADE 200 ML - PACOTE COM 25 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 100 ML - 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, CAPACIDADE 200 ML - PACOTE COM 25 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 100 ML - 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - 100 UNIDADES",
        "COPO, EM FIBRA DE COCO E POLIPROPILENO - 300 ML",
        "COPO PERSONALIZADO, EM FIBRA DE COCO - 350 ML",
        "COPO PLASTICO DESCARTAVEL PARA CAFE - CAPACIDADE 50 ML",
        "COPO PLASTICO DESCARTAVEL PARA AGUA - CAPACIDADE 150 ML",
        "COPO PLASTICO DESCARTAVEL - 200 ML",
        "COPO PLASTICO DESCARTAVEL - 60 ML",
        "COPO PLASTICO DESCARTAVEL - 80 ML",
        "COPO PLASTICO DESCARTAVEL - 180 ML",
        "GAS LIQUEFEITO DE PETROLEO - BOTIJAO COM 13 QUILOS",
        "GAS LIQUEFEITO DE PETROLEO - CILINDRO COM 45 QUILOS",
        "GAS LIQUEFEITO DE PETROLEO",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 3 - AZUL",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 3 - PRETA",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - AZUL",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - PRETA",
        "ALMOFADA ENTINTADA PARA CARIMBO NR. 4 - VERMELHA",
        "APONTADOR PARA LAPIS",
        "APONTADOR PARA LAPIS SIMPLES COM RESERVATORIO",
        "BORRACHA BICOLOR - LAPIS/TINTA",
        "BORRACHA BRANCA PARA LAPIS",
        "BORRACHA DE PAPELARIA PARA GRAFITE, EM LATEX NATURAL, BRANCA - NR. 40",
        "BORRACHA VERDE - GRANDE",
        "CADERNO CAPA DURA 1/4 - 96 A 100 FOLHAS EM PAPEL RECICLADO",
        "CAIXA PARA ARQUIVO MORTO EM PAPELAO - 360 X 250 X 135 MM",
        "CAIXA PARA ARQUIVO MORTO EM PAPELAO - 360 X 250 X 140 MM",
        "CALCULADORA ELETRONICA DE MESA COM 12 DIGITOS",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - AZUL",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - PRETA",
        "CANETA ESFEROGRAFICA TRACO 0,7 MM - VERMELHA",
        "CANETA ESFEROGRAFICA TRACO 1 MM - AZUL",
        "CANETA ESFEROGRAFICA TRACO 1 MM - PRETA",
        "CANETA ESFEROGRAFICA TRACO 1 MM - VERMELHA",
        "CANETA MARCA TEXTO COR - AMARELA",
        "CANETA MARCA COR - LARANJA",
        "CANETA MARCA - TEXTO - ROSA",
        "CANETA MARCA - TEXTO - VERDE",
        "CANETA PARA RETROPROJETOR - AZUL",
        "CANETA PARA RETROPROJETOR - VERMELHA",
        "CANETA PARA RETROPROJETOR PRETA - CAIXA 12 UNIDADES",
        "COLA EM BASTAO - PEQUENA, LAVAVEL - TUBO COM APROXIMADAMENTE 8 A 10 GRAMAS",
        "COLA EM BASTAO, A BASE DE AGUA, ATOXICA - 21 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 110 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 225 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 40 GRAMAS",
        "COLA LIQUIDA BRANCA, LAVAVEL - TUBO COM 90 GRAMAS",
        "COLA LIQUIDA TRANSPARENTE, LAVAVEL - TUBO COM 40 GRAMAS",
        "CORRETIVO EM FITA - 5 MM X 6 M",
        "CORRETIVO EM FITA 4,2 MM X 8,5 M",
        "CORRETIVO EM FITA DE 5 MM - ROLO COM 5 M",
        "CORRETIVO LIQUIDO, A BASE DE AGUA - FRASCO DE 16 A 20 ML",
        "CORRETIVO LIQUIDO, BRANCO - FRASCO COM 18 ML",
        "ENVELOPE SEM IMPRESSAO 75G/M2 - 114 X 229 MM - PAPEL RECICLADO",
        "LAPIS BORRACHA",
        "LAPIS GRAFITE - 2 MM",
        "LAPIS PRETO NR,2 - MADEIRA DE MANEJO SUSTENTAVEL",
        "LAPIS PRETO NR.2",
        "LAPIS PRETO NR.2 - MADEIRA DE MANEJO SUSTENTAVEL",
        "LAPISEIRA, CORPO EM PLASTICO RECICLADO, COM CLIPE, PONTA E ACIONADOR DE METAL/BORRACHA - 0,7 MM",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - AZUL",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - PRETO",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - VERDE",
        "MARCADOR PARA QUADRO BRANCO, RECARREGAVEL - VERMELHO",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 38 X 50 MM - BLOCO COM 100 FOLHAS",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 76 X 102 MM - BLOCO COM 100 FOLHAS",
        "PAPEL LEMBRETE ADESIVO, EM PAPEL RECICLADO, 76 X 76 MM - BLOCO COM 100 FOLHAS",
        "PAPEL SULFITE COM CERTIFICADO AMBIENTAL, BRANCO, A4 - 75 G/M2 - 210 X 297 MM",
        "PAPEL SULFITE RECICLADO A4 - 75G/M2 - 210 X 297 MM",
        "PAPEL SULFITE COM CERTIFICADO AMBIENTAL, BRANCO, A3 - 75 G/M2 - 297 X 420 MM",
        "PASTA PARA PRONTUARIO - ROSA CLARO",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - VERDE",
        "PINCEL ATOMICO PONTA FINA - TRACO 2 MM, RECARREGAVEL - VERMELHO",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - VERDE",
        "PINCEL ATOMICO PONTA GROSSA - TRACO 8 MM, RECARREGAVEL - VERMELHO",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - AZUL",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - PRETO",
        "PINCEL ATOMICO PONTA MEDIA - TRACO 4 MM, RECARREGAVEL - VERMELHO",
        "PORTA FITA ADESIVA - PEQUENO",
        "PORTA TUDO (LAPIS, CLIPS E PAPEL)",
        "REABASTECEDOR PARA PINCEL ATOMICO - PRETO",
        "REABASTECEDOR PARA PINCEL ATOMICO - VERMELHO",
        "REGUA PLASTICA - 30 CM",
        "REGUA PLASTICA - 40 CM",
        "TESOURA DE ACO INOX - USO GERAL (10 A 15 CM) - MEDIA",
        "TESOURA DE ACO INOX - USO GERAL (16 A 22 CM) - GRANDE",
        "TINTA PARA CARIMBO - AZUL - TUBO DE 40 A 50 ML",
        "TINTA PARA CARIMBO - PRETA - TUBO DE 40 A 50 ML",
        "TINTA PARA CARIMBO - VERMELHA - TUBO DE 40 A 50 ML",
        "PAPEL TOALHA EM BOBINA, FOLHA SIMPLES - 20 CM X 200 M",
        "PAPEL TOALHA INTERFOLHA 2 DOBRAS (1 VINCO) - 220 A 230 MM X 220 A 230 MM - PACOTE COM 4 X 250 FOLHAS",
        "PAPEL TOALHA PICOTADO - FOLHA DUPLA - PACOTE COM 2 UNIDADES",
        "PAPEL TOALHA EM BOBINA - ROLO COM 50 METROS",
        "PAPEL TOALHA INTERFOLHA 2 DOBRAS (1 VINCO) - 220 A 230 MM X 260 A 270 MM - PACOTE COM 4 X 250",
        "PAPEL TOALHA INTERFOLHA 2 DOBRAS - 230 X 210 MM - PACOTE COM 1000 FOLHAS",
        "PAPEL TOALHA EM BOBINA - ROLO COM 100 METROS",
        "PAPEL TOALHA INTERFOLHA 3 DOBRAS, 230 X 270 MM - 1000 FOLHAS",
        "PAPEL TOALHA, FOLHA DUPLA, 20 X 22 CM - ROLO COM 60 FOLHAS",
        "PAPEL HIGIENICO, FOLHA DUPLA, 100 MM X 30 M - SELO FSC",
        "PAPEL HIGIENICO - ROLO COM 40 METROS",
        "PAPEL HIGIENICO - ROLO COM 600 METROS",
        "PAPEL HIGIENICO - ROLO COM 300 METROS",
        "PAPEL HIGIENICO - ROLO COM 30 METROS",
        "PAPEL HIGIENICO, FOLHA SIMPLES, ROLO 300 METROS - PACOTE COM 8 UNIDADES",
        "AGUA SANITARIA ALVEJANTE E DESINFETANTE - FRASCO COM 1 LITRO",
        "ALCOOL ANTISSEPTICO 70%, EM GEL - 5 LITROS",
        "ALCOOL ETILICO 46% - FRASCO COM 1 LITRO",
        "ALCOOL ETILICO 70% (P/P) SOLUCAO ALMOTOLIA 100 ML",
        "ALCOOL ETILICO HIDRATADO 70 INPM - 1 LITRO",
        "ALCOOL ETILICO HIDRATADO 70 INPM, EM GEL - 440 GRAMAS",
        "ALCOOL GEL 70% - FRASCO COM 500 ML",
        "ALCOOL LIQUIDO 70 % - 1 LITRO",
        "DESENGRIPANTE DE USO GERAL - ANTIFERRUGINOSO E LUBRIFICANTE AEROSOL DE 300 ML",
        "DETERGENTE EM PO - SACO COM 1 QUILO",
        "DETERGENTE EM PO BIODEGRADAVEL - SACO COM 5 QUILOS",
        "DETERGENTE LIQUIDO BIODEGRADAVEL - FRASCO COM 500 ML",
        "ESPONJA DE ESPUMA - DUPLA FACE",
        "ESPONJA DE LA DE ACO - PACOTE COM 08 UNIDADES",
        "ESPONJA FIBRACO DUPLA FACE",
        "LAVATINA DE NYLON PARA VASO SANITARIO - VASSOURINHA",
        "LIMPADOR GERAL DE MULTIPLO USO - LIMPEZA INSTANTANEA - FRASCO COM 500 ML",
        "PA PARA LIXO COM CABO DE MADEIRA LONGO",
        "PANO DE ALGODAO PARA COPA - 40 X 60 CM",
        "PANO DE ALGODAO PARA COPA - 45 X 75 CM",
        "PANO DE FLANELA - 27 X 37 CM",
        "PANO DE FLANELA - 28 X 38 CM",
        "PANO DE FLANELA - 30 X 40 CM",
        "PANO DE FLANELA - 30 X 50 CM",
        "PANO DE FLANELA - 30 X 60 CM",
        "PANO DE FLANELA - 38 X 58 CM",
        "PANO DE FLANELA - 60 X 40 CM",
        "PANO PARA CHAO - TIPO SACO",
        "RECIPIENTE PARA MATERIAL PERFURO CORTANTE - 7 LITROS",
        "RODO ENXUGADOR - 30 CM",
        "RODO ENXUGADOR - 40 CM",
        "RODO ENXUGADOR - 60 CM",
        "SABAO COMUM EM PEDRA - PEDACO DE 200 GRAMAS",
        "SABAO DE COCO - PEDACO DE 200 GRAMAS",
        "SABAO EM PO",
        "SACO PLASTICO PARA LIXO - 100 LITROS (20 KG) - 75 X 105 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 100 LITROS (20 KG) - 75 X 105 CM - VERMELHO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 20 LITROS",
        "SACO PLASTICO PARA LIXO - 30 LITROS (6 KG) - 59 X 62 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 40 LITROS",
        "SACO PLASTICO PARA LIXO - 50 LITROS (10 KG) - 63 X 80 CM - PRETO - NBR 9191",
        "SACO PLASTICO PARA LIXO - 60 LITROS",
        "SACO PLASTICO PARA LIXO - VERDE - CAPACIDADE 60 LITROS",
        "VASSOURA DE PELO - 30 CM",
        "VASSOURA DE PELO - 40 CM",
        "VASSOURA DE PELO - 60 CM",
        "VASSOURA DE PIACAVA - NR.04",
        "VASSOURAO DE PIACAVA TIPO PREFEITURA - 40 CM"

]

# Estruturação dos produtos
produtos_estruturados = [extrair_informacoes(produto) for produto in produtos]

# Exibir os produtos estruturados
# Exibir os produtos estruturados
for produto in produtos_estruturados:
    print(f"Nome do Item: {produto['Nome do Item']}")
    if produto['Tipo'] != 'sem registro':
        print(f"Tipo: {produto['Tipo']}")
    if produto['Dimensão'] != 'sem registro':
        print(f"Dimensão: {produto['Dimensão']}")
    if produto['Peso'] != 'sem registro':
        print(f"Peso: {produto['Peso']}")
    if produto['Volume'] != 'sem registro':
        print(f"Volume: {produto['Volume']}")
    if produto['Quantidade'] != 'sem registro':
        print(f"Quantidade: {produto['Quantidade']}")
    print()

produtos_estruturados

import re



cores = ["abóbora", "açafrão", "amarelo", "âmbar", "ameixa", "amêndoa", "ametista", "anil", "azul", "bege", "bordô", "branco",
         "bronze", "cáqui", "caramelo", "carmesim", "carmim", "castanho", "cereja", "chocolate", "ciano", "cinza", "cinzento",
         "cobre", "coral", "creme", "damasco", "dourado", "escarlate", "esmeralda", "ferrugem", "fúcsia", "gelo", "grená", "gris",
         "índigo", "jade", "jambo", "laranja", "lavanda", "lilás", "limão", "loiro", "magenta", "malva", "marfim", "marrom",
         "mostarda", "negro", "ocre", "oliva", "ouro", "pêssego", "prata", "preto", "púrpura", "rosa", "roxo", "rubro", "salmão",
         "sépia", "terracota", "tijolo", "turquesa", "uva", "verde", "vermelho", "vinho", "violeta"]


def extrai_apresentacao(produto):
    palavras = produto.split()
    if palavras:
        return palavras[0]
    return ""



def extrai_tipo(produto):
    palavras = produto.split()
    tipo = ' '.join(palavras[1:])
    tipo = re.sub(r'(\d+(\.\d+)?\s*(cm|mm|m|ml|l|g|kg|x|un|pct|cx|mg|lt|m2|m3|km|hz|w|kw|v|amp|in|ft|lb|oz|nr))', '', tipo).strip()
    tipo = re.sub(r'\b(com|de)\b.*', '', tipo).strip()  # Remove partes após 'com' ou 'de' que contêm números
    return tipo

def extrai_dimensao(produto):
    dimensao_pattern = re.compile(r'(\d+(\.\d+)?\s*(cm|mm|m|ml|l|g|kg|x|un|pct|cx|mg|lt|m2|m3|km|hz|w|kw|v|amp|in|ft|lb|oz|nr))')
    matches = dimensao_pattern.findall(produto)
    if matches:
        return ' '.join([m[0] for m in matches])

    # Extrai dimensões que aparecem após 'com' ou 'de'
    pos_com_de = re.search(r'\b(com|de)\b(.*)', produto)
    if pos_com_de and re.search(r'\d+', pos_com_de.group(2)):
        return pos_com_de.group(2).strip()

    return "sem registro"

def extrai_peso(produto):
    # Padrões para gramas (g), quilogramas (kg) e miligramas (mg)
    peso_pattern = re.compile(r'(\d+(\.\d+)?\s*(g|kg|mg))')
    match = peso_pattern.search(produto)
    if match:
        return match.group(1)  # Retorna o número junto com a unidade
    return "sem registro"


def extrai_embalagem(produto):
    # Detecção de cores
    cores_encontradas = [cor for cor in cores if cor in produto.lower()]

    # Detecção de tamanhos e outros padrões
    embalagem_pattern = re.compile(r'\b(sache|saches|frasco|pequeno|pequena|medio|media|grande|fino|fina|grosso|grossa|claro|escuro|tubo)\b')
    tamanho_encontrado = embalagem_pattern.findall(produto)

    embalagem = cores_encontradas + tamanho_encontrado
    return ', '.join(embalagem) if embalagem else "sem registro"







def expand_abbreviations(text):
    replacements = {
        ' ml ': ' mililitro ',
        ' cm ': ' centimetro ',
        ' mm ': ' milimetro ',
        ' m ': ' metro ',
        ' kg ': ' quilograma ',
        ' g ': ' grama ',
        ' l ': ' litro ',
        ' un ': ' unidade ',
        ' pct ': ' pacote ',
        ' cx ': ' caixa ',
        ' und ': ' unidade ',
        ' pc ': ' peça ',
        ' pcs ': ' peças ',
        ' gr ': ' grama ',
        ' mg ': ' miligrama ',
        ' lt ': ' litro ',
        ' m2 ': ' metro quadrado ',
        ' m3 ': ' metro cúbico ',
        ' km ': ' quilometro ',
        ' hz ': ' hertz ',
        ' w ': ' watt ',
        ' kw ': ' kilowatt ',
        ' v ': ' volt ',
        ' amp ': ' ampere ',
        ' in ': ' polegada ',
        ' ft ': ' pé ',
        ' lb ': ' libra ',
        ' oz ': ' onça '
    }

    # Aplicando as substituições
    for key, val in replacements.items():
        text = text.replace(key, val)
    return text

def extrai_dimensao(produto):
    produto_expandido = expand_abbreviations(produto)
    dimensao_pattern = re.compile(r'(\d+(\.\d+)?\s*(mililitro|mililitros|centimetro|centimetros|milimetro|milimetros|metro|metros|unidade|unidades|pacote|pacotes|caixa|caixas|peça|peças|miligrama|metro quadrado|metro cúbico|quilometro|hertz|watt|kilowatt|volt|ampere|polegada|pé|libra|onça))')
    matches = dimensao_pattern.findall(produto_expandido)
    if matches:
        return ' '.join([m[0] for m in matches])

    return "sem registro"

def extrai_quantidade(produto):
    quantidade_pattern = re.compile(r'\b(pacote|pacotes|pacotes com)\b\s*(\d+(\.\d+)?\s*(un|unidades|g|gramas|ml|mililitros))')
    match = quantidade_pattern.search(produto)
    if match:
        return match.group(2)  # Retorna apenas a parte numérica e a unidade
    return "sem registro"




# Dados
produtos = [

        "ACUCAR CRISTAL",
        "ACUCAR REFINADO AMORFO/MICROCRISTALINO",
        "ACUCAR REFINADO GRANULADO - SACHE DE 5 GRAMAS",
        "ACUCAR REFINADO, COM 400 SACHES DE 5 GRAMAS",
        "ACUCAR CRISTAL ORGANICO",
        "CAFE TORRADO MOIDO, PACOTE COM 250 GRAMAS",
        "CAFE TORRADO E MOIDO - ALMOFADA DE 500 GRAMAS",
        "CAFE TORRADO E MOIDO - ALTO VACUO DE 500 GRAMAS - SUPERIOR",
        "CAFE TORRADO E MOIDO, TIPO GOURMET, ALTO VACUO - 500 GRAMAS",
        "CAFE TORRADO E MOIDO, TRADICIONAL - ALTO VACUO DE 500 GRAMAS",
        "FILTRO DE PAPEL PARA CAFE NR, 103 - CAIXA COM 40 UNIDADES",
        "FILTRO DE PAPEL PARA CAFE NR, 103 - 30 UNIDADES",
        "FILTRO PARA CAFE NR, 102 - CAIXA COM 30 UNIDADES",
        "FILTRO DE PAPEL PARA CAFE NR. 102 - 30 UNIDADES",
        "FILTRO DE PAPEL PARA CAFETEIRA ELETRICA, NR. 04 - 30 UNIDADES",
        "CHA DE BOLDO DO CHILE, COM 15 SACHES - 15 GRAMAS",
        "CHA DE CAMOMILA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE CAMOMILA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE CAMOMILA, COM 25 SACHES - 40 GRAMAS",
        "CHA DE CAPIM LIMAO - 1 QUILO",
        "CHA DE CAPIM CIDREIRA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE ERVA CIDREIRA, COM 20 SACHES - 20 GRAMAS",
        "CHA DE ERVA DOCE - 1 QUILO",
        "CHA DE ERVA DOCE, COM 10 SACHES - 20 GRAMAS",
        "CHA DE ERVA DOCE, COM 10 SACHES - 9 GRAMAS",
        "CHA DE ERVA DOCE, COM 15 SACHES - 30 GRAMAS",
        "CHA DE ERVA DOCE, COM 25 SACHES - 40 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 10 SACHES - 20 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 15 SACHES - 24 GRAMAS",
        "CHA DE FRUTAS VERMELHAS, COM 15 SACHES - 30 GRAMAS",
        "CHA DE GENGIBRE COM ESPECIARIAS, COM 10 SACHES - 10 GRAMAS",
        "CHA DE HORTELA, COM 10 SACHES - 10 GRAMAS",
        "CHA DE HORTELA, COM 15 SACHES - 15 GRAMAS",
        "CHA DE HORTELA, COM 25 SACHES - 40 GRAMAS",
        "CHA DE MACA COM CANELA, COM 10 SACHES - 30 GRAMAS",
        "CHA DE MACA COM CANELA, COM 15 SACHES - 30 GRAMAS",
        "CHA DE MACA VERMELHA, COM 10 SACHES - 15 GRAMAS",
        "CHA DE MACA VERMELHA, COM 10 SACHES - 20 GRAMAS",
        "CHA DE MORANGO, COM 10 SACHES - 15 GRAMAS",
        "CHA DE PESSEGO, COM 25 SACHES - 40 GRAMAS",
        "CHA MATE - 200 GRAMAS",
        "CHA MATE - 250 GRAMAS",
        "CHA MATE NATURAL - CAIXA COM 25 SAQUINHOS",
        "CHA MATE, COM 20 SACHES - 32 GRAMAS",
        "CHA MATE, SABOR LIMAO, COM 25 SACHES - 40 GRAMAS",
        "CHA MATE, SABOR NATURAL, COM 25 SACHES - 40 GRAMAS",
        "CHA MISTO DE FRUTAS E FLORES CITRICAS, COM 15 SACHES - 15 GRAMAS",
        "CHA PRETO, COM 15 SACHES - 15 GRAMAS",
        "CHA PRETO, SABOR LIMAO - 340 ML",
        "CHA VERDE, COM 10 SACHES - 16 GRAMAS",
        "CHA VERDE, COM 15 SACHES - 24 GRAMAS",
        "ADOCANTE DIETETICO EM PO, ASPARTAME, SACHE 0,8 GRAMAS - 1000 ENVELOPES",
        "ADOCANTE EM PO (ASPARTAME) - 0,8 GRAMAS - 50 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,6 GRAMAS - 1000 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,8 GRAMAS - 1000 UNIDADES",
        "ADOCANTE EM PO (SUCRALOSE) - 0,8 GRAMAS - 50 UNIDADES",
        "ADOCANTE EM SACHE - 50 UNIDADES",
        "ADOCANTE LIQUIDO - 100 ML",
        "ADOCANTE LIQUIDO (ASPARTAME) - FRASCO COM 100 ML",
        "ADOCANTE LIQUIDO (SACARINA) - FRASCO COM 100 ML",
        "ADOCANTE LIQUIDO (SUCRALOSE) - 100 ML",
        "MEXEDOR DE BAMBU PARA CAFE, COMPRIMENTO 10 CM - 1000 UNIDADES",
        "MEXEDOR DE MADEIRA PARA CAFE, TIPO PALHETA - 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO COLHER - 200 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO ESPATULA DE 9 CM - PACOTE COM 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO ESPATULA DE 9 CM - PACOTE COM 500 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 100 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 250 UNIDADES",
        "MEXEDOR DE PLASTICO PARA CAFE, TIPO PALHETA DE 8,5 CM - 500 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 60 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 180 A 220 ML",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 45 A 60 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 200 ML",
        "COPO DE PAPEL DESCARTAVEL PARA AGUA - CAPACIDADE 180 A 220 ML - 50 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL PARA CAFE - CAPACIDADE 45 A 60 ML - 55 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 70 ML - 50 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 180 ML  - 100 UNIDADES",
        "COPO PLASTICO DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 180 ML - PACOTE COM 100 UNIDADES",
        "COPO DE PLASTICO DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - PACOTE COM 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, CAPACIDADE 200 ML - PACOTE COM 25 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 100 ML - 100 UNIDADES",
        "COPO DE PAPEL DESCARTAVEL, BIODEGRADAVEL, CAPACIDADE 50 ML - 100 UNIDADES"
]



def formatar_saida(apresentacao, tipo, dimensao, quantidade, embalagem, peso):
    elementos = []
    if apresentacao != "sem registro":
        elementos.append(f"Nome do material: {apresentacao}")
    if tipo != "sem registro":
        elementos.append(f"Tipo: {tipo}")
    if dimensao != "sem registro":
        elementos.append(f"Dimensão: {dimensao}")
    if quantidade != "sem registro":
        elementos.append(f"Quantidade: {quantidade}")
    if embalagem != "sem registro":
        elementos.append(f"Embalagem: {embalagem}")
    if peso != "sem registro":
        elementos.append(f"Peso: {peso}")

    return '; '.join(elementos)

for produto in produtos:
    apresentacao = extrai_apresentacao(produto)
    tipo = extrai_tipo(produto)
    dimensao = extrai_dimensao(produto)
    embalagem = extrai_embalagem(produto)
    quantidade = extrai_quantidade(produto)
    peso = extrai_peso(produto)

    saida_formatada = formatar_saida(apresentacao, tipo, dimensao, quantidade, embalagem, peso)
    print(saida_formatada)

#for produto in produtos:
#    apresentacao = extrai_apresentacao(produto)
#    tipo = extrai_tipo(produto)
#    dimensao = extrai_dimensao(produto)
#    quantidade = extrai_quantidade(produto)
#    embalagem = extrai_embalagem(produto)


#    print(f"Nome do material: {apresentacao}")
#    print(f"Tipo: {tipo}")
#    print(f"Dimensão: {dimensao}")
#    print(f"Quantidade: {quantidade}")
#    print(f"Embalagem: {embalagem}")
#    print()


# sempre que tiver as palavras: unidade, grama, quilo, bloco, folhas : crio um campo "Outras informações"
# Dimensao aparecer apenas quando tiver.

import re

TIPO_REGEX = r'\b(de|para|com|em|em)\b\s+(.+)'
DIMENSAO_REGEX = r'((?:\d+,?)+\.?\d*\s*(?:cm|mm|m|ml|l|g|kg|x|por|\d+))'
EMBALAGEM_REGEX = r'\b(pequeno|pequena|medio|media|grande|fino|fina|vermelho|preto|etc)\b'

def extrai_apresentacao(produto):
    termos_exclusao = ["de", "do", "da", "em", "para", "com"]
    termos = produto.split()
    if termos and termos[0].lower() not in termos_exclusao:
        return termos[0]
    return ""

def extrai_tipo(produto):
    match = re.search(TIPO_REGEX, produto)
    return match.group(2) if match else ""

def extrai_dimensao(produto):
    match = re.search(DIMENSAO_REGEX, produto)
    return match.group(1) if match else ""

def extrai_embalagem(produto):
    match = re.search(EMBALAGEM_REGEX, produto)
    return match.group(0) if match else ""

# Dados
produtos = [
    "acucar cristal",
    "acucar cristal organico",
    "acucar refinado amorfomicrocristalino",
    "acucar refinado com 400 saches de 5 gramas",
    "acucar refinado granulado  sache de 5 gramas",
    "adocante liquido  100 ml",
    "adocante liquido sacarina  frasco com 100 ml",
    "adocante liquido sucralose  100 ml",
    "alcool etilico 70 pp solucao almotolia 100 ml",
    "alcool etilico hidratado 70 inpm  1 litro",
    "alcool etilico hidratado 70 inpm em gel  440 gramas",
    "alcool liquido 70   1 litro",
    "almofada entintada para carimbo nr 3  azul",
    "almofada entintada para carimbo nr 3  preta",
    "almofada entintada para carimbo nr 4  azul",
    "almofada entintada para carimbo nr 4  preta",
    "almofada entintada para carimbo nr 4  vermelha",
    "apontador para lapis",
    "apontador para lapis simples com reservatorio",
    "borracha branca para lapis",
    "borracha verde  grande",
    "caderno capa dura 14  96 a 100 folhas em papel reciclado",
    "cafe torrado e moido  almofada de 500 gramas",
    "cafe torrado e moido  alto vacuo de 500 gramas  superior",
    "cafe torrado e moido tipo gourmet alto vacuo  500 gramas",
    "cafe torrado e moido tradicional  alto vacuo de 500 gramas",
    "cafe torrado moido pacote com 250 gramas",
    "caixa para arquivo morto em papelao  360 x 250 x 135 mm",
    "caixa para arquivo morto em papelao  360 x 250 x 140 mm",
    "calculadora eletronica de mesa com 12 digitos",
    "caneta esferografica traco 07 mm  azul",
    "caneta esferografica traco 07 mm  preta",
    "caneta esferografica traco 07 mm  vermelha",
    "caneta esferografica traco 1 mm  azul",
    "caneta esferografica traco 1 mm  preta",
    "caneta esferografica traco 1 mm  vermelha",
    "caneta marcatexto  amarela",
    "caneta marcatexto  laranja",
    "caneta marcatexto  rosa",
    "caneta marcatexto  verde",
    "caneta para retroprojetor  azul",
    "caneta para retroprojetor  vermelha",
    "caneta para retroprojetor preta  caixa 12 unidades",
    "cha de camomila com 10 saches  10 gramas",
    "cha de camomila com 15 saches  15 gramas",
    "cha de camomila com 25 saches  40 gramas",
    "cha de capim limao  1 quilo",
    "cha de erva doce  1 quilo",
    "cha de frutas vermelhas com 10 saches  20 gramas",
    "cha de frutas vermelhas com 15 saches  24 gramas",
    "cha de frutas vermelhas com 15 saches  30 gramas",
    "cha de hortela com 10 saches  10 gramas",
    "cha de hortela com 15 saches  15 gramas",
    "cha de hortela com 25 saches  40 gramas",
    "cha de maca com canela com 10 saches  30 gramas",
    "cha de maca com canela com 15 saches  30 gramas",
    "cha de maca vermelha com 10 saches  15 gramas",
    "cha de maca vermelha com 10 saches  20 gramas",
    "cha de morango com 10 saches  15 gramas",
    "cha de pessego com 25 saches  40 gramas",
    "cha mate  200 gramas",
    "cha mate  250 gramas",
    "cha mate natural  caixa com 25 saquinhos",
    "cha mate sabor limao com 25 saches  40 gramas",
    "cha mate sabor natural com 25 saches  40 gramas",
    "cha misto de frutas e flores citricas com 15 saches  15 gramas",
    "cha preto com 15 saches  15 gramas",
    "cha preto sabor limao  340 ml",
    "copo de papel descartavel biodegradavel capacidade 100 ml  100 unidades",
    "copo de papel descartavel biodegradavel capacidade 180 ml   100 unidades",
    "copo de papel descartavel biodegradavel capacidade 50 ml  100 unidades",
    "copo de papel descartavel biodegradavel capacidade 70 ml  50 unidades",
    "copo de papel descartavel capacidade 200 ml  pacote com 25 unidades",
    "copo de papel descartavel para agua  capacidade 180 a 220 ml",
    "copo de papel descartavel para agua  capacidade 180 a 220 ml  50 unidades",
    "copo de papel descartavel para agua  capacidade 200 ml",
    "copo de papel descartavel para cafe  capacidade 45 a 60 ml",
    "copo de papel descartavel para cafe  capacidade 45 a 60 ml  55 unidades",
    "copo de papel descartavel para cafe  capacidade 60 ml",
    "copo de plastico descartavel biodegradavel capacidade 50 ml  pacote com 100 unidades",
    "copo em fibra de coco e polipropileno  300 ml",
    "copo personalizado em fibra de coco  350 ml",
    "copo plastico descartavel  180 ml",
    "copo plastico descartavel  200 ml",
    "copo plastico descartavel  60 ml",
    "copo plastico descartavel  80 ml",
    "copo plastico descartavel biodegradavel capacidade 180 ml  pacote com 100 unidades",
    "copo plastico descartavel para agua  capacidade 150 ml",
    "copo plastico descartavel para cafe  capacidade 50 ml",
    "corretivo em fita  5 mm x 6 m",
    "corretivo em fita 42 mm x 85 m",
    "corretivo em fita de 5 mm  rolo com 5 m",
    "detergente em po  saco com 1 quilo",
    "detergente em po biodegradavel  saco com 5 quilos",
    "detergente liquido biodegradavel  frasco com 500 ml",
    "envelope sem impressao 75gm2  114 x 229 mm  papel reciclado",
    "esponja de espuma  dupla face",
    "esponja de la de aco  pacote com 08 unidades",
    "esponja fibraco dupla face",
    "gas liquefeito de petroleo",
    "gas liquefeito de petroleo  botijao com 13 quilos",
    "gas liquefeito de petroleo  cilindro com 45 quilos",
    "lapis borracha",
    "lapis grafite  2 mm",
    "lapis preto nr2",
    "lapis preto nr2  madeira de manejo sustentavel",
    "lapis preto nr2  madeira de manejo sustentavel",
    "lapiseira corpo em plastico reciclado com clipe ponta e acionador de metalborracha  07 mm",
    "marcador para quadro branco recarregavel  azul",
    "marcador para quadro branco recarregavel  preto",
    "marcador para quadro branco recarregavel  vermelho",
    "pa para lixo com cabo de madeira longo",
    "pano de algodao para copa  40 x 60 cm",
    "pano de algodao para copa  45 x 75 cm",
    "pano de flanela  28 x 38 cm",
    "pano de flanela  30 x 40 cm",
    "pano de flanela  30 x 50 cm",
    "pano de flanela  30 x 60 cm",
    "pano de flanela  38 x 58 cm",
    "pano de flanela  60 x 40 cm ",
    "pano para chao  tipo saco",
    "papel higienico  rolo com 30 metros",
    "papel higienico  rolo com 300 metros",
    "papel higienico  rolo com 40 metros",
    "papel higienico  rolo com 600 metros",
    "papel higienico folha dupla 100 mm x 30 m  selo fsc",
    "papel higienico folha simples rolo 300 metros  pacote com 8 unidades",
    "papel lembrete adesivo em papel reciclado 38 x 50 mm  bloco com 100 folhas",
    "papel lembrete adesivo em papel reciclado 76 x 102 mm  bloco com 100 folhas",
    "papel lembrete adesivo em papel reciclado 76 x 76 mm  bloco com 100 folhas",
    "papel sulfite com certificado ambiental branco a3  75 gm2  297 x 420 mm",
    "papel sulfite com certificado ambiental branco a4  75 gm2  210 x 297 mm",
    "papel sulfite reciclado a4  75gm2  210 x 297 mm",
    "papel toalha em bobina  rolo com 100 metros",
    "papel toalha em bobina folha simples  20 cm x 200 m",
    "papel toalha folha dupla 20 x 22 cm  rolo com 60 folhas",
    "papel toalha interfolha 2 dobras  230 x 210 mm  pacote com 1000 folhas",
    "papel toalha interfolha 3 dobras 230 x 270 mm  1000 folhas",
    "papel toalha picotado  folha dupla  pacote com 2 unidades",
    "pasta para prontuario  rosa claro",
    "pincel atomico ponta fina  traco 2 mm recarregavel  azul",
    "pincel atomico ponta fina  traco 2 mm recarregavel  preto",
    "pincel atomico ponta fina  traco 2 mm recarregavel  verde",
    "pincel atomico ponta fina  traco 2 mm recarregavel  vermelho",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  azul",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  preto",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  verde",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  vermelho",
    "pincel atomico ponta media  traco 4 mm recarregavel  azul",
    "pincel atomico ponta media  traco 4 mm recarregavel  preto",
    "pincel atomico ponta media  traco 4 mm recarregavel  vermelho",
    "porta fita adesiva  pequeno",
    "porta tudo lapis clips e papel",
    "regua plastica  30 cm",
    "regua plastica  40 cm",
    "rodo enxugador  30 cm",
    "rodo enxugador  40 cm",
    "rodo enxugador  60 cm",
    "sabao de coco  pedaco de 200 gramas",
    "sabao em po",
    "tesoura de aco inox  uso geral 10 a 15 cm  media",
    "tesoura de aco inox  uso geral 16 a 22 cm  grande",
    "tinta para carimbo  azul  tubo de 40 a 50 ml",
    "tinta para carimbo  preta  tubo de 40 a 50 ml",
    "tinta para carimbo  vermelha  tubo de 40 a 50 ml",
    "vassoura de pelo  30 cm",
    "vassoura de pelo  40 cm",
    "vassoura de pelo  60 cm",
    "vassoura de piacava  nr04"
]

for produto in produtos:
    apresentacao = extrai_apresentacao(produto)
    tipo = extrai_tipo(produto)
    dimensao = extrai_dimensao(produto)
    embalagem = extrai_embalagem(produto)

    print(f"Apresentação: {apresentacao}")
    print(f"Tipo: {tipo}")
    print(f"Dimensão: {dimensao}")
    print(f"Embalagem: {embalagem}")
    print()

"""# FIM DE TESTE"""

import pandas as pd
import re

# Função para padronizar as informações do produto
def padronizar_produto(produto):
    # Encontra a posição dos delimitadores
    delimitador_pos = [pos for pos, char in enumerate(produto) if char in [',', '-']]

    # Define o ponto de corte baseado na posição do primeiro delimitador
    ponto_de_corte = delimitador_pos[0] if delimitador_pos else len(produto)

    # Divide a descrição em apresentação e tipo
    apresentacao = produto[:ponto_de_corte].strip()
    tipo = produto[ponto_de_corte:].strip(", -") if delimitador_pos else ''

    # Expressões regulares para dimensão e embalagem
    padrao_dimensao = re.compile(r'\d+(\s*x\s*\d+)?\s*(cm|ml|metros|quilos|kg|litros|gramas|unidades|mm|m)', re.IGNORECASE)
    padrao_embalagem = re.compile(r'(pacote com \d+|caixa com \d+|saco com \d+|botijao com \d+|cilindro com \d+|frasco com \d+|almofada de \d+|alto vacuo de \d+|rolo com \d+|bloco com \d+|tubo de \d+ a \d+ ml)', re.IGNORECASE)

    # Encontrando dimensão e embalagem
    dimensao = padrao_dimensao.search(produto)
    embalagem = padrao_embalagem.search(produto)

    # Remove dimensão e embalagem da descrição para obter apenas o tipo
    tipo = padrao_dimensao.sub('', tipo)
    tipo = padrao_embalagem.sub('', tipo).strip(", -")

    # Retorna o produto padronizado
    produto_padronizado = apresentacao
    if tipo:
        produto_padronizado += f", {tipo}"
    if dimensao:
        produto_padronizado += f", {dimensao.group()}"
    if embalagem:
        produto_padronizado += f", {embalagem.group()}"

    return produto_padronizado

# Exemplo de uso da função com uma lista de produtos
produtos = [
    "acucar cristal",
    "acucar cristal organico",
    "acucar refinado amorfomicrocristalino",
    "acucar refinado com 400 saches de 5 gramas",
    "acucar refinado granulado  sache de 5 gramas",
    "adocante liquido  100 ml",
    "adocante liquido sacarina  frasco com 100 ml",
    "adocante liquido sucralose  100 ml",
    "alcool etilico 70 pp solucao almotolia 100 ml",
    "alcool etilico hidratado 70 inpm  1 litro",
    "alcool etilico hidratado 70 inpm em gel  440 gramas",
    "alcool liquido 70   1 litro",
    "almofada entintada para carimbo nr 3  azul",
    "almofada entintada para carimbo nr 3  preta",
    "almofada entintada para carimbo nr 4  azul",
    "almofada entintada para carimbo nr 4  preta",
    "almofada entintada para carimbo nr 4  vermelha",
    "apontador para lapis",
    "apontador para lapis simples com reservatorio",
    "borracha branca para lapis",
    "borracha verde  grande",
    "caderno capa dura 14  96 a 100 folhas em papel reciclado",
    "cafe torrado e moido  almofada de 500 gramas",
    "cafe torrado e moido  alto vacuo de 500 gramas  superior",
    "cafe torrado e moido tipo gourmet alto vacuo  500 gramas",
    "cafe torrado e moido tradicional  alto vacuo de 500 gramas",
    "cafe torrado moido pacote com 250 gramas",
    "caixa para arquivo morto em papelao  360 x 250 x 135 mm",
    "caixa para arquivo morto em papelao  360 x 250 x 140 mm",
    "calculadora eletronica de mesa com 12 digitos",
    "caneta esferografica traco 07 mm  azul",
    "caneta esferografica traco 07 mm  preta",
    "caneta esferografica traco 07 mm  vermelha",
    "caneta esferografica traco 1 mm  azul",
    "caneta esferografica traco 1 mm  preta",
    "caneta esferografica traco 1 mm  vermelha",
    "caneta marcatexto  amarela",
    "caneta marcatexto  laranja",
    "caneta marcatexto  rosa",
    "caneta marcatexto  verde",
    "caneta para retroprojetor  azul",
    "caneta para retroprojetor  vermelha",
    "caneta para retroprojetor preta  caixa 12 unidades",
    "cha de camomila com 10 saches  10 gramas",
    "cha de camomila com 15 saches  15 gramas",
    "cha de camomila com 25 saches  40 gramas",
    "cha de capim limao  1 quilo",
    "cha de erva doce  1 quilo",
    "cha de frutas vermelhas com 10 saches  20 gramas",
    "cha de frutas vermelhas com 15 saches  24 gramas",
    "cha de frutas vermelhas com 15 saches  30 gramas",
    "cha de hortela com 10 saches  10 gramas",
    "cha de hortela com 15 saches  15 gramas",
    "cha de hortela com 25 saches  40 gramas",
    "cha de maca com canela com 10 saches  30 gramas",
    "cha de maca com canela com 15 saches  30 gramas",
    "cha de maca vermelha com 10 saches  15 gramas",
    "cha de maca vermelha com 10 saches  20 gramas",
    "cha de morango com 10 saches  15 gramas",
    "cha de pessego com 25 saches  40 gramas",
    "cha mate  200 gramas",
    "cha mate  250 gramas",
    "cha mate natural  caixa com 25 saquinhos",
    "cha mate sabor limao com 25 saches  40 gramas",
    "cha mate sabor natural com 25 saches  40 gramas",
    "cha misto de frutas e flores citricas com 15 saches  15 gramas",
    "cha preto com 15 saches  15 gramas",
    "cha preto sabor limao  340 ml",
    "copo de papel descartavel biodegradavel capacidade 100 ml  100 unidades",
    "copo de papel descartavel biodegradavel capacidade 180 ml   100 unidades",
    "copo de papel descartavel biodegradavel capacidade 50 ml  100 unidades",
    "copo de papel descartavel biodegradavel capacidade 70 ml  50 unidades",
    "copo de papel descartavel capacidade 200 ml  pacote com 25 unidades",
    "copo de papel descartavel para agua  capacidade 180 a 220 ml",
    "copo de papel descartavel para agua  capacidade 180 a 220 ml  50 unidades",
    "copo de papel descartavel para agua  capacidade 200 ml",
    "copo de papel descartavel para cafe  capacidade 45 a 60 ml",
    "copo de papel descartavel para cafe  capacidade 45 a 60 ml  55 unidades",
    "copo de papel descartavel para cafe  capacidade 60 ml",
    "copo de plastico descartavel biodegradavel capacidade 50 ml  pacote com 100 unidades",
    "copo em fibra de coco e polipropileno  300 ml",
    "copo personalizado em fibra de coco  350 ml",
    "copo plastico descartavel  180 ml",
    "copo plastico descartavel  200 ml",
    "copo plastico descartavel  60 ml",
    "copo plastico descartavel  80 ml",
    "copo plastico descartavel biodegradavel capacidade 180 ml  pacote com 100 unidades",
    "copo plastico descartavel para agua  capacidade 150 ml",
    "copo plastico descartavel para cafe  capacidade 50 ml",
    "corretivo em fita  5 mm x 6 m",
    "corretivo em fita 42 mm x 85 m",
    "corretivo em fita de 5 mm  rolo com 5 m",
    "detergente em po  saco com 1 quilo",
    "detergente em po biodegradavel  saco com 5 quilos",
    "detergente liquido biodegradavel  frasco com 500 ml",
    "envelope sem impressao 75gm2  114 x 229 mm  papel reciclado",
    "esponja de espuma  dupla face",
    "esponja de la de aco  pacote com 08 unidades",
    "esponja fibraco dupla face",
    "gas liquefeito de petroleo",
    "gas liquefeito de petroleo  botijao com 13 quilos",
    "gas liquefeito de petroleo  cilindro com 45 quilos",
    "lapis borracha",
    "lapis grafite  2 mm",
    "lapis preto nr2",
    "lapis preto nr2  madeira de manejo sustentavel",
    "lapis preto nr2  madeira de manejo sustentavel",
    "lapiseira corpo em plastico reciclado com clipe ponta e acionador de metalborracha  07 mm",
    "marcador para quadro branco recarregavel  azul",
    "marcador para quadro branco recarregavel  preto",
    "marcador para quadro branco recarregavel  vermelho",
    "pa para lixo com cabo de madeira longo",
    "pano de algodao para copa  40 x 60 cm",
    "pano de algodao para copa  45 x 75 cm",
    "pano de flanela  28 x 38 cm",
    "pano de flanela  30 x 40 cm",
    "pano de flanela  30 x 50 cm",
    "pano de flanela  30 x 60 cm",
    "pano de flanela  38 x 58 cm",
    "pano de flanela  60 x 40 cm ",
    "pano para chao  tipo saco",
    "papel higienico  rolo com 30 metros",
    "papel higienico  rolo com 300 metros",
    "papel higienico  rolo com 40 metros",
    "papel higienico  rolo com 600 metros",
    "papel higienico folha dupla 100 mm x 30 m  selo fsc",
    "papel higienico folha simples rolo 300 metros  pacote com 8 unidades",
    "papel lembrete adesivo em papel reciclado 38 x 50 mm  bloco com 100 folhas",
    "papel lembrete adesivo em papel reciclado 76 x 102 mm  bloco com 100 folhas",
    "papel lembrete adesivo em papel reciclado 76 x 76 mm  bloco com 100 folhas",
    "papel sulfite com certificado ambiental branco a3  75 gm2  297 x 420 mm",
    "papel sulfite com certificado ambiental branco a4  75 gm2  210 x 297 mm",
    "papel sulfite reciclado a4  75gm2  210 x 297 mm",
    "papel toalha em bobina  rolo com 100 metros",
    "papel toalha em bobina folha simples  20 cm x 200 m",
    "papel toalha folha dupla 20 x 22 cm  rolo com 60 folhas",
    "papel toalha interfolha 2 dobras  230 x 210 mm  pacote com 1000 folhas",
    "papel toalha interfolha 3 dobras 230 x 270 mm  1000 folhas",
    "papel toalha picotado  folha dupla  pacote com 2 unidades",
    "pasta para prontuario  rosa claro",
    "pincel atomico ponta fina  traco 2 mm recarregavel  azul",
    "pincel atomico ponta fina  traco 2 mm recarregavel  preto",
    "pincel atomico ponta fina  traco 2 mm recarregavel  verde",
    "pincel atomico ponta fina  traco 2 mm recarregavel  vermelho",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  azul",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  preto",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  verde",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  vermelho",
    "pincel atomico ponta media  traco 4 mm recarregavel  azul",
    "pincel atomico ponta media  traco 4 mm recarregavel  preto",
    "pincel atomico ponta media  traco 4 mm recarregavel  vermelho",
    "porta fita adesiva  pequeno",
    "porta tudo lapis clips e papel",
    "regua plastica  30 cm",
    "regua plastica  40 cm",
    "rodo enxugador  30 cm",
    "rodo enxugador  40 cm",
    "rodo enxugador  60 cm",
    "sabao de coco  pedaco de 200 gramas",
    "sabao em po",
    "tesoura de aco inox  uso geral 10 a 15 cm  media",
    "tesoura de aco inox  uso geral 16 a 22 cm  grande",
    "tinta para carimbo  azul  tubo de 40 a 50 ml",
    "tinta para carimbo  preta  tubo de 40 a 50 ml",
    "tinta para carimbo  vermelha  tubo de 40 a 50 ml",
    "vassoura de pelo  30 cm",
    "vassoura de pelo  40 cm",
    "vassoura de pelo  60 cm",
    "vassoura de piacava  nr04"
]

# Processando cada produto
for produto in produtos:
    resultado = padronizar_produto(produto)
    print(resultado)

# Suponha que o DataFrame já foi carregado
dataset = pd.read_excel('/content/Itens centralizáveis 23_10_26.xlsx')

dataset['Item'] = dataset['Item'].apply(padronizar_produto)
dataset.to_csv('seu_dataset_modificado.csv', index=False)

pd.read_csv("/content/seu_dataset_modificado.csv")



import pandas as pd
import re

# Função para extrair as informações de cada produto
def padronizar_produto(produto):
    padroes_tamanho = [
        'pequeno', 'medio', 'grande', 'largo', 'estreito',
        'fino', 'grosso', 'alto', 'baixo', 'gigante', 'mini', 'compacto'
    ]
    padrao_tamanho = r'(' + '|'.join(padroes_tamanho) + ')'
    padrao_dimensao = re.compile(r'\d+(\s*x\s*\d+)?\s*(cm|ml|metros|quilos|kg|litros|gramas|unidades|mm|m)')
    padrao_embalagem = re.compile(r'(pacote com \d+|caixa com \d+|saco com \d+|botijao com \d+|cilindro com \d+|frasco com \d+|almofada de \d+|alto vacuo de \d+|rolo com \d+|bloco com \d+|tubo de \d+ a \d+ ml)', re.IGNORECASE)

    # Adiciona adjetivos de tamanho como parte do padrão de embalagem
    padrao_embalagem_com_tamanho = re.compile(padrao_tamanho + r'\s+' + padrao_embalagem.pattern)

    # Encontrando dimensão, embalagem e tamanho
    dimensao = padrao_dimensao.search(produto)
    embalagem = padrao_embalagem_com_tamanho.search(produto) or padrao_embalagem.search(produto)

    # Remove dimensão, embalagem e tamanho da descrição
    descricao_sem_dimensao = padrao_dimensao.sub('', produto)
    descricao_sem_embalagem = padrao_embalagem_com_tamanho.sub('', descricao_sem_dimensao).strip()

    # Divide a descrição em apresentação e tipo, considerando preposições e conjunções
    partes = re.split(r'\s(de|para|com|em|sem|e)\s', descricao_sem_embalagem, 1)
    apresentacao = partes[0].strip()
    tipo = " ".join(partes[1:]).strip() if len(partes) > 1 else ''

    # Retorna o produto padronizado
    produto_padronizado = apresentacao
    if tipo:
        produto_padronizado += f" {tipo}"
    if dimensao:
        produto_padronizado += f", {dimensao.group()}"
    if embalagem:
        produto_padronizado += f", {embalagem.group()}"

    return produto_padronizado

# Supondo que você já tenha o DataFrame carregado:
dataset = pd.read_csv('/content/dados_padronizados_amostra_centralizados')

# Aplicar a padronização à coluna 'Item'
dataset['Item'] = dataset['Item'].apply(padronizar_produto)

# Salvar o DataFrame padronizado
dataset.to_csv('seu_dataset_modificado.csv', index=False)

import pandas as pd
pd.read_excel("/content/Itens centralizáveis 23_10_26.xlsx").describe

import re

UNIDADES_MEDIDA = ["cm", "mm", "m", "ml", "l", "g", "kg", "x", "un", "pct", "cx"]

def extrai_dimensao(produto):
    palavras = produto.split()
    dimensao = ""
    for p in palavras:
        numero = re.search(r"^\d+", p)
        if numero and p[-2:] in UNIDADES_MEDIDA:
            dimensao += p + " "

    if dimensao:
        return dimensao.strip()
    else:
        return ""

def extrai_tipo(produto):
  apresentacao = extrai_apresentacao(produto)
  if apresentacao in produto:
    tipo = produto.split(apresentacao)[1]
    match = re.search(TIPO_REGEX, tipo)
    if match:
      return match.group(1)
  return ""


def extrai_apresentacao(produto):
  termos_exclusao = ["de","do","da","em","para","com"]
  termo = ""
  for palavra in produto.split():
    if palavra.lower() not in termos_exclusao:
        termo += palavra + " "
    else:
        break
  return termo.strip()

produto = [
    "acucar cristal",
    "acucar cristal organico",
    "acucar refinado amorfomicrocristalino",
    "acucar refinado com 400 saches de 5 gramas",
    "acucar refinado granulado  sache de 5 gramas",
    "adocante liquido  100 ml",
    "adocante liquido sacarina  frasco com 100 ml",
    "adocante liquido sucralose  100 ml",
    "alcool etilico 70 pp solucao almotolia 100 ml",
    "alcool etilico hidratado 70 inpm  1 litro",
    "alcool etilico hidratado 70 inpm em gel  440 gramas",
    "alcool liquido 70   1 litro",
    "almofada entintada para carimbo nr 3  azul",
    "almofada entintada para carimbo nr 3  preta",
    "almofada entintada para carimbo nr 4  azul",
    "almofada entintada para carimbo nr 4  preta",
    "almofada entintada para carimbo nr 4  vermelha",
    "apontador para lapis",
    "apontador para lapis simples com reservatorio",
    "borracha branca para lapis",
    "borracha verde  grande",
    "caderno capa dura 14  96 a 100 folhas em papel reciclado",
    "cafe torrado e moido  almofada de 500 gramas",
    "cafe torrado e moido  alto vacuo de 500 gramas  superior",
    "cafe torrado e moido tipo gourmet alto vacuo  500 gramas",
    "cafe torrado e moido tradicional  alto vacuo de 500 gramas",
    "cafe torrado moido pacote com 250 gramas",
    "caixa para arquivo morto em papelao  360 x 250 x 135 mm",
    "caixa para arquivo morto em papelao  360 x 250 x 140 mm",
    "calculadora eletronica de mesa com 12 digitos",
    "caneta esferografica traco 07 mm  azul",
    "caneta esferografica traco 07 mm  preta",
    "caneta esferografica traco 07 mm  vermelha",
    "caneta esferografica traco 1 mm  azul",
    "caneta esferografica traco 1 mm  preta",
    "caneta esferografica traco 1 mm  vermelha",
    "caneta marcatexto  amarela",
    "caneta marcatexto  laranja",
    "caneta marcatexto  rosa",
    "caneta marcatexto  verde",
    "caneta para retroprojetor  azul",
    "caneta para retroprojetor  vermelha",
    "caneta para retroprojetor preta  caixa 12 unidades",
    "cha de camomila com 10 saches  10 gramas",
    "cha de camomila com 15 saches  15 gramas",
    "cha de camomila com 25 saches  40 gramas",
    "cha de capim limao  1 quilo",
    "cha de erva doce  1 quilo",
    "cha de frutas vermelhas com 10 saches  20 gramas",
    "cha de frutas vermelhas com 15 saches  24 gramas",
    "cha de frutas vermelhas com 15 saches  30 gramas",
    "cha de hortela com 10 saches  10 gramas",
    "cha de hortela com 15 saches  15 gramas",
    "cha de hortela com 25 saches  40 gramas",
    "cha de maca com canela com 10 saches  30 gramas",
    "cha de maca com canela com 15 saches  30 gramas",
    "cha de maca vermelha com 10 saches  15 gramas",
    "cha de maca vermelha com 10 saches  20 gramas",
    "cha de morango com 10 saches  15 gramas",
    "cha de pessego com 25 saches  40 gramas",
    "cha mate  200 gramas",
    "cha mate  250 gramas",
    "cha mate natural  caixa com 25 saquinhos",
    "cha mate sabor limao com 25 saches  40 gramas",
    "cha mate sabor natural com 25 saches  40 gramas",
    "cha misto de frutas e flores citricas com 15 saches  15 gramas",
    "cha preto com 15 saches  15 gramas",
    "cha preto sabor limao  340 ml",
    "copo de papel descartavel biodegradavel capacidade 100 ml  100 unidades",
    "copo de papel descartavel biodegradavel capacidade 180 ml   100 unidades",
    "copo de papel descartavel biodegradavel capacidade 50 ml  100 unidades",
    "copo de papel descartavel biodegradavel capacidade 70 ml  50 unidades",
    "copo de papel descartavel capacidade 200 ml  pacote com 25 unidades",
    "copo de papel descartavel para agua  capacidade 180 a 220 ml",
    "copo de papel descartavel para agua  capacidade 180 a 220 ml  50 unidades",
    "copo de papel descartavel para agua  capacidade 200 ml",
    "copo de papel descartavel para cafe  capacidade 45 a 60 ml",
    "copo de papel descartavel para cafe  capacidade 45 a 60 ml  55 unidades",
    "copo de papel descartavel para cafe  capacidade 60 ml",
    "copo de plastico descartavel biodegradavel capacidade 50 ml  pacote com 100 unidades",
    "copo em fibra de coco e polipropileno  300 ml",
    "copo personalizado em fibra de coco  350 ml",
    "copo plastico descartavel  180 ml",
    "copo plastico descartavel  200 ml",
    "copo plastico descartavel  60 ml",
    "copo plastico descartavel  80 ml",
    "copo plastico descartavel biodegradavel capacidade 180 ml  pacote com 100 unidades",
    "copo plastico descartavel para agua  capacidade 150 ml",
    "copo plastico descartavel para cafe  capacidade 50 ml",
    "corretivo em fita  5 mm x 6 m",
    "corretivo em fita 42 mm x 85 m",
    "corretivo em fita de 5 mm  rolo com 5 m",
    "detergente em po  saco com 1 quilo",
    "detergente em po biodegradavel  saco com 5 quilos",
    "detergente liquido biodegradavel  frasco com 500 ml",
    "envelope sem impressao 75gm2  114 x 229 mm  papel reciclado",
    "esponja de espuma  dupla face",
    "esponja de la de aco  pacote com 08 unidades",
    "esponja fibraco dupla face",
    "gas liquefeito de petroleo",
    "gas liquefeito de petroleo  botijao com 13 quilos",
    "gas liquefeito de petroleo  cilindro com 45 quilos",
    "lapis borracha",
    "lapis grafite  2 mm",
    "lapis preto nr2",
    "lapis preto nr2  madeira de manejo sustentavel",
    "lapis preto nr2  madeira de manejo sustentavel",
    "lapiseira corpo em plastico reciclado com clipe ponta e acionador de metalborracha  07 mm",
    "marcador para quadro branco recarregavel  azul",
    "marcador para quadro branco recarregavel  preto",
    "marcador para quadro branco recarregavel  vermelho",
    "pa para lixo com cabo de madeira longo",
    "pano de algodao para copa  40 x 60 cm",
    "pano de algodao para copa  45 x 75 cm",
    "pano de flanela  28 x 38 cm",
    "pano de flanela  30 x 40 cm",
    "pano de flanela  30 x 50 cm",
    "pano de flanela  30 x 60 cm",
    "pano de flanela  38 x 58 cm",
    "pano de flanela  60 x 40 cm ",
    "pano para chao  tipo saco",
    "papel higienico  rolo com 30 metros",
    "papel higienico  rolo com 300 metros",
    "papel higienico  rolo com 40 metros",
    "papel higienico  rolo com 600 metros",
    "papel higienico folha dupla 100 mm x 30 m  selo fsc",
    "papel higienico folha simples rolo 300 metros  pacote com 8 unidades",
    "papel lembrete adesivo em papel reciclado 38 x 50 mm  bloco com 100 folhas",
    "papel lembrete adesivo em papel reciclado 76 x 102 mm  bloco com 100 folhas",
    "papel lembrete adesivo em papel reciclado 76 x 76 mm  bloco com 100 folhas",
    "papel sulfite com certificado ambiental branco a3  75 gm2  297 x 420 mm",
    "papel sulfite com certificado ambiental branco a4  75 gm2  210 x 297 mm",
    "papel sulfite reciclado a4  75gm2  210 x 297 mm",
    "papel toalha em bobina  rolo com 100 metros",
    "papel toalha em bobina folha simples  20 cm x 200 m",
    "papel toalha folha dupla 20 x 22 cm  rolo com 60 folhas",
    "papel toalha interfolha 2 dobras  230 x 210 mm  pacote com 1000 folhas",
    "papel toalha interfolha 3 dobras 230 x 270 mm  1000 folhas",
    "papel toalha picotado  folha dupla  pacote com 2 unidades",
    "pasta para prontuario  rosa claro",
    "pincel atomico ponta fina  traco 2 mm recarregavel  azul",
    "pincel atomico ponta fina  traco 2 mm recarregavel  preto",
    "pincel atomico ponta fina  traco 2 mm recarregavel  verde",
    "pincel atomico ponta fina  traco 2 mm recarregavel  vermelho",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  azul",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  preto",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  verde",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  vermelho",
    "pincel atomico ponta media  traco 4 mm recarregavel  azul",
    "pincel atomico ponta media  traco 4 mm recarregavel  preto",
    "pincel atomico ponta media  traco 4 mm recarregavel  vermelho",
    "porta fita adesiva  pequeno",
    "porta tudo lapis clips e papel",
    "regua plastica  30 cm",
    "regua plastica  40 cm",
    "rodo enxugador  30 cm",
    "rodo enxugador  40 cm",
    "rodo enxugador  60 cm",
    "sabao de coco  pedaco de 200 gramas",
    "sabao em po",
    "tesoura de aco inox  uso geral 10 a 15 cm  media",
    "tesoura de aco inox  uso geral 16 a 22 cm  grande",
    "tinta para carimbo  azul  tubo de 40 a 50 ml",
    "tinta para carimbo  preta  tubo de 40 a 50 ml",
    "tinta para carimbo  vermelha  tubo de 40 a 50 ml",
    "vassoura de pelo  30 cm",
    "vassoura de pelo  40 cm",
    "vassoura de pelo  60 cm",
    "vassoura de piacava  nr04"
]


print(f"Dimensão: {extrai_dimensao(produto)}")
print(f"Tipo: {extrai_tipo(produto)}")

import re

TIPO_REGEX = r'([a-zA-Z0-9]+(?=\s+\d+))?'
DIMENSAO_REGEX = r'((?:\d+,?)+\.?\d*\s*(?:cm|mm|m|ml|l|g|kg|x|por|\d+))'
UNIDADES_MEDIDA = ["cm", "mm", "m", "ml", "l", "g", "kg", "x", "un", "pct", "cx"]

def extrai_dimensao(produto):
    palavras = produtos.split()
    dimensao = ""
    for p in palavras:
        numero = re.search(r'^\d+', p)
        if numero and p[-2:] in UNIDADES_MEDIDA:
            dimensao += p + " "

    if dimensao:
        return dimensao.strip()
    else:
        return ""



def extrai_dimensao(produto):
   match = re.search(DIMENSAO_REGEX, produtos)
   if match:
     return match.group(1)
   else:
     return ""



EMBALAGEM_REGEX = r'\b(pequeno|pequena|medio|media|grande|fino|fina|vermelho|preto|etc)\b'

def extrai_tipo(produto):
  apresentacao = extrai_apresentacao(produto)

  if apresentacao in produto:
    tipo = produto.split(apresentacao)[1]
    match = re.search(TIPO_REGEX, tipo)
    if match:
      return match.group(1)

  return ""

def extrai_dimensao(produto):
    match = re.search(DIMENSAO_REGEX, produto)
    if match:
        return match.group(1)
    else:
        return ""

def extrai_embalagem(produto):
    match = re.search(EMBALAGEM_REGEX, produto)
    if match:
        return match.group(0)
    else:
        return ""

def extrai_apresentacao(produto):
    termos_exclusao = ["de","do","da","em","para","com"]
    termo = ""
    for palavra in produto.split():
        if palavra.lower() not in termos_exclusao:
            termo += palavra + " "
        else:
            break
    return termo.strip()


# Dados
produtos = [
    "acucar cristal",
    "acucar cristal organico",
    "acucar refinado amorfomicrocristalino",
    "acucar refinado com 400 saches de 5 gramas",
    "acucar refinado granulado  sache de 5 gramas",
    "adocante liquido  100 ml",
    "adocante liquido sacarina  frasco com 100 ml",
    "adocante liquido sucralose  100 ml",
    "alcool etilico 70 pp solucao almotolia 100 ml",
    "alcool etilico hidratado 70 inpm  1 litro",
    "alcool etilico hidratado 70 inpm em gel  440 gramas",
    "alcool liquido 70   1 litro",
    "almofada entintada para carimbo nr 3  azul",
    "almofada entintada para carimbo nr 3  preta",
    "almofada entintada para carimbo nr 4  azul",
    "almofada entintada para carimbo nr 4  preta",
    "almofada entintada para carimbo nr 4  vermelha",
    "apontador para lapis",
    "apontador para lapis simples com reservatorio",
    "borracha branca para lapis",
    "borracha verde  grande",
    "caderno capa dura 14  96 a 100 folhas em papel reciclado",
    "cafe torrado e moido  almofada de 500 gramas",
    "cafe torrado e moido  alto vacuo de 500 gramas  superior",
    "cafe torrado e moido tipo gourmet alto vacuo  500 gramas",
    "cafe torrado e moido tradicional  alto vacuo de 500 gramas",
    "cafe torrado moido pacote com 250 gramas",
    "caixa para arquivo morto em papelao  360 x 250 x 135 mm",
    "caixa para arquivo morto em papelao  360 x 250 x 140 mm",
    "calculadora eletronica de mesa com 12 digitos",
    "caneta esferografica traco 07 mm  azul",
    "caneta esferografica traco 07 mm  preta",
    "caneta esferografica traco 07 mm  vermelha",
    "caneta esferografica traco 1 mm  azul",
    "caneta esferografica traco 1 mm  preta",
    "caneta esferografica traco 1 mm  vermelha",
    "caneta marcatexto  amarela",
    "caneta marcatexto  laranja",
    "caneta marcatexto  rosa",
    "caneta marcatexto  verde",
    "caneta para retroprojetor  azul",
    "caneta para retroprojetor  vermelha",
    "caneta para retroprojetor preta  caixa 12 unidades",
    "cha de camomila com 10 saches  10 gramas",
    "cha de camomila com 15 saches  15 gramas",
    "cha de camomila com 25 saches  40 gramas",
    "cha de capim limao  1 quilo",
    "cha de erva doce  1 quilo",
    "cha de frutas vermelhas com 10 saches  20 gramas",
    "cha de frutas vermelhas com 15 saches  24 gramas",
    "cha de frutas vermelhas com 15 saches  30 gramas",
    "cha de hortela com 10 saches  10 gramas",
    "cha de hortela com 15 saches  15 gramas",
    "cha de hortela com 25 saches  40 gramas",
    "cha de maca com canela com 10 saches  30 gramas",
    "cha de maca com canela com 15 saches  30 gramas",
    "cha de maca vermelha com 10 saches  15 gramas",
    "cha de maca vermelha com 10 saches  20 gramas",
    "cha de morango com 10 saches  15 gramas",
    "cha de pessego com 25 saches  40 gramas",
    "cha mate  200 gramas",
    "cha mate  250 gramas",
    "cha mate natural  caixa com 25 saquinhos",
    "cha mate sabor limao com 25 saches  40 gramas",
    "cha mate sabor natural com 25 saches  40 gramas",
    "cha misto de frutas e flores citricas com 15 saches  15 gramas",
    "cha preto com 15 saches  15 gramas",
    "cha preto sabor limao  340 ml",
    "copo de papel descartavel biodegradavel capacidade 100 ml  100 unidades",
    "copo de papel descartavel biodegradavel capacidade 180 ml   100 unidades",
    "copo de papel descartavel biodegradavel capacidade 50 ml  100 unidades",
    "copo de papel descartavel biodegradavel capacidade 70 ml  50 unidades",
    "copo de papel descartavel capacidade 200 ml  pacote com 25 unidades",
    "copo de papel descartavel para agua  capacidade 180 a 220 ml",
    "copo de papel descartavel para agua  capacidade 180 a 220 ml  50 unidades",
    "copo de papel descartavel para agua  capacidade 200 ml",
    "copo de papel descartavel para cafe  capacidade 45 a 60 ml",
    "copo de papel descartavel para cafe  capacidade 45 a 60 ml  55 unidades",
    "copo de papel descartavel para cafe  capacidade 60 ml",
    "copo de plastico descartavel biodegradavel capacidade 50 ml  pacote com 100 unidades",
    "copo em fibra de coco e polipropileno  300 ml",
    "copo personalizado em fibra de coco  350 ml",
    "copo plastico descartavel  180 ml",
    "copo plastico descartavel  200 ml",
    "copo plastico descartavel  60 ml",
    "copo plastico descartavel  80 ml",
    "copo plastico descartavel biodegradavel capacidade 180 ml  pacote com 100 unidades",
    "copo plastico descartavel para agua  capacidade 150 ml",
    "copo plastico descartavel para cafe  capacidade 50 ml",
    "corretivo em fita  5 mm x 6 m",
    "corretivo em fita 42 mm x 85 m",
    "corretivo em fita de 5 mm  rolo com 5 m",
    "detergente em po  saco com 1 quilo",
    "detergente em po biodegradavel  saco com 5 quilos",
    "detergente liquido biodegradavel  frasco com 500 ml",
    "envelope sem impressao 75gm2  114 x 229 mm  papel reciclado",
    "esponja de espuma  dupla face",
    "esponja de la de aco  pacote com 08 unidades",
    "esponja fibraco dupla face",
    "gas liquefeito de petroleo",
    "gas liquefeito de petroleo  botijao com 13 quilos",
    "gas liquefeito de petroleo  cilindro com 45 quilos",
    "lapis borracha",
    "lapis grafite  2 mm",
    "lapis preto nr2",
    "lapis preto nr2  madeira de manejo sustentavel",
    "lapis preto nr2  madeira de manejo sustentavel",
    "lapiseira corpo em plastico reciclado com clipe ponta e acionador de metalborracha  07 mm",
    "marcador para quadro branco recarregavel  azul",
    "marcador para quadro branco recarregavel  preto",
    "marcador para quadro branco recarregavel  vermelho",
    "pa para lixo com cabo de madeira longo",
    "pano de algodao para copa  40 x 60 cm",
    "pano de algodao para copa  45 x 75 cm",
    "pano de flanela  28 x 38 cm",
    "pano de flanela  30 x 40 cm",
    "pano de flanela  30 x 50 cm",
    "pano de flanela  30 x 60 cm",
    "pano de flanela  38 x 58 cm",
    "pano de flanela  60 x 40 cm ",
    "pano para chao  tipo saco",
    "papel higienico  rolo com 30 metros",
    "papel higienico  rolo com 300 metros",
    "papel higienico  rolo com 40 metros",
    "papel higienico  rolo com 600 metros",
    "papel higienico folha dupla 100 mm x 30 m  selo fsc",
    "papel higienico folha simples rolo 300 metros  pacote com 8 unidades",
    "papel lembrete adesivo em papel reciclado 38 x 50 mm  bloco com 100 folhas",
    "papel lembrete adesivo em papel reciclado 76 x 102 mm  bloco com 100 folhas",
    "papel lembrete adesivo em papel reciclado 76 x 76 mm  bloco com 100 folhas",
    "papel sulfite com certificado ambiental branco a3  75 gm2  297 x 420 mm",
    "papel sulfite com certificado ambiental branco a4  75 gm2  210 x 297 mm",
    "papel sulfite reciclado a4  75gm2  210 x 297 mm",
    "papel toalha em bobina  rolo com 100 metros",
    "papel toalha em bobina folha simples  20 cm x 200 m",
    "papel toalha folha dupla 20 x 22 cm  rolo com 60 folhas",
    "papel toalha interfolha 2 dobras  230 x 210 mm  pacote com 1000 folhas",
    "papel toalha interfolha 3 dobras 230 x 270 mm  1000 folhas",
    "papel toalha picotado  folha dupla  pacote com 2 unidades",
    "pasta para prontuario  rosa claro",
    "pincel atomico ponta fina  traco 2 mm recarregavel  azul",
    "pincel atomico ponta fina  traco 2 mm recarregavel  preto",
    "pincel atomico ponta fina  traco 2 mm recarregavel  verde",
    "pincel atomico ponta fina  traco 2 mm recarregavel  vermelho",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  azul",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  preto",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  verde",
    "pincel atomico ponta grossa  traco 8 mm recarregavel  vermelho",
    "pincel atomico ponta media  traco 4 mm recarregavel  azul",
    "pincel atomico ponta media  traco 4 mm recarregavel  preto",
    "pincel atomico ponta media  traco 4 mm recarregavel  vermelho",
    "porta fita adesiva  pequeno",
    "porta tudo lapis clips e papel",
    "regua plastica  30 cm",
    "regua plastica  40 cm",
    "rodo enxugador  30 cm",
    "rodo enxugador  40 cm",
    "rodo enxugador  60 cm",
    "sabao de coco  pedaco de 200 gramas",
    "sabao em po",
    "tesoura de aco inox  uso geral 10 a 15 cm  media",
    "tesoura de aco inox  uso geral 16 a 22 cm  grande",
    "tinta para carimbo  azul  tubo de 40 a 50 ml",
    "tinta para carimbo  preta  tubo de 40 a 50 ml",
    "tinta para carimbo  vermelha  tubo de 40 a 50 ml",
    "vassoura de pelo  30 cm",
    "vassoura de pelo  40 cm",
    "vassoura de pelo  60 cm",
    "vassoura de piacava  nr04"
]


for produto in produtos:
    apresentacao = extrai_apresentacao(produto)
    tipo = extrai_tipo(produto)
    dimensao = extrai_dimensao(produto)
    embalagem = extrai_embalagem(produto)

    print(f"Apresentação: {apresentacao}")
    print(f"Tipo: {tipo}")
    print(f"Dimensão: {dimensao}")
    print(f"Embalagem: {embalagem}")
    print()

TIPO_MAP = {
    'ml': 'mililitro',
    'cm': 'centimetro',
    'mm': 'milimetro',
    'm': 'metro',
    'kg': 'quilograma',
    'g': 'grama',
    'l': 'litro',
    'un': 'unidade',
    'pct': 'pacote',
    'cx': 'caixa',
    'und': 'unidade',
    'pc': 'peça',
    'pcs': 'peças',
    'gr': 'grama',
    'mg': 'miligrama',
    'lt': 'litro',
    'm2': 'metro quadrado',
    'm3': 'metro cúbico',
    'km': 'quilometro',
    'hz': 'hertz',
    'w': 'watt',
    'kw': 'kilowatt',
    'v': 'volt',
    'amp': 'ampere',
    'in': 'polegada',
    'ft': 'pé',
    'lb': 'libra',
    'oz': 'onça',
    'nr': 'numero'
}

import pandas as pd
import re

# Carrega o dataset
dataset = pd.read_excel('/content/Itens centralizáveis 23_10_26.xlsx')

# Define a função de padronização conforme anteriormente
# Função para padronizar as informações do produto
def padronizar_produto(descricao):
    # Expressões regulares para identificar dimensões e embalagens
    padrao_dimensao = re.compile(r'(\d+\s?(x\s?\d+)?\s?(gramas|ml|litro|saches|pp|inpm|cm|mm|m))', re.IGNORECASE)
    padrao_embalagem = re.compile(r'(pacote com \d+|caixa com \d+|saco com \d+|botijao com \d+|cilindro com \d+|frasco com \d+|almofada de \d+|alto vacuo de \d+|rolo com \d+|bloco com \d+|tubo de \d+ a \d+ ml)', re.IGNORECASE)

    # Encontra dimensão e embalagem
    dimensao = padrao_dimensao.search(descricao)
    embalagem = padrao_embalagem.search(descricao)

    # Remove dimensão e embalagem da descrição para obter a apresentação
    descricao_sem_dimensao = padrao_dimensao.sub('', descricao)
    descricao_sem_embalagem = padrao_embalagem.sub('', descricao_sem_dimensao).strip()

    # Identifica a apresentação e o tipo (se houver)
    partes = descricao_sem_embalagem.split('  ')
    apresentacao = partes[0].strip()
    tipo = partes[1].strip() if len(partes) > 1 else ''

    # Retorna um dicionário com as informações padronizadas
    return {
        "Apresentação": apresentacao,
        "Tipo": tipo,
        "Dimensão": dimensao.group().strip() if dimensao else '',
        "Embalagem": embalagem.group().strip() if embalagem else ''
    }

# Aplica a função a cada descrição do produto no dataset
# Supondo que a coluna com as descrições se chame 'descricao_produto'
produtos_padronizados = dataset['Item'].apply(padronizar_produto)
# Cria novas colunas no dataset para as informações padronizadas
dataset['Apresentacao'] = produtos_padronizados.apply(lambda x: x['Apresentação'])
dataset['Tipo'] = produtos_padronizados.apply(lambda x: x['Tipo'])
dataset['Dimensao'] = produtos_padronizados.apply(lambda x: x['Dimensão'])
dataset['Embalagem'] = produtos_padronizados.apply(lambda x: x['Embalagem'])

# Salva o dataset modificado
dataset.to_csv('dados_padronizados_amostra_centralizados', index=False)

pd.read_csv("/content/dados_padronizados_amostra_centralizados")

produtos_padronizados = dataset['Item'].apply(padronizar_produto)

dataset

!pip install ngram
!pip install unidecode
!pip install fuzzywuzzy
!pip install unidecode
!pip install transformers
!pip install torch
!pip install bert
!pip install bert-serving-client

import pandas as pd
from fuzzywuzzy import fuzz
from bert_serving.client import BertClient
import numpy as np

# Função para calcular a similaridade BERT entre duas strings
def bert_similarity(text1, text2, bert_client):
    embeddings1 = bert_client.encode([text1])
    embeddings2 = bert_client.encode([text2])
    cosine_similarity = np.dot(embeddings1, embeddings2.T) / (np.linalg.norm(embeddings1) * np.linalg.norm(embeddings2))
    return cosine_similarity[0][0]

# Defina os datasets, colunas de comparação e subgrupos de códigos desejados
dataset1 = pd.read_csv('/content/Itens centralizáveis 23_10_26.csv',sep=";")
dataset2 = pd.read_excel('/content/catmat112023.xlsx')
comparison_column1 = 'Item'
comparison_column2 = 'Item'
desired_subgroups1 = [51]
desired_subgroups2 = [72,73,75,76,85]

# Filtrar os datasets com base nos subgrupos de códigos desejados
filtered_dataset1 = dataset1[dataset1['Natureza'].isin(desired_subgroups1)]
filtered_dataset2 = dataset2[dataset2['cod_grupo'].isin(desired_subgroups2)]

# Inicialize o cliente BERT
bert_client = BertClient(check_length=False)

results = []

for index, row1 in filtered_dataset1.iterrows():
    item1 = row1[comparison_column1]
    print(f"\nComparando item {index + 1}/{len(filtered_dataset1)} do dataset1: '{item1}'")

    max_similarity = 0
    best_match = None

    for _, row2 in filtered_dataset2.iterrows():
        item2 = row2[comparison_column2]

        # Verifique se todos os n-grams do item1 existem em item2
        ngrams_item1 = set(item1.split())
        ngrams_item2 = set(item2.split())

        if ngrams_item1.issubset(ngrams_item2):
            # Calcule a similaridade BERT
            similarity_bert = bert_similarity(item1, item2, bert_client)

            if similarity_bert > max_similarity:
                max_similarity = similarity_bert
                best_match = row2  # Mantenha o registro correspondente de dataset2

    if best_match is not None:
        results.append({
            'item1': item1,
            'item2': best_match[comparison_column2],
            'similarity_bert': max_similarity
        })

# Ordene os resultados por similaridade BERT em ordem decrescente
results.sort(key=lambda x: x['similarity_bert'], reverse=True)

# Exiba os resultados
for result in results:
    print(f"Item 1: {result['item1']}")
    print(f"Item 2: {result['item2']}")
    print(f"Similaridade BERT: {result['similarity_bert']}")
    print("=" * 50)

# Feche o cliente BERT
bert_client.close()

