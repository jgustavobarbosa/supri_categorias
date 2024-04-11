# supri_categorias
Script para categorização dos itens de descrição do COBES - SUPRI pmsp
Aqui há a explicação do propósito do script, como ele funciona e como outros podem usá-lo.

---

# Categorizador de Itens

Este script Python automatiza a categorização de itens com base em suas descrições, utilizando expressões regulares para identificar características específicas como peso, volume, quantidade, dimensões, tipo, linha, cor, material, entre outros. Destina-se a simplificar a organização de inventários ou listagens de produtos, proporcionando uma visão estruturada das principais características dos itens listados.

## Funcionalidades

- **Detecção Automática de Características**: Identifica e categoriza automaticamente as características dos itens, como peso, volume e tipo, com base em suas descrições.
- **Suporte a Várias Unidades e Categorias**: O script pode reconhecer uma ampla gama de unidades de medida e categorias, tornando-o versátil para diversos tipos de inventários.
- **Facilidade de Expansão**: As expressões regulares usadas para a identificação das características podem ser facilmente ajustadas ou expandidas para atender a necessidades específicas.

## Requisitos

- Python 3.11
- Módulo `re` (já incluído na instalação padrão do Python)

## Uso

1. **Preparação dos Dados**: Seu arquivo de texto deve listar os itens a serem categorizados, com suas descrições separadas por " - ". Por exemplo:
   
   ```
   Nome do Item - característica 1 - característica 2 - ...
   ```

2. **Configuração do Script**: No início do script, ajuste os caminhos para o arquivo de entrada e para onde o arquivo de saída será salvo, conforme necessário.

3. **Execução**: Rode o script no seu ambiente Python preferido. O script processará cada linha do arquivo de entrada, identificará e categorizará as características de cada item, e salvará os resultados em um novo arquivo.

## Exemplo de Saída

```
Nome do Item: Caneta Azul; Cor: azul, Tipo: comum
Nome do Item: Caderno 100 folhas; Quantidade: 100 folhas, Tipo: espiral
```

## Personalização

Para adicionar ou modificar as categorias e unidades reconhecidas pelo script, ajuste o dicionário `unidade_para_categoria` no início do script. Isso permite uma ampla customização para atender às especificidades de diferentes tipos de dados de inventário.

## Contribuições

Contribuições para o projeto são bem-vindas. Se você deseja adicionar novas funcionalidades, melhorar o código ou expandir a lista de expressões regulares para categorização, fique à vontade para criar um pull request.
