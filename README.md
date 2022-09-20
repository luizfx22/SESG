<h1 align="center">SESPG - Summer Eletrohits Spotify Playlist Generator</h1>

## O quê diabos é SESPG?

O SESPG é um projetinho simples escrito em Python que permite criar na sua conta do Spotify as playlists com os álbums do Summer Eletrohits. Álbums icônicos da época pré-streaming que marcaram a vida de muita gente.

## Como usar?

É simples, se você já tem o Python 3.9> instalado, basta clonar o repositório e instalar as dependências, caso contrário, basta instalar e rodar os comandos abaixo:

```bash
$ git clone
$ cd SESPG
$ pip install pipenv
$ pipenv install
$ pipenv shell
```

Porém ainda não está pronto para rodar!

## Criando o .env

Para rodar o projeto, você precisa criar um arquivo chamado `.env` na raiz do projeto e preencher com as informações necessárias. Para isso, você precisa criar um app no [Spotify Developer](https://developer.spotify.com/dashboard/applications), informar a URL de callback (use a do exemplo abaixo), dai é só pegar o `client_id` e o `client_secret`.

Você irá precisar do seu nome de usuário no Spotify, você consegue ele na [página de perfil do Spotify](https://www.spotify.com/br/account/overview/);

Depois disso, basta preencher o arquivo `.env` com as informações abaixo:

```bash

SPOTIFY_USERNAME="seu_username"
SPOTIPY_CLIENT_ID="seu_client_id"
SPOTIPY_CLIENT_SECRET="seu_client_secret"

# URL de callback do seu app coloque no campo Redirect URIs do seu app no site do Spotify Developer
SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"
```

## Rodando o projeto

Agora que você já tem o `.env` preenchido, basta rodar o projeto:

```bash
$ python main.py
```
