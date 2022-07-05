# 🐍 API do Bot do Telegram

## Funcionalidades:

- Poderá cadastrar rastreio de encomenda.
- Poderá cadastrar o horário do remédio.
- Um usuário tem:
    - Nome
    - Nome de usuário único
    - Senha
- Um cliente tem:
    - Id do telegram
    - Telefone
- Um rastreio tem:
    - Código de Rastreio
    - Informações
- Uma solicitação de Rastreio tem:
    - Ligação com o rastreio
    - Ligação com o usuário
    - Nome de Rastreio
- Um horário do remédio tem:
    - Horário
- Uma solicitação de horário do remédio tem:
    - Ligação com o horário do remédio
    - Ligação com o usuário
    - Nome do remédio
- Cada usuário terá uma lista de rastreios solicitados e horários dos remédios feitos.

## Arquitetura e Ferramentas

- [Utilizamos a linguagem Python](https://www.python.org/)
- [Utilizamos FastAPI](https://fastapi.tiangolo.com/)
- Banco de Dados:
    - [PostgreSQL](https://www.postgresql.org/)
    - [MongoDB](https://www.mongodb.com/pt-br)
    - [Firebase](https://firebase.google.com/)
- Docker para o Banco de Dados
- MVC
- DDD e Arquitetura Limpa
