# Python API Development - Comprehensive Course for Beginners

API REST feita com **FastAPI**, **SQLAlchemy** e **PostgreSQL**, com autenticação
por token **JWT** (OAuth2 Password Bearer).

### Projeto de estudo.


###  Requisitos

- Python 3.12 ou superior
- PostgreSQL rodando na máquina

### Bibliotecas

Todas as versões usadas estão fixadas no `requirements.txt`. Para instalar tudo:

```bash
pip install -r requirements.txt
```

| Biblioteca | Para que serve |
|---|---|
| `fastapi` | Framework que constrói a API e gera a documentação |
| `uvicorn` | Servidor que executa a aplicação (`uvicorn app.main:app --reload`) |
| `sqlalchemy` | ORM: faz as queries do banco usando classes Python |
| `psycopg2-binary` | Driver que conecta o SQLAlchemy no PostgreSQL |
| `python-jose` | Cria e valida o token JWT (usado em `app/oauth2.py`) |
| `passlib` | Verifica se a senha digitada bate com o hash guardado no banco |
| `bcrypt` | Algoritmo de hash usado pelo passlib |
| `python-dotenv` | Lê o arquivo `.env` e transforma em variáveis de ambiente |
| `pydantic` | Valida e converte o JSON de entrada e saída da API |

Dependências diretas dessas bibliotecas também estão listadas no
`requirements.txt` (instaladas automaticamente junto).

### Configuração

O projeto guarda **segredos** num arquivo `.env` na raiz, que **não** vai para o
GitHub. Para criar o seu:

```bash
cria .env -> na raiz do projeto

cp .env.example -> para .env mais com seus dados 
```

Depois preencha no `.env`:

```bash
# Gere uma chave nova para o SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

```bash
SECRET_KEY=<a chave que voce gerou>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SQLALCHEMY_DATABASE_URL=postgresql://postgres:suaSenha@localhost:5432/nome-do-seu-banco
```

### Banco de dados

O banco  precisa existir antes de rodar a API:

```bash
createdb nome-do-seu-banco
```

As tabelas são criadas sozinhas na primeira execução — `main.py` chama
`Base.metadata.create_all()` na inicialização.

### Rodando

```bash
uvicorn app.main:app --reload
```

A API sobe em `http://127.0.0.1:8000`

e a documentação interativa fica em `http://127.0.0.1:8000/docs`.

### Como autenticar

Rotas protegidas esperam o header:

```
Authorization: Bearer <token>
```

O token sai do `/login`:

```bash
curl -X POST http://127.0.0.1:8000/login \
  -d "username=seu@email.com&password=suaSenha"
```
+