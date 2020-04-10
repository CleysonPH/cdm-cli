# Manga Downloader

Projeto usado para estudo que é capaz de baixar mangás do site [Central de Mangas](http://centraldemangas.online/) através de um CLI .

> **OBS** Esse projeto foi feito apenas com objetivo de estudo, sobre web crawler's, cli's e publicação de pacotes Python no PyPi

## Bibliotecas utilizadas

- beautifulsoup4
- requests
- click


## Requisitos

- Python = ^3.6


## Como contribuir

1º Clone o repositório e entre na pasta do projeto
```sh
git clone https://github.com/CleysonPH/cdm-cli.git
cd cdm-cli
```

2º Instale as dependências do projeto com o Poetry
```sh
poetry install
```

3º Inicie o ambiente virtual
```sh
poetry shell
```


## Como utilizar esse projeto

Instale o projeto via pip

```sh
pip install cdm-cli
```


### Mostrar lista de mangás disponíveis

```sh
cdm show
```


### Procurar por um mangá na lista de mangás disponíveis

```sh
cdm search 'termo_da_busca'
```

Exemplo:

Mostra todos os mangás que possuem o termo 'boku' no nome
```sh
cdm search 'boku'
```


### Atualiza a lista de mangás disponíveis

```sh
cdm update
```


### Baixar um capítulo especifico de um mangá

```sh
cdm download 'nome_do_manga' --chapter numero_do_capitulo
```

Exemplo:

Baixar o capítulo 5 de Kimetsu no Yaiba
```sh
cdm download 'kimetsu no yaiba' --chapter 005
```


### Baixar todos os capítulos de um mangá

```sh
cdm download 'nome_do_manga' --all
```

Exemplo:

Baixar todos os capítulos de One Piece
```sh
cdm download 'one piece' --all
```


### Baixar o último capítulo lançando de um mangá

```sh
cdm download 'nome_do_manga' --last
```

Exemplo:

Baixar o último capítulo lançado de Solo Leveling
```sh
cdm download 'solo leveling' --last
```