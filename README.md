# Reddit Analyse

Este projeto é uma ferramenta para análise de dados do Reddit. A seguir, você encontrará as instruções para clonar e configurar o projeto.


## Clonando o Projeto

Abra o terminal e execute o seguinte comando para clonar o repositório:

```
git clone https://github.com/seuusuario/reddit-analyser.git
```

Após clonar, acesse o diretório do projeto:

```
cd reddit-analyser
```

## Configuração

1. Crie um virtual environment (recomendado python 3.12):
   
   ```
   python -m venv venv
   ```

2. Ative a virtual environment:
   
   - No Linux/macOS:
     ```
     source venv/bin/activate
     ```
   - No Windows:
     ```
     venv\Scripts\activate
     ```

3. Instale as dependências:
   
   ```
   pip install -r requirements.txt
   ```

## Executando o Projeto

Após a configuração, inicie a aplicação:
   
```
fastapi dev src/main.py
```

## Configurando Variáveis de Ambiente

Renomeie o arquivo ".env.sample" para ".env" para utilizar as configurações padrão:

```
cp .env.sample .env
```

Em seguida, edite o arquivo ".env" para ajustar as variáveis conforme necessário.

## Contribuições

Contribuições são bem-vindas! Caso queira ajudar, sinta-se à vontade para reportar issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença Apache 2.0.