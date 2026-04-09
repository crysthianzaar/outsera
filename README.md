# Golden Raspberry Awards API

API RESTful para consulta de intervalos de prêmios da categoria **Pior Filme** do Golden Raspberry Awards.

## Requisitos

- Python 3.12+
- Docker e Docker Compose (opcional)

## Executando com Docker

```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8080`.

## Executando localmente

### 1. Criar e ativar ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
```

### 2. Instalar dependências

```bash
pip install -r requirements-dev.txt
```

### 3. Iniciar a aplicação

```bash
python main.py
```

A API estará disponível em `http://localhost:8080`.

## Endpoints

| Método | Rota                          | Autenticação | Descrição                                 |
|--------|-------------------------------|--------------|-------------------------------------------|
| GET    | `/ping`                       | Não          | Verifica se a API está no ar              |
| GET    | `/health`                     | Não          | Status de saúde da aplicação              |
| GET    | `/producers/award-intervals`  | Opcional     | Intervalos de prêmios por produtor        |

### Exemplo de resposta — `/producers/award-intervals`

```json
{
  "min": [
    {
      "producer": "Joel Silver",
      "interval": 1,
      "previousWin": 1990,
      "followingWin": 1991
    }
  ],
  "max": [
    {
      "producer": "Matthew Vaughn",
      "interval": 13,
      "previousWin": 2002,
      "followingWin": 2015
    }
  ]
}
```

## Autenticação (opcional)

Se a variável de ambiente `API_TOKEN` estiver definida, o endpoint `/producers/award-intervals` exigirá o token via header:

```
Authorization: Bearer <API_TOKEN>
```

Os endpoints `/ping` e `/health` são sempre públicos.

### Ativando autenticação localmente

```bash
API_TOKEN=my-secret python main.py
```

### Ativando autenticação via Docker

Descomente a linha `API_TOKEN` no `docker-compose.yml`:

```yaml
environment:
  - API_TOKEN=your-secret-token
```

## Rodando os testes de integração

```bash
# Com o ambiente virtual ativado
pytest

# Com saída detalhada
pytest -v
```

## Variáveis de ambiente

| Variável       | Padrão                  | Descrição                          |
|----------------|-------------------------|------------------------------------|
| `DATABASE_URL` | `sqlite:///:memory:`    | URL do banco de dados              |
| `CSV_PATH`     | `data/movielist.csv`    | Caminho para o arquivo CSV         |
| `API_TOKEN`    | _(não definido)_        | Token de autenticação (opcional)   |

## Estrutura do projeto

```
.
├── api/                        # Rotas, autenticação e schemas de resposta
│   ├── auth.py
│   ├── routes.py
│   └── schemas.py
├── domain/
│   ├── entities/               # Entidades puras (sem dependência de framework)
│   │   └── movie.py
│   ├── repositories/           # Interface (Protocol) do repositório
│   │   └── movie_repository.py
│   └── services/               # Regras de negócio
│       └── award_interval_service.py
├── infra/
│   ├── csv/                    # Leitura do CSV
│   │   └── csv_loader.py
│   ├── db/                     # Modelos SQLAlchemy e sessão
│   │   ├── models.py
│   │   └── session.py
│   └── repositories/           # Implementação concreta do repositório
│       └── sqlalchemy_movie_repository.py
├── usecases/                   # Orquestração dos casos de uso
│   ├── get_award_intervals.py
│   └── import_movies.py
├── tests/integration/          # Testes de integração
├── app_factory.py              # Factory da aplicação Flask
├── config.py                   # Configurações via variáveis de ambiente
├── main.py                     # Entrypoint
├── data/movielist.csv          # Dados dos filmes
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
